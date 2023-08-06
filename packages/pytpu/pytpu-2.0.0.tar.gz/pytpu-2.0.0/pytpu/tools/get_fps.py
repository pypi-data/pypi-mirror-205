# # pylint: disable=E0611,C0103,R0914,W1514,R1735,R1734,C0206
#
# import asyncio
# from typing import Dict, List
# import time
# from zipfile import ZipFile
# import contextlib
# import tempfile
# import json
# import os
# import shutil
# import numpy as np
# import concurrent.futures
# import threading
# from collections import deque
# from math import ceil
#
# from ..pytpu import TPU                 # type: ignore
# from ..pytpu import TPUDevice           # type: ignore
# from ..pytpu import TPUProgram          # type: ignore
# from ..pytpu import TPUInference        # type: ignore
# from ..pytpu import TPUProcessingMode   # type: ignore
# from ..pytpu import load_inference      # type: ignore
# from ..pytpu import get_inference       # type: ignore
# from ..pytpu import submit_inference
# from ..tools.helpers import to_raw
# from ..tools.helpers import STR_TO_DTYPE
# from ..tools.helpers import get_tpu_devices
#
#
# __all__ = [
#     'get_fps',
# ]
#
#
# def get_fps(program_path: str, raw: bool = False, n_queries: int = 100, n_proc: int = 1) -> float:
#     print(f'\nStart measure performance for program: {program_path}')
#     print(f'\nConfiguration: RAW = {raw}; queries = {n_queries}; processes = {n_proc}')
#
#     _thread_to_inference = dict()
#
#     def worker_init():
#         tpu_program = tpu_program_queque.pop()
#         thread = threading.current_thread()
#         inference = TPU.get_inference(tpu_program)
#         _thread_to_inference[thread] = inference
#
#     def target(input_):
#         thread = threading.current_thread()
#         inference = _thread_to_inference[thread]
#         out = inference.sync(input_)
#         return out
#
#     with tempfile.TemporaryDirectory() as tempdir:
#         with ZipFile(program_path, 'r') as zip_obj:
#             zip_obj.extractall(tempdir)
#
#         with open(os.path.join(tempdir, 'metadata.json'), 'r') as metadata_file:
#             metadata = json.load(metadata_file)
#
#
#         layers_param = dict()
#         for _, region in metadata['inputs'].items():
#             for name, inp in region.items():
#                 layers_param[inp['anchor']] = inp
#
#         data_list = list()
#         for _ in range(n_queries):
#             for name in layers_param:
#                 data_shape = layers_param[name]['user_shape']
#                 data_type = STR_TO_DTYPE[layers_param[name]['user_dtype']]
#                 generated_data = (np.random.rand(*data_shape) * 2 - 1) * 100
#                 generated_data = generated_data.astype(data_type)
#                 generated_data_dict = {name: generated_data}
#                 data_list.append(generated_data_dict)
#
#         with contextlib.ExitStack() as tpu_device_stack:
#             tpu_devices = [tpu_device_stack.enter_context(TPU.open(i)) for i in TPU.list_devices()]
#
#             with contextlib.ExitStack() as tpu_program_stack:
#                 tpu_programs = [tpu_program_stack.enter_context(tpu.load(program_path)) for tpu in tpu_devices]
#                 tpu_program_queque = deque(tuple(tpu_programs) * ceil(n_proc / len(tpu_devices)))
#
#                 time_0 = time.time()
#                 try:
#                     with concurrent.futures.ThreadPoolExecutor(max_workers=n_proc,
#                                        initializer=worker_init, initargs=()) as executor:
#                         futures = []
#
#                         for input_ in data_list:
#                             futures.append(executor.submit(target, input_))
#
#                         for future in concurrent.futures.as_completed(futures):
#                             out = future.result()
#
#                 finally:
#                     for inference in _thread_to_inference.values():
#                        inference.close()
#                 time_1 = time.time()
#                 fps = n_queries / (time_1 - time_0)
#
#     return fps
#
