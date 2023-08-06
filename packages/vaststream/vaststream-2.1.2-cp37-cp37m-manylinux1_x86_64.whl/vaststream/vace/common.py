"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from _vaststream_pybind11 import vace as _vace
from typing import Any
from typing import List
from .utils import *

# =========================== ENUM =============================
class IMAGE_TYPE():
    """
    vace codec type. \n
    @enum IMG_YUV_NV12. \n
    @enum IMG_YUV_I420. \n
    @enum IMG_RGB_PLANAR. \n
    @enum IMG_RGB888. \n
    @enum IMG_BGR888. \n
    @enum IMG_GRAY. \n
    @enum IMG_FORMAT_BUTT. \n
    """
    IMG_YUV_NV12:int = _vace.imageType.vaceIMG_YUV_NV12
    IMG_YUV_I420:int = _vace.imageType.vaceIMG_YUV_I420
    IMG_RGB_PLANAR:int = _vace.imageType.vaceIMG_RGB_PLANAR
    IMG_RGB888:int = _vace.imageType.vaceIMG_RGB888
    IMG_BGR888:int = _vace.imageType.vaceIMG_BGR888
    IMG_GRAY:int = _vace.imageType.vaceIMG_RGB888
    IMG_FORMAT_BUTT:int = _vace.imageType.vaceIMG_FORMAT_BUTT

class OP_TYPE():
    """
    vace op type. \n
    @enum OP_MEM_COPY_OP. \n
    @enum OP_CUSTOMIZED_OP. \n
    @enum OP_CROP. \n
    @enum OP_CVT_COLOR. \n
    @enum OP_BATCH_CROP_RESIZE. \n
    @enum OP_WARP_AFFINE. \n
    @enum OP_FLIP. \n
    @enum OP_SCALE. \n
    @enum OP_COPY_MAKE_BOARDER. \n
    @enum OP_FUSION_OP_YUV_NV12_RESIZE_2RGB_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR. \n
    @enum OP_FUSION_OP_YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR. \n
    @enum OP_FUSION_OP_RGB_CVTCOLOR_NORM_TENSOR. \n
    @enum OP_FUSION_OP_RGB_RESIZE_CVTCOLOR_NORM_TENSOR. \n
    @enum OP_FUSION_OP_RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR. \n
    @enum OP_FUSION_OP_RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR. \n
    @enum OP_FUSION_OP_RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR. \n
    @enum OP_FUSION_OP_MAX_NUM. \n
    """
    OP_MEM_COPY_OP:int = _vace.opType.vaceOP_MEM_COPY_OP
    OP_CUSTOMIZED_OP:int = _vace.opType.vaceOP_CUSTOMIZED_OP
    OP_RESIZE:int = _vace.opType.vaceOP_RESIZE
    OP_CROP:int = _vace.opType.vaceOP_CROP
    OP_CVT_COLOR:int = _vace.opType.vaceOP_CVT_COLOR
    OP_BATCH_CROP_RESIZE:int = _vace.opType.vaceOP_BATCH_CROP_RESIZE
    OP_WARP_AFFINE:int = _vace.opType.vaceOP_WARP_AFFINE
    OP_FLIP:int = _vace.opType.vaceOP_FLIP
    OP_SCALE:int = _vace.opType.vaceOP_SCALE
    OP_COPY_MAKE_BOARDER:int = _vace.opType.vaceOP_COPY_MAKE_BOARDER
    OP_FUSION_OP_YUV_NV12_RESIZE_2RGB_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_RESIZE_2RGB_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR
    OP_FUSION_OP_YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR
    OP_FUSION_OP_RGB_CVTCOLOR_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_RGB_CVTCOLOR_NORM_TENSOR
    OP_FUSION_OP_RGB_RESIZE_CVTCOLOR_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_RGB_RESIZE_CVTCOLOR_NORM_TENSOR
    OP_FUSION_OP_RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR
    OP_FUSION_OP_RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR
    OP_FUSION_OP_RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR:int = _vace.opType.vaceOP_FUSION_OP_RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR
    OP_FUSION_OP_MAX_NUM:int = _vace.opType.vaceOP_FUSION_OP_MAX_NUM

class RESIZE_TYPE():
    """
    vace resize type. \n
    @enum RESIZE_NO_RESIZE. \n
    @enum RESIZE_BILINEAR. \n
    @enum RESIZE_NEAREST. \n
    @enum RESIZE_BICUBIC. \n
    @enum RESIZE_LANCOZ. \n
    @enum RESIZE_BILINEAR_PILLOW. \n
    @enum RESIZE_BILINEAR_CV. \n
    @enum RESIZE_LANCZOS_PILLOW. \n
    @enum RESIZE_LANCZOS_CV. \n
    @enum RESIZE_BOX_PILLOW. \n
    @enum RESIZE_HAMMING_PILLOW. \n
    @enum RESIZE_BICUBIC_PILLOW. \n
    @enum RESIZE_BUTT. \n
    """
    RESIZE_NO_RESIZE:int = _vace.resizeType.vaceRESIZE_NO_RESIZE
    RESIZE_BILINEAR:int = _vace.resizeType.vaceRESIZE_BILINEAR
    RESIZE_NEAREST:int = _vace.resizeType.vaceRESIZE_NEAREST
    RESIZE_BICUBIC:int = _vace.resizeType.vaceRESIZE_BICUBIC
    RESIZE_LANCOZ:int = _vace.resizeType.vaceRESIZE_LANCOZ
    RESIZE_BILINEAR_PILLOW:int = _vace.resizeType.vaceRESIZE_BILINEAR_PILLOW
    RESIZE_BILINEAR_CV:int = _vace.resizeType.vaceRESIZE_BILINEAR_CV
    RESIZE_LANCZOS_PILLOW:int = _vace.resizeType.vaceRESIZE_LANCZOS_PILLOW
    RESIZE_LANCZOS_CV:int = _vace.resizeType.vaceRESIZE_LANCZOS_CV
    RESIZE_BOX_PILLOW:int = _vace.resizeType.vaceRESIZE_BOX_PILLOW
    RESIZE_HAMMING_PILLOW:int = _vace.resizeType.vaceRESIZE_HAMMING_PILLOW
    RESIZE_BICUBIC_PILLOW:int = _vace.resizeType.vaceRESIZE_BICUBIC_PILLOW
    RESIZE_BUTT:int = _vace.resizeType.vaceRESIZE_BUTT

class COLOR_CVT_CODE():
    """
    vace color cvtdoce type. \n
    @enum COLOR_YUV2RGB_NV12. \n
    @enum COLOR_YUV2BGR_NV12. \n
    @enum COLOR_NO_CHANGE. \n
    @enum COLOR_BGR2RGB. \n
    @enum COLOR_RGB2BGR. \n
    @enum COLOR_BGR2RGB_INTERLEAVE2PLANAR. \n
    @enum COLOR_RGB2BGR_INTERLEAVE2PLANAR. \n
    @enum COLOR_BGR2BGR_INTERLEAVE2PLANAR. \n
    @enum COLOR_RGB2RGB_INTERLEAVE2PLANAR. \n
    @enum COLOR_YUV2GRAY_NV12. \n
    @enum COLOR_BGR2GRAY_INTERLEAVE. \n
    @enum COLOR_RGB2GRAY_PLANAR. \n
    @enum COLOR_BGR2YUV_NV12_PLANAR. \n
    @enum COLOR_CVT_CODE_BUTT. \n
    """

    COLOR_YUV2RGB_NV12:int = _vace.colorCvtCode.vaceCOLOR_YUV2RGB_NV12
    COLOR_YUV2BGR_NV12:int = _vace.colorCvtCode.vaceCOLOR_YUV2BGR_NV12
    COLOR_NO_CHANGE:int = _vace.colorCvtCode.vaceCOLOR_NO_CHANGE
    COLOR_BGR2RGB:int = _vace.colorCvtCode.vaceCOLOR_BGR2RGB
    COLOR_RGB2BGR:int = _vace.colorCvtCode.vaceCOLOR_RGB2BGR
    COLOR_BGR2RGB_INTERLEAVE2PLANAR:int = _vace.colorCvtCode.vaceCOLOR_BGR2RGB_INTERLEAVE2PLANAR
    COLOR_RGB2BGR_INTERLEAVE2PLANAR:int = _vace.colorCvtCode.vaceCOLOR_RGB2BGR_INTERLEAVE2PLANAR
    COLOR_BGR2BGR_INTERLEAVE2PLANAR:int = _vace.colorCvtCode.vaceCOLOR_BGR2BGR_INTERLEAVE2PLANAR
    COLOR_RGB2RGB_INTERLEAVE2PLANAR:int = _vace.colorCvtCode.vaceCOLOR_RGB2RGB_INTERLEAVE2PLANAR
    COLOR_YUV2GRAY_NV12:int = _vace.colorCvtCode.vaceCOLOR_YUV2GRAY_NV12
    COLOR_BGR2GRAY_INTERLEAVE:int = _vace.colorCvtCode.vaceCOLOR_BGR2GRAY_INTERLEAVE
    COLOR_BGR2GRAY_PLANAR:int = _vace.colorCvtCode.vaceCOLOR_BGR2GRAY_PLANAR
    COLOR_RGB2GRAY_INTERLEAVE:int = _vace.colorCvtCode.vaceCOLOR_RGB2GRAY_INTERLEAVE
    COLOR_RGB2GRAY_PLANAR:int = _vace.colorCvtCode.vaceCOLOR_RGB2GRAY_PLANAR
    COLOR_RGB2YUV_NV12_PLANAR:int = _vace.colorCvtCode.vaceCOLOR_RGB2YUV_NV12_PLANAR
    COLOR_BGR2YUV_NV12_PLANAR:int = _vace.colorCvtCode.vaceCOLOR_BGR2YUV_NV12_PLANAR  
    COLOR_CVT_CODE_BUTT:int = _vace.colorCvtCode.vaceCOLOR_CVT_CODE_BUTT

class COLOR_SPACE():
    """
    vace color space. \n
    @enum COLOR_SPACE_BT709. \n
    @enum COLOR_SPACE_BT601. \n
    @enum COLOR_SPACE_BUTT. \n
    """

    COLOR_SPACE_BT709:int = _vace.colorSpace.vaceCOLOR_SPACE_BT709
    COLOR_SPACE_BT601:int = _vace.colorSpace.vaceCOLOR_SPACE_BT601
    COLOR_SPACE_BUTT:int = _vace.colorSpace.vaceCOLOR_SPACE_BUTT

class FLIP_TYPE():
    """
    vace flip type. \n
    @enum FLIP_X_AXIS. \n
    @enum FLIP_Y_AXIS. \n
    @enum FLIP_BOTH_AXES. \n
    """
    
    FLIP_X_AXIS:int = _vace.flipType.vaceFLIP_X_AXIS
    FLIP_Y_AXIS:int = _vace.flipType.vaceFLIP_Y_AXIS
    FLIP_BOTH_AXES:int = _vace.flipType.vaceFLIP_BOTH_AXES

class PADDING_TYPE():
    """
    vace padding type. \n
    @enum EDGE_PADDING_TYPE_CONSTANT. \n
    @enum EDGE_PADDING_REPLICATE. \n
    @enum EDGE_PADDING_TYPE_REFLECT. \n
    @enum EDGE_PADDING_TYPE_BUTT. \n
    """

    EDGE_PADDING_TYPE_CONSTANT:int = _vace.paddingType.vaceEDGE_PADDING_TYPE_CONSTANT
    EDGE_PADDING_REPLICATE:int = _vace.paddingType.vaceEDGE_PADDING_REPLICATE
    EDGE_PADDING_TYPE_REFLECT:int = _vace.paddingType.vaceEDGE_PADDING_TYPE_REFLECT
    EDGE_PADDING_TYPE_BUTT:int = _vace.paddingType.vaceEDGE_PADDING_TYPE_BUTT

class WARP_AFFINE_MODE():
    """
    vace warp affine mode. \n
    @enum WARP_AFFINE_MODE_NEAREST. \n
    @enum WARP_AFFINE_MODE_BILINEAR. \n
    @enum WARP_AFFINE_MODE_BUTT. \n
    """

    WARP_AFFINE_MODE_NEAREST:int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_NEAREST
    WARP_AFFINE_MODE_BILINEAR:int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_BILINEAR
    WARP_AFFINE_MODE_BUTT:int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_BUTT

class DATA_TYPE():
    """
    vace data type. \n
    @enum DT_INT. \n
    @enum DT_UINT_8. \n
    @enum DT_UINT_16. \n
    @enum DT_UINT_32. \n
    @enum DT_UINT_64. \n
    @enum DT_FLOAT. \n
    @enum DT_FLOAT_16. \n
    @enum DT_DOUBLE. \n
    """

    DT_INT:int = _vace.dataType.vaceDT_INT     
    DT_UINT_8:int = _vace.dataType.vaceDT_UINT_8      
    DT_UINT_16:int = _vace.dataType.vaceDT_UINT_16     
    DT_UINT_32:int = _vace.dataType.vaceDT_UINT_32     
    DT_UINT_64:int = _vace.dataType.vaceDT_UINT_64     
    DT_FLOAT:int = _vace.dataType.vaceDT_FLOAT       
    DT_FLOAT_16:int = _vace.dataType.vaceDT_FLOAT_16    
    DT_DOUBLE:int = _vace.dataType.vaceDT_DOUBLE   

class PARAM_TYPE():
    """
    vace param type. \n
    @enum PARAM_ELEMENT. \n
    @enum PARAM_ARRAY. \n
    @enum PARAM_TENSOR. \n
    """

    PARAM_ELEMENT:int = _vace.paramType.vacePARAM_ELEMENT
    PARAM_ARRAY:int = _vace.paramType.vacePARAM_ARRAY
    PARAM_TENSOR:int = _vace.paramType.vacePARAM_TENSOR

class NORM_TYPE():
    """
    vace norm type. \n
    @enum NORM_NORMALIZATION_NONE. \n
    @enum NORM_EQUAL. \n
    @enum NORM_MINUSMEAN. \n
    @enum NORM_MINUSMEAN_DIVSTD. \n
    @enum NORM_DIV255_MINUSMEAN_DIVSTD. \n
    @enum NORM_DIV1275_MINUSONE. \n
    @enum NORM_DIV255. \n
    @enum NORM_NORMALIZATION_NONE_BUTT. \n
    """

    NORM_NORMALIZATION_NONE:int = _vace.normType.vaceNORM_NORMALIZATION_NONE
    NORM_EQUAL:int = _vace.normType.vaceNORM_EQUAL
    NORM_MINUSMEAN:int = _vace.normType.vaceNORM_MINUSMEAN
    NORM_MINUSMEAN_DIVSTD:int = _vace.normType.vaceNORM_MINUSMEAN_DIVSTD
    NORM_DIV255_MINUSMEAN_DIVSTD:int = _vace.normType.vaceNORM_DIV255_MINUSMEAN_DIVSTD
    NORM_DIV1275_MINUSONE:int = _vace.normType.vaceNORM_DIV1275_MINUSONE
    NORM_DIV255:int = _vace.normType.vaceNORM_DIV255
    NORM_NORMALIZATION_NONE_BUTT:int = _vace.normType.vaceNORM_NORMALIZATION_NONE_BUTT

class TENSORIZATION_TYPE():
    """
    vace tensorization type. \n
    @enum TENSORIZATION_NONE. \n
    @enum TENSORIZATION_UINT8. \n
    @enum TENSORIZATION_UINT8_INTERLEAVE. \n
    @enum TENSORIZATION_FP16. \n
    @enum TENSORIZATION_FP16_INTERLEAVE. \n
    @enum TENSORIZATION_FP16_INTERLEAVE_RGB. \n
    @enum TENSORIZATION_TYPE_BUTT. \n
    """

    TENSORIZATION_NONE:int = _vace.tensorizationType.vaceTENSORIZATION_NONE
    TENSORIZATION_UINT8:int = _vace.tensorizationType.vaceTENSORIZATION_UINT8
    TENSORIZATION_UINT8_INTERLEAVE:int = _vace.tensorizationType.vaceTENSORIZATION_UINT8_INTERLEAVE
    TENSORIZATION_FP16:int = _vace.tensorizationType.vaceTENSORIZATION_FP16
    TENSORIZATION_FP16_INTERLEAVE:int = _vace.tensorizationType.vaceTENSORIZATION_FP16_INTERLEAVE
    TENSORIZATION_FP16_INTERLEAVE_RGB:int = _vace.tensorizationType.vaceTENSORIZATION_FP16_INTERLEAVE_RGB
    TENSORIZATION_TYPE_BUTT:int = _vace.tensorizationType.vaceTENSORIZATION_TYPE_BUTT

# ================================ STRUCT ============================
class ImageDesc(_vace.imageDesc):
    imageWidth:int
    imageHeight:int
    imageWidthPitch:int
    imageHeightPitch:int
    imageFormat:IMAGE_TYPE

class CropRect(_vace.cropRect):
    start_x:int
    start_y:int
    width:int
    height:int

class PaddingValues(_vace.paddingValuesPy):
    value:List[int]

class PaddingEdges(_vace.paddingEdges):
    edgeTop:int
    edgeBottom:int
    edgeLeft:int
    edgeRight:int

class AffineMatrix(_vace.affineMatrixPy):
    matrix:List[float]

class CustomizedOpCallback():
    getInputCount:Any
    getInputShape:Any
    getOutputCount:Any
    getOutputShape:Any    
    getInputSize:Any
    getOutputSize:Any         
    isRunModelInput:int 
    isDynamicInputShape:int

# class ImageDescList(vace.imageDescList):
#     descs:List[Any]

# ================================ API ============================
def getVersion() -> str:
    """
    Get the VAME API version information.\n
    """
    return _vace.getVersion()