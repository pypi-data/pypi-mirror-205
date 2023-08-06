# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "RgbCropResizeCvtcolorNormal", "RgbCvtcolorNormal", "RgbLetterboxCvtcolorNormal",
    "RgbResizeCvtColorCropNormal", "RgbResizeCvtcolorNormal",
    "YuvNV12CvtcolorLetterboxNormal", "YuvNV12CropCvtColorResizeNormal",
    "YuvNV12CvtColorResizeCropNormal", "YuvNV12CvtColorResizeNormal",
    "YuvNV12Letterbox2RgbNormal", "YuvNv12Resize2RgbNormal",
    "YuvNv12ResizeCvtcolorCropNormal"
]

from .common import *
from .op_attr_desc import *
from .op_base import OpBase


class RgbCropResizeCvtcolorNormal(OpBase):
    """RgbCropResizeCvtcolorNormal class.
    
    Provides a class that calls RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR more conveniently and quickly. 
    The input image type is RGB. and crop, resize and cvtcolor operations are performed in sequence.
    
    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        crop_desc(CropDesc): Crop descrition, .
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 crop_desc: CropDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(
            iimage_desc=iimage_desc,
            oimage_desc=oimage_desc,
            crop_desc=crop_desc,
            cvt_color_desc=cvt_color_desc,
            normal_desc=normal_desc,
            scale_desc=scale_desc,
            resize_desc=resize_desc,
            tensor_desc=tensor_desc,
        )

    def _requires_inputFormat(self) -> bool:
        return True

    def type(self) -> OP_TYPE:
        return OP_TYPE.RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR


class RgbCvtcolorNormal(OpBase):
    """RgbCvtcolorNormal class.
    
    Provides a class that calls RGB_CVTCOLOR_NORM_TENSOR more conveniently and quickly. 
    The input image type is RGB. cvtcolor and normal operations are performed in sequence.
    
    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.        
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(
            iimage_desc=iimage_desc,
            cvt_color_desc=cvt_color_desc,
            normal_desc=normal_desc,
            scale_desc=scale_desc,
            tensor_desc=tensor_desc,
        )

    def type(self) -> OP_TYPE:
        return OP_TYPE.RGB_CVTCOLOR_NORM_TENSOR


class RgbLetterboxCvtcolorNormal(OpBase):
    """RgbLetterboxCvtcolorNormal class.
    
    Provides a class that calls RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR more conveniently and quickly. 
    The input image type is RGB. Letterbox and Cvtcolor operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        padding_desc(PaddingDesc): Padding descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 padding_desc: PaddingDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         padding_desc=padding_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def _requires_inputFormat(self) -> bool:
        return True

    def type(self) -> OP_TYPE:
        return OP_TYPE.RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR


class RgbResizeCvtColorCropNormal(OpBase):
    """RgbResizeCvtColorCropNormal class.
    
    Provides a class that calls RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR more conveniently and quickly. 
    The input image type is RGB. Resize, Cvtcolor, Crop and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        crop_desc(CropDesc): Crop descrition.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 crop_desc: CropDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         crop_desc=crop_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def _requires_inputFormat(self) -> bool:
        return True

    def type(self) -> OP_TYPE:
        return OP_TYPE.RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR


class RgbResizeCvtcolorNormal(OpBase):
    """RgbResizeCvtcolorNormal class.
    
    Provides a class that calls RGB_RESIZE_CVTCOLOR_NORM_TENSOR more conveniently and quickly. 
    The input image type is RGB. Resize and Cvtcolor operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def _requires_inputFormat(self) -> bool:
        return True

    def type(self) -> OP_TYPE:
        return OP_TYPE.RGB_RESIZE_CVTCOLOR_NORM_TENSOR


class YuvNV12CvtcolorLetterboxNormal(OpBase):
    """YuvNV12CvtcolorLetterboxNormal class.
    
    Provides a class that calls YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV. Cvtcolor and Letterbox operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        padding_desc(PaddingDesc): Padding descrption.
        resize_desc(ResizeDesc): Resize descrition.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 resize_desc: ResizeDesc,
                 padding_desc: PaddingDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         cvt_color_desc=cvt_color_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         padding_desc=padding_desc,
                         resize_desc=resize_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR


class YuvNV12CropCvtColorResizeNormal(OpBase):
    """YuvNV12CropCvtColorResizeNormal class.
    
    Provides a class that calls YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV. Crop, CvtColor, Resize and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        crop_desc(CropDesc): Crop descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 crop_desc: CropDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         crop_desc=crop_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR


class YuvNV12CvtColorResizeCropNormal(OpBase):
    """YuvNV12CvtColorResizeCropNormal class.
    
    Provides a class that calls YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV. CvtColor, Resize, Crop and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        crop_desc(CropDesc): Crop descrition.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 crop_desc: CropDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         crop_desc=crop_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR


class YuvNV12CvtColorResizeNormal(OpBase):
    """YuvNV12CvtColorResizeNormal class.
    
    Provides a class that calls YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV. CvtColor, Resize and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR


class YuvNV12Letterbox2RgbNormal(OpBase):
    """YuvNV12Letterbox2RgbNormal class.
    
    Provides a class that calls YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV, output image type is RGB. Letterbox and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        padding_desc(PaddingDesc): Padding descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 padding_desc: PaddingDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         padding_desc=padding_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR


class YuvNv12Resize2RgbNormal(OpBase):
    """YuvNv12Resize2RgbNormal class.
    
    Provides a class that calls YUV_NV12_RESIZE_2RGB_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV, output image type is RGB. Resize and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_RESIZE_2RGB_NORM_TENSOR


class YuvNv12ResizeCvtcolorCropNormal(OpBase):
    """YuvNv12ResizeCvtcolorCropNormal class.
    
    Provides a class that calls YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR more conveniently and quickly. 
    The input image type is YUV. Resize, Cvtcolor, Crop and Normal operations are performed in sequence.

    Args:
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        resize_desc(ResizeDesc): Resize descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        crop_desc(CropDesc): Crop descrition.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        tensor_desc(TensorDesc): Tensor descrption.
    """

    def __init__(self,
                 iimage_desc: ImageDesc,
                 oimage_desc: ImageDesc,
                 resize_desc: ResizeDesc,
                 cvt_color_desc: CvtColorDesc,
                 crop_desc: CropDesc,
                 normal_desc: NormalDesc,
                 scale_desc: ScaleDesc = None,
                 tensor_desc: TensorDesc = None):
        super().__init__(iimage_desc=iimage_desc,
                         oimage_desc=oimage_desc,
                         resize_desc=resize_desc,
                         cvt_color_desc=cvt_color_desc,
                         crop_desc=crop_desc,
                         normal_desc=normal_desc,
                         scale_desc=scale_desc,
                         tensor_desc=tensor_desc)

    def type(self) -> OP_TYPE:
        return OP_TYPE.YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR
