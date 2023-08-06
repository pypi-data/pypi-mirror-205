# import asyncio
# import json
# import logging
# import os
# import shutil
# import tempfile
#
# from math import ceil
# from typing import Any
# from typing import Dict
# from typing import Tuple
# from zipfile import ZipFile
#
# import numpy as np
#
# from tpu_tlm_is.base import TensorDescription
# from tpu_tlm_is.base.number_types import UserNumberType
# from tpu_tlm_is.base.number_types import TpuNumberType
# from tpu_tlm_is.base.number_types import STR_TO_USER_NUMBER_TYPE
# from tpu_tlm_is.base.number_types import STR_TO_TPU_NUMBER_TYPE
# from tpu_tlm_is.models.iotools import post_process
# from tpu_tlm_is.models.iotools import pre_process
# from pytpu.pytpu import TPUDevice, TPUProgram, TPUInference, TPU  # type: ignore
# from pytpu.pytpu import TPUProcessingMode
# from pytpu.pytpu import load_inference
# from pytpu.pytpu import get_inference
# from pytpu.pytpu import submit_inference
# from ..tools.helpers import get_tpu_devices
# from ..tools.helpers import get_tpu_parameters
# from ..tools.helpers import to_raw
#
#
# __all__ = [
#     'TpuRunner',
# ]
#
# LOGGER = logging.getLogger(__name__)
# _SUFFIX = ':0'
#
#
# def _get_tensor_description(io_: Dict[str, Any], cwl: int) -> TensorDescription:
#     if 'user_shape' in io_.keys():
#         LOGGER.debug('Generate NON-RAW descriptions')
#         return TensorDescription(
#             user_shape_mask=tuple(tuple([True, ] * abs(p[0]) + [False, ] * s + [True, ] * abs(p[1])
#                                   for p, s in zip(io_['padding'], io_['user_shape']))),
#             user_order=io_['user_order'],
#             user_dtype=STR_TO_USER_NUMBER_TYPE[io_['user_dtype']],
#             tpu_shape=io_['tpu_shape'],
#             tpu_order=io_['tpu_order'],
#             tpu_dtype=STR_TO_TPU_NUMBER_TYPE[io_['tpu_dtype']],
#             scales=tuple([float(s) for s in io_['scales']]),
#             anchor=io_['anchor'],
#         )
#     else:
#         LOGGER.debug('Generate RAW descriptions')
#         return TensorDescription(
#             user_shape_mask=((False, ), tuple([False, ] * int(io_['size'])), ),
#             user_order=('N', 'C', ),
#             user_dtype=UserNumberType.INT8,
#             tpu_shape=(1, ceil(int(io_['size']) / cwl), np.minimum(cwl, int(io_['size']))),
#             tpu_order=('N', 'C', 'B'),
#             tpu_dtype=TpuNumberType.INT8,
#             scales=(1.0, ),
#         )
#
#
# def _tensor_as_node(node: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], bool]:
#     node_tensor = {}
#     _len_suffix = len(_SUFFIX)
#     flag_suffix = False
#     for key, data in node.items():
#         if key[-_len_suffix:] == _SUFFIX:
#             node_tensor[key[:-_len_suffix]] = data
#             flag_suffix = True
#         else:
#             node_tensor[key] = data
#     return node_tensor, flag_suffix
#
#
# def _node_as_tensor(node: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
#     node_tensor = {}
#     _len_suffix = len(_SUFFIX)
#     for key, data in node.items():
#         if key[-_len_suffix:] == _SUFFIX:
#             node_tensor[key] = data
#         else:
#             node_tensor[key + _SUFFIX] = data
#
#     return node_tensor
#
#
# class TpuRunner:
#     def __init__(self, program_path):
#         self.program_path = program_path
#         self._tpu_par = None
#         self._tensor_descriptions = None
#
#     def __enter__(self):
#         dev_name = TPU.list_devices()[0] # first device
#         self.device = TPU.get_device(dev_name)
#         self.program = TPU.get_program(self.program_path)
#         self.device.load_program(self.program)
#         self.program.device = self.device
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.program.close()
#         self.device.close()
#
#     def __call__(self, input_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
#         input_data, flag_suffix = _tensor_as_node(input_data)
#         with self.program.inference() as inference:
#             output_data = inference.sync(input_data)
#             if flag_suffix:
#                 output_data = _node_as_tensor(output_data)
#
#         return output_data
#
#     # pyprocessing
#     def create_raw_programe(self):
#         with tempfile.TemporaryDirectory() as tempdir:
#             with ZipFile(self.program_path, 'r') as zip_obj:
#                 zip_obj.extractall(tempdir)
#
#             with open(os.path.join(tempdir, 'metadata.json'), 'r') as metadata_file:
#                 metadata = json.load(metadata_file)
#
#             tpu_par = get_tpu_parameters(metadata['hardware_parameters'])
#
#             tensor_descriptions: Dict[str, TensorDescription] = dict()
#             for _, region in metadata['inputs'].items():
#                 for name, io_ in region.items():
#                     tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)
#                     LOGGER.debug(f'Input: {name}, {[len(s) for s in tensor_descriptions[name].user_shape_mask]}, '
#                                  f'{tensor_descriptions[name].user_dtype}')
#
#             for _, region in metadata['outputs'].items():
#                 for name, io_ in region.items():
#                     tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)
#
#             with open(os.path.join(tempdir, 'metadata.json'), 'w') as metadata_file:
#                 raw_metadata = to_raw(metadata)
#                 json.dump(raw_metadata, metadata_file)
#
#             with tempfile.NamedTemporaryFile() as temp_file:
#                 self.program_path = os.path.join(tempdir, 'program_raw.tpu')
#                 shutil.make_archive(temp_file.name, 'zip', tempdir)
#                 os.rename(temp_file.name + '.zip', self.program_path)
#                 LOGGER.debug(f'Raw program saved to {self.program_path}')
#
#             self._tpu_par = tpu_par
#             self._tensor_descriptions = tensor_descriptions
#
#     def run_with_pyprocessing(self, input_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
#         self.create_raw_programe()
#
#         input_data, flag_suffix = _tensor_as_node(input_data)
#         mode = TPUProcessingMode.kRaw.value
#         input_data = pre_process(self._tpu_par, input_data, self._tensor_descriptions)
#
#         # Convert to raw program format
#         input_data = {n: v.reshape((1, -1)).view(np.int8) for n, v in input_data.items()}
#
#         with self.program.inference() as inference:
#             tpu_input_buf, tpu_output_buf, ctx = load_inference(input_data, self.program)
#             inference.set_inputs(tpu_input_buf)
#             inference.set_outputs(tpu_output_buf)
#             self.device.run_inference(inference, mode)
#             output_data = get_inference(self.program, tpu_output_buf, ctx, as_dict=True)
#             output_data = post_process(self._tpu_par, output_data, self._tensor_descriptions)
#
#             if flag_suffix:
#                 output_data = _node_as_tensor(output_data)
#
#             return output_data
#
