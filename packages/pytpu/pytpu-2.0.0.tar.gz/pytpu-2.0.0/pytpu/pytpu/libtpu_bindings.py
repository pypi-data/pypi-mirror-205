import json
from ctypes import (CDLL, c_char, c_char_p, c_int, c_void_p, c_uint8, c_size_t, c_bool, cast,
                    POINTER, CFUNCTYPE, Structure)
from enum import Enum

import numpy as np
import contextlib
from typing import Mapping
from typing import Dict
from typing import Any
import collections.abc
from ..tools.helpers import get_tpu_devices

libtpu = CDLL('/usr/lib/libtpu.2.so')
# libtpu = CDLL('libtpu-experimental/build/libtpu.so')
# libtpu = CDLL('/home/d.baburin/iva_tpu_sdk/libtpu.2/build/libtpu.2.so')

__all__ = [
    'Device',  # TODO: consider remove TPU prefix? recommended user will be "import pytpu as tpu; tpu.Device(...)"?
    'Program',
    'Inference',
    'ProcessingMode',
]


class ProcessingMode(Enum):
    RAW = 0
    PRE_PROCESS = 1
    POST_PROCESS = 2
    FULL = 3


class _TensorBufferType(Enum):
    INPUTS = 0
    OUTPUTS = 1


class Device(Structure):
    _fields_ = []

    @staticmethod
    @contextlib.contextmanager
    def open(dev_name):
        if not isinstance(dev_name, bytes):
            dev_name = dev_name.encode('utf-8')

        pointer = libtpu.tpu_create_device(c_char_p(dev_name))
        device = Device(pointer)

        yield device
        libtpu.tpu_destroy_device(pointer)

    @staticmethod
    def list_devices():
        list_devices = get_tpu_devices()
        if len(list_devices) < 1:
            raise EnvironmentError('No TPU devices found')

        return list_devices

    def __init__(self, pointer):

        super().__init__()

        self._pointer = pointer

        init_code = libtpu.tpu_init_device(pointer)
        if init_code != 0:
            raise ValueError(f'Invalid init code {init_code}: {self._get_error_message()}')

        if not libtpu.tpu_is_device_valid(self._pointer):
            raise ValueError(f'Invalid device: {self._get_error_message()}')

    def _get_error_message(self) -> str:
        msg = libtpu.tpu_get_device_error_message(self._pointer)
        return msg.decode('utf-8')

    def info(self):
        return libtpu.tpu_get_device_info(self._pointer)

    def close(self):
        libtpu.tpu_destroy_device(self._pointer)

    @contextlib.contextmanager
    def load(self, program_path, raw=False):
        if not isinstance(program_path, bytes):
            program_path = program_path.encode('utf-8')

        program_pointer = libtpu.tpu_create_program(c_char_p(program_path), raw)
        program = Program(self, program_pointer)
        libtpu.tpu_load_program(self._pointer, program_pointer)

        yield program
        libtpu.tpu_destroy_program(program_pointer)


class _TensorBufferObject(Structure):
    _fields_ = []

    def __init__(self, pointer):
        super().__init__()
        self._pointer = pointer

    def set_user_tensor_buffer_ptr(self, n, ptr):
        return libtpu.tpu_set_user_tensor_buffer_ptr(self._pointer, c_size_t(n), ptr)


class Program(Structure):
    _fields_ = []

    def __init__(self, device: Device, pointer):
        super().__init__()

        self._device = device
        self._pointer = pointer

        # Check status
        if not libtpu.tpu_is_program_valid(self._pointer):
            msg = libtpu.tpu_get_program_error_message(self._pointer)
            raise ValueError('Invalid program: ' + str(msg.decode('utf-8')))

        # Preload metadata
        metadata = json.loads(self.info())
        self._input_metadata = metadata['inputs']['1']
        self._output_metadata = metadata['outputs']['2']

    def info(self):
        return libtpu.tpu_get_program_info(self._pointer)

    def get_input_size(self, n, raw):
        return libtpu.tpu_get_input_size(self._pointer, c_size_t(n), c_bool(raw))

    def get_output_size(self, n, raw):
        return libtpu.tpu_get_output_size(self._pointer, c_size_t(n), c_bool(raw))

    def close(self):
        libtpu.tpu_destroy_program(self._pointer)

    @contextlib.contextmanager
    def inference(self):
        inference = Inference(self)
        yield inference
        inference.close()

    @contextlib.contextmanager
    def buffer(self, type_: _TensorBufferType):
        buffer_pointer = libtpu.tpu_create_tensor_buffer_object(self._pointer, type_.value)  # make pointer
        yield _TensorBufferObject(buffer_pointer)
        libtpu.tpu_destroy_tensor_buffer_object(buffer_pointer)  # destroy pointer


CTX = Any


class Inference(Structure):
    _fields_ = []

    def __init__(self, program: Program, raw: bool = False):
        super().__init__()
        self._program = program
        self._pointer = libtpu.tpu_create_inference(program._pointer)
        self._raw = raw

        # Explicitly order inputs and outputs:
        _input_tensor_name_to_input_tensor_index = {
            tensor_name: i
            for i, tensor_name in enumerate(program._input_metadata)
        }

        _output_tensor_name_to_output_tensor_index = {
            tensor_name: i
            for i, tensor_name in enumerate(program._output_metadata)
        }

        self._tensor_name_to_tensor_index: Dict[str, int] = dict()
        self._tensor_name_to_tensor_index.update(_input_tensor_name_to_input_tensor_index)
        self._tensor_name_to_tensor_index.update(_output_tensor_name_to_output_tensor_index)

        # Precalculate sizes:
        _input_sizes = {
            tensor_name: program.get_input_size(self._tensor_name_to_tensor_index[tensor_name], raw)
            for tensor_name in program._input_metadata
        }

        _output_sizes = {
            tensor_name: program.get_output_size(self._tensor_name_to_tensor_index[tensor_name], raw)
            for tensor_name in program._output_metadata
        }

        self._tensor_name_to_tensor_size: Dict[str, int] = dict()
        self._tensor_name_to_tensor_size.update(_input_sizes)
        self._tensor_name_to_tensor_size.update(_output_sizes)

    def _run(self, mode: ProcessingMode):
        libtpu.tpu_run_inference(
            self._program._device._pointer,  # device pointer
            self._pointer,  # inference pointer
            mode.value,  # pass numerical value of processing mode
        )

    def sync(self, inputs, mode: ProcessingMode = ProcessingMode.FULL):

        with contextlib.ExitStack() as buffer_exit_stack:
            # Reserve pointers for input and output buffers:
            tpu_input_buf = buffer_exit_stack.enter_context(self._program.buffer(_TensorBufferType.INPUTS))
            tpu_output_buf = buffer_exit_stack.enter_context(self._program.buffer(_TensorBufferType.OUTPUTS))

            # Load
            ctx = self._load_inference(tpu_input_buf, tpu_output_buf, inputs)

            # Run
            self._run(mode)

            # Get results:
            result = self._get_inference(ctx)

            # NOTE: only after we have a copy of results in memory as numpy arrays -
            #       we can exit from buffer_exit_stack thus releasing IO pointers!

        self._check_status()

        return result

    def _check_status(self):
        status_code = libtpu.tpu_get_inference_status(self._pointer)
        if status_code != 0:
            msg = libtpu.tpu_get_inference_error_message(self._pointer).decode('utf-8')
            raise ValueError(f'Invalid inference status code {status_code}: {msg}')

    def close(self):
        libtpu.tpu_destroy_inference(self._pointer)

    def _load_inference(self, tpu_input: _TensorBufferObject, tpu_output: _TensorBufferObject,
                        input_data: Mapping[str, np.ndarray]) -> Dict[str, CTX]:

        if not isinstance(input_data, collections.abc.Mapping):
            raise ValueError('Input data must be a mapping, got:' + str(type(input_data)))

        # Inputs:
        for tensor_name, tensor_data in input_data.items():
            tensor_idx = self._tensor_name_to_tensor_index[tensor_name]
            tensor_size = self._tensor_name_to_tensor_size[tensor_name]

            in_tensor = bytearray(tensor_data)
            p_in_tensor = (c_uint8 * tensor_size).from_buffer(in_tensor)
            tpu_input.set_user_tensor_buffer_ptr(tensor_idx, cast(p_in_tensor, POINTER(c_uint8)))

        libtpu.tpu_set_inference_inputs(self._pointer, tpu_input._pointer)

        # Outputs:
        out_ctx = dict()

        for tensor_name in self._program._output_metadata:
            tensor_idx = self._tensor_name_to_tensor_index[tensor_name]
            tensor_size = self._tensor_name_to_tensor_size[tensor_name]

            out_tensor = bytearray(np.empty((tensor_size,), dtype=np.uint8))
            p_out_tensor = (c_uint8 * tensor_size).from_buffer(out_tensor)
            c_out_ptr = cast(p_out_tensor, POINTER(c_uint8))
            tpu_output.set_user_tensor_buffer_ptr(tensor_idx, c_out_ptr)

            out_ctx[tensor_name] = c_out_ptr

        libtpu.tpu_set_inference_outputs(self._pointer, tpu_output._pointer)

        return out_ctx

    def _get_inference(self, ctx: Dict[str, CTX]) -> Dict[str, np.ndarray]:
        out_meta = self._program._output_metadata
        collected_data = dict()

        for tensor_name, out_ctx in ctx.items():
            tensor_size = self._tensor_name_to_tensor_size[tensor_name]
            data = np.ctypeslib.as_array(out_ctx, shape=(tensor_size,))

            data = _convert_from_uint8_to_user_dtype(data, out_meta[tensor_name]['user_dtype'])
            data = data.reshape(out_meta[tensor_name]['user_shape'])

            collected_data[tensor_name] = data

        return collected_data


CB_POINTER = CFUNCTYPE(None, POINTER(Inference), c_int, c_void_p)

# TPUDevice
libtpu.tpu_create_device.restype = POINTER(Device)
# libtpu.tpu_create_device.argtypes = [c_int]
libtpu.tpu_create_device.argtypes = [c_char_p]

libtpu.tpu_destroy_device.restype = c_void_p
libtpu.tpu_destroy_device.argtypes = [POINTER(Device)]

libtpu.tpu_is_device_valid.restype = c_int
libtpu.tpu_is_device_valid.argtypes = [POINTER(Device)]

libtpu.tpu_init_device.restype = c_int
libtpu.tpu_init_device.argtypes = [POINTER(Device)]

libtpu.tpu_get_device_error_message.restype = c_char_p
libtpu.tpu_get_device_error_message.argtypes = [POINTER(Device)]

libtpu.tpu_get_device_info.restype = c_char_p
libtpu.tpu_get_device_info.argtypes = [POINTER(Device)]

libtpu.tpu_load_program.restype = c_int
libtpu.tpu_load_program.argtypes = [POINTER(Device), POINTER(Program)]

libtpu.tpu_run_inference.restype = c_int
libtpu.tpu_run_inference.argtypes = [POINTER(Device), POINTER(Inference), c_int]

libtpu.tpu_submit_inference.restype = c_int
libtpu.tpu_submit_inference.argtypes = [POINTER(Device), POINTER(Inference), c_int, CB_POINTER, c_void_p]

# TPUProgram
libtpu.tpu_create_program.restype = POINTER(Program)
libtpu.tpu_create_program.argtypes = [POINTER(c_char), c_int]

libtpu.tpu_destroy_program.restype = c_void_p
libtpu.tpu_destroy_program.argtypes = [POINTER(Program)]

libtpu.tpu_is_program_valid.restype = c_int
libtpu.tpu_is_program_valid.argtypes = [POINTER(Program)]

libtpu.tpu_get_program_info.restype = c_char_p
libtpu.tpu_get_program_info.argtypes = [POINTER(Program)]

libtpu.tpu_get_program_error_message.restype = c_char_p
libtpu.tpu_get_program_error_message.argtypes = [POINTER(Program)]

libtpu.tpu_get_batch_size.restype = c_size_t
libtpu.tpu_get_batch_size.argtypes = [POINTER(Program)]

libtpu.tpu_get_input_count.restype = c_size_t
libtpu.tpu_get_input_count.argtypes = [POINTER(Program)]

libtpu.tpu_get_input_size.restype = c_size_t
libtpu.tpu_get_input_size.argtypes = [POINTER(Program), c_size_t, c_bool]

libtpu.tpu_get_output_count.restype = c_size_t
libtpu.tpu_get_output_count.argtypes = [POINTER(Program)]

libtpu.tpu_get_output_size.restype = c_size_t
libtpu.tpu_get_output_size.argtypes = [POINTER(Program), c_size_t, c_bool]

# TPUTensorBufferObject
libtpu.tpu_create_tensor_buffer_object.restype = POINTER(_TensorBufferObject)
libtpu.tpu_create_tensor_buffer_object.argtypes = [POINTER(Program), c_int]

libtpu.tpu_destroy_tensor_buffer_object.restype = c_void_p
libtpu.tpu_destroy_tensor_buffer_object.argtypes = [POINTER(_TensorBufferObject)]

libtpu.tpu_process_tensor_buffers.restype = c_void_p
libtpu.tpu_process_tensor_buffers.argtypes = [POINTER(_TensorBufferObject)]

libtpu.tpu_get_tensor_buffer_ptr.restype = POINTER(c_uint8)
libtpu.tpu_get_tensor_buffer_ptr.argtypes = [POINTER(_TensorBufferObject), c_size_t, c_bool]

libtpu.tpu_set_user_tensor_buffer_ptr.restype = POINTER(c_uint8)
libtpu.tpu_set_user_tensor_buffer_ptr.argtypes = [POINTER(_TensorBufferObject), c_size_t, POINTER(c_uint8)]

# TPUInference
libtpu.tpu_create_inference.restype = POINTER(Inference)
libtpu.tpu_create_inference.argtypes = [POINTER(Program)]

libtpu.tpu_destroy_inference.restype = c_void_p
libtpu.tpu_destroy_inference.argtypes = [POINTER(Inference)]

libtpu.tpu_get_inference_program.restype = POINTER(Program)
libtpu.tpu_get_inference_program.argtypes = [POINTER(Inference)]

libtpu.tpu_get_inference_inputs.restype = POINTER(_TensorBufferObject)
libtpu.tpu_get_inference_inputs.argtypes = [POINTER(Inference)]

libtpu.tpu_set_inference_inputs.restype = POINTER(_TensorBufferObject)
libtpu.tpu_set_inference_inputs.argtypes = [POINTER(Inference), POINTER(_TensorBufferObject)]

libtpu.tpu_get_inference_outputs.restype = POINTER(_TensorBufferObject)
libtpu.tpu_get_inference_outputs.argtypes = [POINTER(Inference)]

libtpu.tpu_set_inference_outputs.restype = POINTER(_TensorBufferObject)
libtpu.tpu_set_inference_outputs.argtypes = [POINTER(Inference), POINTER(_TensorBufferObject)]

libtpu.tpu_get_inference_status.restype = c_int
libtpu.tpu_get_inference_status.argtypes = [POINTER(Inference)]

libtpu.tpu_get_inference_error_message.restype = c_char_p
libtpu.tpu_get_inference_error_message.argtypes = [POINTER(Inference)]


def _convert_from_uint8_to_user_dtype(data, user_dtype):
    if 'int' in user_dtype:
        return data.view(user_dtype)
    elif 'float16' == user_dtype:
        return data.view(np.uint16).view(user_dtype)
    elif 'float32' == user_dtype:
        return data.view(np.uint32).view(user_dtype)
    else:
        raise AssertionError(f'{user_dtype} as user_dtype does not support!')
