import os
import copy
import shutil
import numpy as np
import json
import tempfile
import zipfile
from math import ceil

from typing import Dict
from typing import Any

try:
    from tpu_tlm_is.models.iotools import tpu_encode, tpu_decode
    from tpu_tlm_is.base import TensorDescription
    from tpu_tlm_is.base import TpuParameters
    from tpu_tlm_is.base import get_hw_params
    from tpu_tlm_is.base.number_types import STR_TO_USER_NUMBER_TYPE
    from tpu_tlm_is.base.number_types import STR_TO_TPU_NUMBER_TYPE
    from tpu_tlm_is.base.number_types import UserNumberType
    from tpu_tlm_is.base.number_types import TpuNumberType
except ImportError:
    pass


class Codec:
    def __init__(self, tpu_par, tensor_descriptions):
        self._tpu_par = tpu_par
        self._tensor_descriptions = tensor_descriptions

    def encode(self, input_dict):
        return tpu_encode(self._tpu_par, input_dict, self._tensor_descriptions)

    def decode(self, output_raw_dict):
        return tpu_decode(self._tpu_par, output_raw_dict, self._tensor_descriptions)


def _to_raw_old(io_: Dict[str, Any], name: str) -> Dict[str, Any]:
    size = io_['size']
    io_out = {
        'address': io_['address'],
        'size': size,
        'user_shape': [1, size, ],
        'user_order': ['N', 'C', ],
        'user_dtype': 'int8',
        'tpu_shape': [1, size, ],
        'tpu_order': ['N', 'C', ],
        'tpu_dtype': 'int8',
        'padding': [[0, 0], [0, 0]],
        'scales': [1.0, ],
        'anchor': io_.get('anchor', name),
    }
    return io_out


def _get_tpu_parameters(hw_par: Dict[str, Any]) -> TpuParameters:
    if hw_par['cache_word_len'] == 128 and hw_par['ddr_word_len'] == 32:
        return get_hw_params('128x128').tpu_parameters
    if hw_par['cache_word_len'] == 64 and hw_par['ddr_word_len'] == 16:
        return get_hw_params('64x64').tpu_parameters
    if hw_par['cache_word_len'] == 64 and hw_par['ddr_word_len'] == 64:
        return get_hw_params('64x64_fpga').tpu_parameters

    raise NotImplementedError('Translation of such platform does not supported!')


def _to_raw(metadata: Dict[str, Any]) -> Dict[str, Any]:
    raw_metadata = copy.copy(metadata)
    for idx, region in raw_metadata['inputs'].items():
        for name, _ in region.items():
            raw_metadata['inputs'][idx][name] = _to_raw_old(metadata['inputs'][idx][name], name)

    for idx, region in raw_metadata['outputs'].items():
        for name, _ in region.items():
            raw_metadata['outputs'][idx][name] = _to_raw_old(metadata['outputs'][idx][name], name)

    return raw_metadata


def _get_tensor_description(io_: Dict[str, Any], cwl: int) -> TensorDescription:
    if 'user_shape' in io_.keys():
        return TensorDescription(
            user_shape_mask=tuple(tuple([True, ] * abs(p[0]) + [False, ] * s + [True, ] * abs(p[1])
                                  for p, s in zip(io_['padding'], io_['user_shape']))),
            user_order=io_['user_order'],
            user_dtype=STR_TO_USER_NUMBER_TYPE[io_['user_dtype']],
            tpu_shape=io_['tpu_shape'],
            tpu_order=io_['tpu_order'],
            tpu_dtype=STR_TO_TPU_NUMBER_TYPE[io_['tpu_dtype']],
            scales=tuple([float(s) for s in io_['scales']]),
            anchor=io_['anchor'],
        )
    else:
        return TensorDescription(
            user_shape_mask=((False, ), tuple([False, ] * int(io_['size'])), ),
            user_order=('N', 'C', ),
            user_dtype=UserNumberType.INT8,
            tpu_shape=(1, ceil(int(io_['size']) / cwl), np.minimum(cwl, int(io_['size']))),
            tpu_order=('N', 'C', 'B'),
            tpu_dtype=TpuNumberType.INT8,
            scales=(1.0, ),
        )


def convert_to_raw(program_path: str, raw_program_path: str) -> Codec:
    try:
        from tpu_tlm_is.base import TensorDescription
    except ImportError:
        raise BaseException('no tpu_tlm_is package found')

    with zipfile.ZipFile(program_path, 'r') as program:
        data = program.read('metadata.json')

    metadata = json.loads(data)
    tpu_par = _get_tpu_parameters(metadata['hardware_parameters'])
    tensor_descriptions: Dict[str, TensorDescription] = dict()

    for _, region in metadata['inputs'].items():
        for name, io_ in region.items():
            tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)

    for _, region in metadata['outputs'].items():
        for name, io_ in region.items():
            tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)

    with tempfile.TemporaryDirectory() as tempdir:
        with zipfile.ZipFile(program_path, 'r') as zip_obj:
            zip_obj.extractall(tempdir)

        with open(os.path.join(tempdir, 'metadata.json'), 'w') as metadata_file:
            json.dump(_to_raw(metadata), metadata_file, indent=4)

        shutil.make_archive(raw_program_path, 'zip', tempdir)
        os.rename(raw_program_path + '.zip', raw_program_path)

    return Codec(tpu_par, tensor_descriptions)
