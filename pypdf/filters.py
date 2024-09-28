"""
Implementation of stream filters for PDF.

See TABLE H.1 Abbreviations for standard filter names
"""
__author__ = 'Mathieu Fenniak'
__author_email__ = 'biziqe@mathieu.fenniak.net'
import math
import struct
import zlib
from base64 import a85decode
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from ._utils import WHITESPACES_AS_BYTES, b_, deprecate_with_replacement, deprecation_no_replacement, logger_warning, ord_
from .constants import CcittFaxDecodeParameters as CCITT
from .constants import ColorSpaces
from .constants import FilterTypeAbbreviations as FTA
from .constants import FilterTypes as FT
from .constants import ImageAttributes as IA
from .constants import LzwFilterParameters as LZW
from .constants import StreamAttributes as SA
from .errors import DeprecationError, PdfReadError, PdfStreamError
from .generic import ArrayObject, DictionaryObject, IndirectObject, NullObject

def decompress(data: bytes) -> bytes:
    """
    Decompress the given data using zlib.

    This function attempts to decompress the input data using zlib. If the
    decompression fails due to a zlib error, it falls back to using a
    decompression object with a larger window size.

    Args:
        data: The input data to be decompressed.

    Returns:
        The decompressed data.
    """
    pass

class FlateDecode:

    @staticmethod
    def decode(data: bytes, decode_parms: Optional[DictionaryObject]=None, **kwargs: Any) -> bytes:
        """
        Decode data which is flate-encoded.

        Args:
          data: flate-encoded data.
          decode_parms: a dictionary of values, understanding the
            "/Predictor":<int> key only

        Returns:
          The flate-decoded data.

        Raises:
          PdfReadError:
        """
        pass

    @staticmethod
    def encode(data: bytes, level: int=-1) -> bytes:
        """
        Compress the input data using zlib.

        Args:
            data: The data to be compressed.
            level: See https://docs.python.org/3/library/zlib.html#zlib.compress

        Returns:
            The compressed data.
        """
        pass

class ASCIIHexDecode:
    """
    The ASCIIHexDecode filter decodes data that has been encoded in ASCII
    hexadecimal form into a base-7 ASCII format.
    """

    @staticmethod
    def decode(data: Union[str, bytes], decode_parms: Optional[DictionaryObject]=None, **kwargs: Any) -> bytes:
        """
        Decode an ASCII-Hex encoded data stream.

        Args:
          data: a str sequence of hexadecimal-encoded values to be
            converted into a base-7 ASCII string
          decode_parms: a string conversion in base-7 ASCII, where each of its values
            v is such that 0 <= ord(v) <= 127.

        Returns:
          A string conversion in base-7 ASCII, where each of its values
          v is such that 0 <= ord(v) <= 127.

        Raises:
          PdfStreamError:
        """
        pass

class RunLengthDecode:
    """
    The RunLengthDecode filter decodes data that has been encoded in a
    simple byte-oriented format based on run length.
    The encoded data is a sequence of runs, where each run consists of
    a length byte followed by 1 to 128 bytes of data. If the length byte is
    in the range 0 to 127,
    the following length + 1 (1 to 128) bytes are copied literally during
    decompression.
    If length is in the range 129 to 255, the following single byte is to be
    copied 257 − length (2 to 128) times during decompression. A length value
    of 128 denotes EOD.
    """

    @staticmethod
    def decode(data: bytes, decode_parms: Optional[DictionaryObject]=None, **kwargs: Any) -> bytes:
        """
        Decode a run length encoded data stream.

        Args:
          data: a bytes sequence of length/data
          decode_parms: ignored.

        Returns:
          A bytes decompressed sequence.

        Raises:
          PdfStreamError:
        """
        pass

class LZWDecode:
    """
    Taken from:

    http://www.java2s.com/Open-Source/Java-Document/PDF/PDF-
    Renderer/com/sun/pdfview/decode/LZWDecode.java.htm
    """

    class Decoder:

        def __init__(self, data: bytes) -> None:
            self.STOP = 257
            self.CLEARDICT = 256
            self.data = data
            self.bytepos = 0
            self.bitpos = 0
            self.dict = [''] * 4096
            for i in range(256):
                self.dict[i] = chr(i)
            self.reset_dict()

        def decode(self) -> str:
            """
            TIFF 6.0 specification explains in sufficient details the steps to
            implement the LZW encode() and decode() algorithms.

            algorithm derived from:
            http://www.rasip.fer.hr/research/compress/algorithms/fund/lz/lzw.html
            and the PDFReference

            Raises:
              PdfReadError: If the stop code is missing
            """
            pass

    @staticmethod
    def decode(data: bytes, decode_parms: Optional[DictionaryObject]=None, **kwargs: Any) -> str:
        """
        Decode an LZW encoded data stream.

        Args:
          data: ``bytes`` or ``str`` text to decode.
          decode_parms: a dictionary of parameter values.

        Returns:
          decoded data.
        """
        pass

class ASCII85Decode:
    """Decodes string ASCII85-encoded data into a byte format."""

    @staticmethod
    def decode(data: Union[str, bytes], decode_parms: Optional[DictionaryObject]=None, **kwargs: Any) -> bytes:
        """
        Decode an Ascii85 encoded data stream.

        Args:
          data: ``bytes`` or ``str`` text to decode.
          decode_parms: a dictionary of parameter values.

        Returns:
          decoded data.
        """
        pass

class DCTDecode:
    pass

class JPXDecode:
    pass

class CCITParameters:
    """§7.4.6, optional parameters for the CCITTFaxDecode filter."""

    def __init__(self, K: int=0, columns: int=0, rows: int=0) -> None:
        self.K = K
        self.EndOfBlock = None
        self.EndOfLine = None
        self.EncodedByteAlign = None
        self.columns = columns
        self.rows = rows
        self.DamagedRowsBeforeError = None

class CCITTFaxDecode:
    """
    §7.4.6, CCITTFaxDecode filter (ISO 32000).

    Either Group 3 or Group 4 CCITT facsimile (fax) encoding.
    CCITT encoding is bit-oriented, not byte-oriented.

    §7.4.6, optional parameters for the CCITTFaxDecode filter.
    """

def decode_stream_data(stream: Any) -> Union[bytes, str]:
    """
    Decode the stream data based on the specified filters.

    This function decodes the stream data using the filters provided in the
    stream. It supports various filter types, including FlateDecode,
    ASCIIHexDecode, RunLengthDecode, LZWDecode, ASCII85Decode, DCTDecode, JPXDecode, and
    CCITTFaxDecode.

    Args:
        stream: The input stream object containing the data and filters.

    Returns:
        The decoded stream data.

    Raises:
        NotImplementedError: If an unsupported filter type is encountered.
    """
    pass

def decodeStreamData(stream: Any) -> Union[str, bytes]:
    """Deprecated. Use decode_stream_data."""
    pass

def _xobj_to_image(x_object_obj: Dict[str, Any]) -> Tuple[Optional[str], bytes, Any]:
    """
    Users need to have the pillow package installed.

    It's unclear if pypdf will keep this function here, hence it's private.
    It might get removed at any point.

    Args:
      x_object_obj:

    Returns:
        Tuple[file extension, bytes, PIL.Image.Image]
    """
    pass