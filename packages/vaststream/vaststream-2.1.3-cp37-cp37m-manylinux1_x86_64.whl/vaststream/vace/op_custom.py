# """
# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# The information contained herein is confidential property of the company.
# The user, copying, transfer or disclosure of such information is prohibited
# except by express written agreement with VASTAI Technologies Co., Ltd.
# """
# # coding: utf-8

# from _vaststream_pybind11 import vace as _vace
# from typing import List
# from typing import Any
# from .common import *
# from .utils import *

# # =========================== API =============================
# def loadCustomizedOp(elfFilePath: str) -> Any:
#     """
#     loadCustomizedOp.\n
#     ----------\n
#     elfFilePath [in]: l.\n
#     """
#     opInfoPy = _vace.customizedOpInfoPy()
#     err = _vace.createDecoderChannel(elfFilePath, opInfoPy)
#     if err != _vace.vaceER_SUCCESS:
#         raise Exception(f"{loadCustomizedOp.__name__} return error {err}.")
#     return opInfoPy

# @err_check
# def destroyCustomizedOpInfo(opInfo:Any) -> int:
#     """
#     destroyCustomizedOpInfo.\n
#     ----------\n
#     opInfo [in]: l.\n
#     """
#     return _vace.destroyCustomizedOpInfo(opInfo)

# @err_check
# def unloadCustomizedOps(opInfo:Any) -> int:
#     """
#     unloadCustomizedOps.\n
#     ----------\n
#     CustomizedOpInfo [in]: l.\n
#     """
#     return _vace.unloadCustomizedOps(opInfo)

# def getCustomizedOpCount(opInfo) -> int:
#     """
#     getCustomizedOpCount.\n
#     ----------\n
#     opInfo [in]: l.\n
#     """
#     return _vace.getCustomizedOpCount(opInfo)

# def getCustomizedOpName(opInfo:Any, 
#                         index:int) -> str:
#     """
#     getCustomizedOpName.\n
#     ----------\n
#     opInfo [in]: l.\n
#     index [in]: l.\n
#     """
#     return _vace.getCustomizedOpName(opInfo, index)

# def createCustomizedOp(opInfo:Any, 
#                        opname:str) -> Any:
#     """
#     createCustomizedOp.\n
#     ----------\n
#     opInfo [in]: l.\n
#     opname [in]: l.\n
#     op [in]: l.\n
#     """
#     return _vace.createCustomizedOp(opInfo, opname)

# def setCustomizedOpCfgCallback(op:Any, 
#                                opCfgCallback:CustomizedOpCallback) -> int:
#     """
#     setCustomizedOpCfgCallback.\n
#     ----------\n
#     op [in]: l.\n
#     opCfgCallback [in]: l.\n
#     """
#     err = _vace.setCustomizedOpCfgCallback(op, opCfgCallback)
#     if err != _vace.vaceER_SUCCESS:
#         raise Exception(f"{loadCustomizedOp.__name__} return error {err}.")
#     return err



