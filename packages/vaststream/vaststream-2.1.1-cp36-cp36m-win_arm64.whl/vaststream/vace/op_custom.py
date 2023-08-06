# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = ["CustomOp"]

from _vaststream_pybind11 import vace as _vace
import ctypes
from ctypes import c_void_p
from typing import List
from .common import *
from .op_fusion import destroyOp
from .utils import *


# =========================== API =============================
class CustomOp(_vace.CustomizedOp, Op):

    def __init__(self, opName: str, elfPath: str, inputCount: int,
                 outputCount: int, inputSize: List[int], outputSize: List[int],
                 inputShape: List[List[int]], outputShape: List[List[int]],
                 isRunModelInput: bool, isDynamicInputShape: bool) -> None:
        """CustomOp class.
        
        You can load custom op from your elf file by this class.

        Args:
            opName(str): The name of the custom op.
            elfPath(str): The path of the elf file.
            inputCount(int): The input count of the custom op.
            outputCount(int): The output count of the custom op.
            inputSize(List[int]): The input size of the custom op.
            outputSize(List[int]): The output size of the custom op.
            inputShape(List[List[int]]): The input shape of the custom op.
            outputShape(List[List[int]]): The output shape of the custom op.
            isRunModelInput(bool): Wether is run model input custom op.
            isDynamicInputShape(bool): Wether is dynamic input shape custom op.
        """
        super().__init__(opName, elfPath)
        self.setInputCount(inputCount)
        self.setOutputCount(outputCount)
        self.setInputSize(inputSize)
        self.setOutputSize(outputSize)
        self.setInputShape(inputShape)
        self.setOutputShape(outputShape)
        isRunModelInput_ = 1 if isRunModelInput else 0
        self.setIsRunModelInput(isRunModelInput_)
        isDynamicInputShape_ = 1 if isDynamicInputShape else 0
        self.setIsDynamicInputShape(isDynamicInputShape_)
        self._ptr = None
        self._cfg = None
        self.create()

    def destroy(self):
        if self._ptr is not None:
            self.destroy()

    @property
    def count(self):
        return self.getCustomizedOpCount()

    def create(self):
        if self._ptr is None:
            ret = self.loadCustomizedOp()
            if ret != _vace.vaceER_SUCCESS:
                raise RuntimeError(f"load customized op error, ret: {ret}.")
            self._ptr = self.createCustomizedOp()

    @err_check
    def destroy(self):
        ret = _vace.vaceER_SUCCESS
        if self._ptr is not None:
            destroyOp(self)
            ret = self.unloadCustomizedOps()
            if ret != _vace.vaceER_SUCCESS:
                raise RuntimeError(f"unload customized op error, ret: {ret}.")
            ret = self.destroyCustomizedOpInfo()
            if ret != _vace.vaceER_SUCCESS:
                raise RuntimeError(f"destroy customized opInfo error, ret: {ret}.")
            self._ptr = None
        return ret

    @err_check
    def setConfig(self, config: dict):
        """Set custom op config.

        Please use ctypes construct the dict, because ctypes can descrition the
        real lenth in device, python can not support types such as uint16.

        Example:
            >>> import ctypes
            >>> class CustomizedCfg(ctypes.Structure):
            >>>     _fields_ = [("width", ctypes.c_int32), ("height", ctypes.c_int32),
            >>>                 ("w_pitch_in", ctypes.c_int32), ("h_pitch_in", ctypes.c_int32),
            >>>                 ("temp_buffer", ctypes.c_uint64),
            >>>                 ("model_addr", ctypes.c_uint64),
            >>>                 ("place_holder", ctypes.c_uint64 * 4)]
            >>> cfg = CustomizedCfg(...)
            >>> op.setConfig(cfg)
        
        Args:
            config(dict): The config of the custom op.
        """
        config_ptr = ctypes.cast(ctypes.byref(config), c_void_p)
        config_address = int(config_ptr.value)
        cfg_size = ctypes.sizeof(config)
        return self.setCustomizedOpConfig(config_address, cfg_size)