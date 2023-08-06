"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from _vaststream_pybind11 import vace as _vace
from typing import List
from typing import Any
from .common import *
from .utils import *

# =========================== API =============================
def createOp(opType: OP_TYPE) -> Any:
    """
    createOp.\n
    ----------\n
    OP_TYPE [in]: l.\n
    """
    return _vace.createOp(opType)

@err_check
def destroyOp(op: Any) -> int:
    """
    destroyOp.\n
    ----------\n
    VaceOp [in]: l.\n
    """
    return _vace.destroyOp(op)

def setOpAttr(op: Any, 
              attrName: str, 
              attrDType: DATA_TYPE,
              attrGType: PARAM_TYPE,
              value: Any) -> int:
    """
    setOpAttr.\n
    ----------\n
    opPy [in]: l.\n
    attrName [in]: l.\n
    attrDType [in]: l.\n
    attrGType [in]: l.\n
    args [in]: l.\n
    """
    if attrDType == DATA_TYPE.DT_INT:
        return _vace.setVaceOPAttrInt(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_UINT_8:
        return _vace.setVaceOPAttrUint8(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_UINT_16:
        return _vace.setVaceOPAttrUint16(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_UINT_32:
        return _vace.setVaceOPAttrUint32(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_UINT_64:
        return _vace.setVaceOPAttrUint64(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_FLOAT:
        return _vace.setVaceOPAttrFloat(op, attrName, attrDType, attrGType, value)
    
    elif attrDType == DATA_TYPE.DT_DOUBLE:
        return _vace.setVaceOPAttrDouble(op, attrName, attrDType, attrGType, value)

def getOpAttr(op: Any, 
              attrName: str, 
              attrDType: DATA_TYPE) -> int:
    """
    getOpAttr.\n
    ----------\n
    opPy [in]: l.\n
    attrName [in]: l.\n
    attrDType [in]: l.\n
    """ 
    if attrDType == DATA_TYPE.DT_INT:
        return _vace.getVaceOPAttrInt(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_8:
        return _vace.getVaceOPAttrUint8(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_16:
        return _vace.getVaceOPAttrUint16(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_32:
        return _vace.getVaceOPAttrUint32(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_64:
        return _vace.getVaceOPAttrUint64(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_FLOAT:
        return _vace.getVaceOPAttrFloat(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_DOUBLE:
        return _vace.getVaceOPAttrDouble(op, attrName, attrDType)

def getOpAttrArray(op: Any, 
                   attrName: str, 
                   attrDType: DATA_TYPE, 
                   index: int) -> Any:
    """
    getOpAttrArray.\n
    ----------\n
    opPy [in]: l.\n
    attrName [in]: l.\n
    attrDType [in]: l.\n
    attrGType [in]: l.\n
    """
    if attrDType == DATA_TYPE.DT_INT:
        return _vace.getVaceOPAttrArrayInt(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_8:
        return _vace.getVaceOPAttrArrayUint8(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_16:
        return _vace.getVaceOPAttrArrayUint16(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_32:
        return _vace.getVaceOPAttrArrayUint32(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_UINT_64:
        return _vace.getVaceOPAttrArrayUint64(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_FLOAT:
        return _vace.getVaceOPAttrArrayFloat(op, attrName, attrDType)
    
    elif attrDType == DATA_TYPE.DT_DOUBLE:
        return _vace.getVaceOPAttrArrayDouble(op, attrName, attrDType)
    
def executeOp(op: Any, 
              input: Any, 
              output: Any) -> int:
    """
    executeOp.\n
    ----------\n
    opPy [in]: l.\n
    input [in]: l.\n
    attrDType [in]: l.\n
    attrGType [in]: l.\n
    """
    ret = _vace.executeOp(op, input, output)
    if ret != _vace.vaceER_SUCCESS:
        raise Exception(f"{executeOp.__name__} return error {ret}.")
    return ret