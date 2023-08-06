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

@err_check
def resize(resizeType: RESIZE_TYPE,
           inputImageDesc: ImageDesc,
           inputHandle: Any,
           outputImageDesc: ImageDesc,
           outputHandle: Any) -> int:
    """
    resize.\n
    ----------\n
    resizeType [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """        
    return _vace.resize(resizeType, inputImageDesc, inputHandle,
                       outputImageDesc, outputHandle)    

@err_check
def crop(cropRect: CropRect,
         inputImageDesc: ImageDesc,
         inputHandle: Any,
         outputImageDesc: ImageDesc,
         outputHandle: Any) -> int:
    """
    crop.\n
    ----------\n
    cropRect [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n

    """        
    return _vace.crop(cropRect, inputImageDesc, inputHandle,
                     outputImageDesc, outputHandle)     

@err_check
def yuvFlip(flipType: FLIP_TYPE,
            inputImageDesc: ImageDesc,
            inputHandle: Any,
            outputImageDesc: ImageDesc,
            outputHandle: Any) -> int:
    """
    crop.\n
    ----------\n
    flipType [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """       
    return _vace.yuvFlip(flipType, inputImageDesc, inputHandle,
                        outputImageDesc, outputHandle)        

@err_check
def warpAffine(affineMatrixPy:AffineMatrix, 
               warpAffineMode:WARP_AFFINE_MODE,
               borderMode:PADDING_TYPE, 
               borderValuesPy:PaddingValues,
               inputImageDesc: ImageDesc,
               inputHandle: Any,
               outputImageDesc: ImageDesc,
               outputHandle: Any) -> int:
    """
    warpAffine.\n
    ----------\n
    affineMatrixPy [in]: l.\n
    warpAffineMode [in]: l.\n
    inputImageDesc [in]: l.\n
    borderMode [in]: l.\n
    borderValuesPy [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """    
    return _vace.warpAffine(affineMatrixPy, warpAffineMode, borderMode, borderValuesPy,
                           inputImageDesc, inputHandle, outputImageDesc, outputHandle)  

@err_check
def cvtColor(cvtType: COLOR_CVT_CODE,
             cvtColorSpace: COLOR_SPACE,
             inputImageDesc: ImageDesc,
             inputHandle: Any,
             outputImageDesc: ImageDesc,
             outputHandle: Any) -> int:
    """
    cvtColor.\n
    ----------\n
    cvtType [in]: l.\n
    cvtColorSpace [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """    
    return _vace.cvtColor(cvtType, cvtColorSpace, inputImageDesc,
						 inputHandle, outputImageDesc, outputHandle)  

@err_check
def resizeCopyMakeBorder(resizeType: RESIZE_TYPE,						
						 paddingType: PADDING_TYPE,
						 paddingValues: Any,
                         paddingEdges:PaddingEdges,
						 inputImageDesc: ImageDesc,
						 inputHandle: Any,
						 outputImageDesc: ImageDesc,
						 outputHandle: Any) -> int:
    """
    resizeCopyMakeBorder.\n
    ----------\n
    cvtType [in]: l.\n
    paddingType [in]: l.\n
	paddingValues [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """    
    return _vace.resizeCopyMakeBorder(resizeType, paddingType, paddingValues, 
                                     paddingEdges, inputImageDesc, 
						             inputHandle, outputImageDesc, outputHandle)      


@err_check
def batchCropResize(cropRects: CropRect,						
                    resizeType: RESIZE_TYPE,
                    inputImageDesc: List[ImageDesc],
                    inputHandle: Any,
                    outputImageDesc: ImageDesc,
                    outputHandle: List[Any]) -> int:
    """
    batchCropResize.\n
    ----------\n
    cropRects [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """		    
    return _vace.batchCropResize(cropRects, resizeType, inputImageDesc, 
                                inputHandle, outputImageDesc, outputHandle)    

@err_check
def scale(resizeType: RESIZE_TYPE,						
          inputImageDesc: List[ImageDesc],
          inputHandle: Any,
          outputImageDesc: ImageDesc,
          outputHandle: List[Any]) -> int:
    """
    scale.\n
    ----------\n
    resizeType [in]: l.\n
    outputCount [in]: l.\n
    inputImageDesc [in]: l.\n
    inputHandle [in]: l.\n
    outputImageDesc [in]: l.\n
    outputHandle [out]: l.\n
    """		
    return _vace.scale(resizeType, inputImageDesc, 
                      inputHandle, outputImageDesc, outputHandle)    




