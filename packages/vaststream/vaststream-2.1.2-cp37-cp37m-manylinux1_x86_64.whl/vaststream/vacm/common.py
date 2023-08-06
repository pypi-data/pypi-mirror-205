"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from _vaststream_pybind11 import vacm as _vacm
from .utils import *

# =========================== ENUM =============================


class D_TYPE:
    """
    vacm data type.\n
    ----------\n
    @enum DT_UINT8\n
    @enum DT_INT8\n
    @enum DT_UINT16\n
    @enum DT_INT16\n
    @enum DT_UINT32\n
    @enum DT_INT32\n
    @enum DT_FLOAT16\n
    @enum DT_FLOAT32\n
    @enum DT_BFLOAT\n
    @enum DT_ANY\n
    """
    DT_UINT8: int = _vacm.dType.vacmDT_UINT8
    DT_INT8: int = _vacm.dType.vacmDT_INT8
    DT_UINT16: int = _vacm.dType.vacmDT_UINT16
    DT_INT16: int = _vacm.dType.vacmDT_INT16
    DT_UINT32: int = _vacm.dType.vacmDT_UINT32
    DT_INT32: int = _vacm.dType.vacmDT_INT32
    DT_FLOAT16: int = _vacm.dType.vacmDT_FLOAT16
    DT_FLOAT32: int = _vacm.dType.vacmDT_FLOAT32
    DT_BFLOAT: int = _vacm.dType.vacmDT_BFLOAT
    DT_ANY: int = _vacm.dType.vacmDT_ANY


# =========================== DEFINE =============================
SUCCESS = _vacm.ER_SUCCESS
ER_NOT_IMPLEMENT = _vacm.ER_NOT_IMPLEMENT
