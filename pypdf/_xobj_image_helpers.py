"""Code in here is only used by pypdf.filters._xobj_to_image"""
import sys
from io import BytesIO
from typing import Any, List, Tuple, Union, cast
from ._utils import check_if_whitespace_only, logger_warning
from .constants import ColorSpaces
from .errors import PdfReadError
from .generic import ArrayObject, DecodedStreamObject, EncodedStreamObject, IndirectObject, NullObject
if sys.version_info[:2] >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info[:2] >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    raise ImportError("pillow is required to do image extraction. It can be installed via 'pip install pypdf[image]'")
mode_str_type: TypeAlias = Literal['', '1', 'RGB', '2bits', '4bits', 'P', 'L', 'RGBA', 'CMYK']
MAX_IMAGE_MODE_NESTING_DEPTH: int = 10

def _get_imagemode(color_space: Union[str, List[Any], Any], color_components: int, prev_mode: mode_str_type, depth: int=0) -> Tuple[mode_str_type, bool]:
    """
    Returns
        Image mode not taking into account mask(transparency)
        ColorInversion is required (like for some DeviceCMYK)
    """
    pass

def _handle_flate(size: Tuple[int, int], data: bytes, mode: mode_str_type, color_space: str, colors: int, obj_as_text: str) -> Tuple[Image.Image, str, str, bool]:
    """
    Process image encoded in flateEncode
    Returns img, image_format, extension, color inversion
    """
    pass

def _handle_jpx(size: Tuple[int, int], data: bytes, mode: mode_str_type, color_space: str, colors: int) -> Tuple[Image.Image, str, str, bool]:
    """
    Process image encoded in flateEncode
    Returns img, image_format, extension, inversion
    """
    pass