"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from _vaststream_pybind11 import vacm as _vacm


def err_check(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret == _vacm.ER_NOT_IMPLEMENT:
            raise Exception("Not implement.")
        elif ret != _vacm.ER_SUCCESS:
            raise Exception(f"{func.__name__} return error {ret}.")
        return ret
    return wrapper
