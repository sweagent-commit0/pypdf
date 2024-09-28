"""Extract PDF text preserving the layout of the source PDF"""
import sys
from itertools import groupby
from math import ceil
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from ..._utils import logger_warning
from .. import LAYOUT_NEW_BT_GROUP_SPACE_WIDTHS
from ._font import Font
from ._text_state_manager import TextStateManager
from ._text_state_params import TextStateParams
if sys.version_info >= (3, 8):
    from typing import Literal, TypedDict
else:
    from typing_extensions import Literal, TypedDict

class BTGroup(TypedDict):
    """
    Dict describing a line of text rendered within a BT/ET operator pair.
    If multiple text show operations render text on the same line, the text
    will be combined into a single BTGroup dict.

    Keys:
        tx: x coordinate of first character in BTGroup
        ty: y coordinate of first character in BTGroup
        font_size: nominal font size
        font_height: effective font height
        text: rendered text
        displaced_tx: x coordinate of last character in BTGroup
        flip_sort: -1 if page is upside down, else 1
    """
    tx: float
    ty: float
    font_size: float
    font_height: float
    text: str
    displaced_tx: float
    flip_sort: Literal[-1, 1]

def bt_group(tj_op: TextStateParams, rendered_text: str, dispaced_tx: float) -> BTGroup:
    """
    BTGroup constructed from a TextStateParams instance, rendered text, and
    displaced tx value.

    Args:
        tj_op (TextStateParams): TextStateParams instance
        rendered_text (str): rendered text
        dispaced_tx (float): x coordinate of last character in BTGroup
    """
    pass

def recurs_to_target_op(ops: Iterator[Tuple[List[Any], bytes]], text_state_mgr: TextStateManager, end_target: Literal[b'Q', b'ET'], fonts: Dict[str, Font], strip_rotated: bool=True) -> Tuple[List[BTGroup], List[TextStateParams]]:
    """
    Recurse operators between BT/ET and/or q/Q operators managing the transform
    stack and capturing text positioning and rendering data.

    Args:
        ops: iterator of operators in content stream
        text_state_mgr: a TextStateManager instance
        end_target: Either b"Q" (ends b"q" op) or b"ET" (ends b"BT" op)
        fonts: font dictionary as returned by PageObject._layout_mode_fonts()

    Returns:
        tuple: list of BTGroup dicts + list of TextStateParams dataclass instances.
    """
    pass

def y_coordinate_groups(bt_groups: List[BTGroup], debug_path: Optional[Path]=None) -> Dict[int, List[BTGroup]]:
    """
    Group text operations by rendered y coordinate, i.e. the line number.

    Args:
        bt_groups: list of dicts as returned by text_show_operations()
        debug_path (Path, optional): Path to a directory for saving debug output.

    Returns:
        Dict[int, List[BTGroup]]: dict of lists of text rendered by each BT operator
            keyed by y coordinate
    """
    pass

def text_show_operations(ops: Iterator[Tuple[List[Any], bytes]], fonts: Dict[str, Font], strip_rotated: bool=True, debug_path: Optional[Path]=None) -> List[BTGroup]:
    """
    Extract text from BT/ET operator pairs.

    Args:
        ops (Iterator[Tuple[List, bytes]]): iterator of operators in content stream
        fonts (Dict[str, Font]): font dictionary
        strip_rotated: Removes text if rotated w.r.t. to the page. Defaults to True.
        debug_path (Path, optional): Path to a directory for saving debug output.

    Returns:
        List[BTGroup]: list of dicts of text rendered by each BT operator
    """
    pass

def fixed_char_width(bt_groups: List[BTGroup], scale_weight: float=1.25) -> float:
    """
    Calculate average character width weighted by the length of the rendered
    text in each sample for conversion to fixed-width layout.

    Args:
        bt_groups (List[BTGroup]): List of dicts of text rendered by each
            BT operator

    Returns:
        float: fixed character width
    """
    pass

def fixed_width_page(ty_groups: Dict[int, List[BTGroup]], char_width: float, space_vertically: bool) -> str:
    """
    Generate page text from text operations grouped by rendered y coordinate.

    Args:
        ty_groups: dict of text show ops as returned by y_coordinate_groups()
        char_width: fixed character width
        space_vertically: include blank lines inferred from y distance + font height.

    Returns:
        str: page text in a fixed width format that closely adheres to the rendered
            layout in the source pdf.
    """
    pass