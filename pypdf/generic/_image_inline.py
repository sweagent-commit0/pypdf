import logging
from io import BytesIO
from .._utils import WHITESPACES, StreamType, read_non_whitespace
from ..errors import PdfReadError
logger = logging.getLogger(__name__)
BUFFER_SIZE = 8192

def extract_inline_AHx(stream: StreamType) -> bytes:
    """
    Extract HexEncoded Stream from Inline Image.
    the stream will be moved onto the EI
    """
    pass

def extract_inline_A85(stream: StreamType) -> bytes:
    """
    Extract A85 Stream from Inline Image.
    the stream will be moved onto the EI
    """
    pass

def extract_inline_RL(stream: StreamType) -> bytes:
    """
    Extract RL Stream from Inline Image.
    the stream will be moved onto the EI
    """
    pass

def extract_inline_DCT(stream: StreamType) -> bytes:
    """
    Extract DCT (JPEG) Stream from Inline Image.
    the stream will be moved onto the EI
    """
    pass

def extract_inline_default(stream: StreamType) -> bytes:
    """
    Legacy method
    used by default
    """
    pass