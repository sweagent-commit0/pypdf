"""Helpers for working with PDF types."""
from abc import abstractmethod
from pathlib import Path
from typing import IO, Any, Dict, List, Optional, Tuple, Union
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol
from ._utils import StrByteType, StreamType

class PdfObjectProtocol(Protocol):
    indirect_reference: Any

class XmpInformationProtocol(PdfObjectProtocol):
    pass

class PdfCommonDocProtocol(Protocol):
    pass

class PdfReaderProtocol(PdfCommonDocProtocol, Protocol):
    pass

class PdfWriterProtocol(PdfCommonDocProtocol, Protocol):
    _objects: List[Any]
    _id_translated: Dict[int, Dict[int, int]]