import os
import re
from io import BytesIO, UnsupportedOperation
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union, cast
from ._doc_common import PdfDocCommon, convert_to_int
from ._encryption import Encryption, PasswordType
from ._page import PageObject
from ._utils import StrByteType, StreamType, b_, logger_warning, read_non_whitespace, read_previous_line, read_until_whitespace, skip_over_comment, skip_over_whitespace
from .constants import TrailerKeys as TK
from .errors import EmptyFileError, FileNotDecryptedError, PdfReadError, PdfStreamError, WrongPasswordError
from .generic import ArrayObject, ContentStream, DecodedStreamObject, DictionaryObject, EncodedStreamObject, IndirectObject, NameObject, NullObject, NumberObject, PdfObject, TextStringObject, read_object
from .xmp import XmpInformation

class PdfReader(PdfDocCommon):
    """
    Initialize a PdfReader object.

    This operation can take some time, as the PDF stream's cross-reference
    tables are read into memory.

    Args:
        stream: A File object or an object that supports the standard read
            and seek methods similar to a File object. Could also be a
            string representing a path to a PDF file.
        strict: Determines whether user should be warned of all
            problems and also causes some correctable problems to be fatal.
            Defaults to ``False``.
        password: Decrypt PDF file at initialization. If the
            password is None, the file will not be decrypted.
            Defaults to ``None``.
    """

    def __init__(self, stream: Union[StrByteType, Path], strict: bool=False, password: Union[None, str, bytes]=None) -> None:
        self.strict = strict
        self.flattened_pages: Optional[List[PageObject]] = None
        self.resolved_objects: Dict[Tuple[Any, Any], Optional[PdfObject]] = {}
        self.xref_index = 0
        self.xref: Dict[int, Dict[Any, Any]] = {}
        self.xref_free_entry: Dict[int, Dict[Any, Any]] = {}
        self.xref_objStm: Dict[int, Tuple[Any, Any]] = {}
        self.trailer = DictionaryObject()
        self._page_id2num: Optional[Dict[Any, Any]] = None
        if hasattr(stream, 'mode') and 'b' not in stream.mode:
            logger_warning('PdfReader stream/file object is not in binary mode. It may not be read correctly.', __name__)
        self._stream_opened = False
        if isinstance(stream, (str, Path)):
            with open(stream, 'rb') as fh:
                stream = BytesIO(fh.read())
            self._stream_opened = True
        self.read(stream)
        self.stream = stream
        self._override_encryption = False
        self._encryption: Optional[Encryption] = None
        if self.is_encrypted:
            self._override_encryption = True
            id_entry = self.trailer.get(TK.ID)
            id1_entry = id_entry[0].get_object().original_bytes if id_entry else b''
            encrypt_entry = cast(DictionaryObject, self.trailer[TK.ENCRYPT].get_object())
            self._encryption = Encryption.read(encrypt_entry, id1_entry)
            pwd = password if password is not None else b''
            if self._encryption.verify(pwd) == PasswordType.NOT_DECRYPTED and password is not None:
                raise WrongPasswordError('Wrong password')
            self._override_encryption = False
        elif password is not None:
            raise PdfReadError('Not encrypted file')

    def __enter__(self) -> 'PdfReader':
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        self.close()

    def close(self) -> None:
        """Close the stream if opened in __init__ and clear memory."""
        pass

    @property
    def root_object(self) -> DictionaryObject:
        """Provide access to "/Root". Standardized with PdfWriter."""
        pass

    @property
    def _info(self) -> Optional[DictionaryObject]:
        """
        Provide access to "/Info". Standardized with PdfWriter.

        Returns:
            /Info Dictionary; None if the entry does not exist
        """
        pass

    @property
    def _ID(self) -> Optional[ArrayObject]:
        """
        Provide access to "/ID". Standardized with PdfWriter.

        Returns:
            /ID array; None if the entry does not exist
        """
        pass

    def _repr_mimebundle_(self, include: Union[None, Iterable[str]]=None, exclude: Union[None, Iterable[str]]=None) -> Dict[str, Any]:
        """
        Integration into Jupyter Notebooks.

        This method returns a dictionary that maps a mime-type to its
        representation.

        See https://ipython.readthedocs.io/en/stable/config/integrating.html
        """
        pass

    @property
    def pdf_header(self) -> str:
        """
        The first 8 bytes of the file.

        This is typically something like ``'%PDF-1.6'`` and can be used to
        detect if the file is actually a PDF file and which version it is.
        """
        pass

    @property
    def xmp_metadata(self) -> Optional[XmpInformation]:
        """XMP (Extensible Metadata Platform) data."""
        pass

    def _get_page(self, page_number: int) -> PageObject:
        """
        Retrieve a page by number from this PDF file.

        Args:
            page_number: The page number to retrieve
                (pages begin at zero)

        Returns:
            A :class:`PageObject<pypdf._page.PageObject>` instance.
        """
        pass

    def _get_page_number_by_indirect(self, indirect_reference: Union[None, int, NullObject, IndirectObject]) -> Optional[int]:
        """
        Generate _page_id2num.

        Args:
            indirect_reference:

        Returns:
            The page number or None
        """
        pass

    def _basic_validation(self, stream: StreamType) -> None:
        """Ensure file is not empty. Read at most 5 bytes."""
        pass

    def _find_eof_marker(self, stream: StreamType) -> None:
        """
        Jump to the %%EOF marker.

        According to the specs, the %%EOF marker should be at the very end of
        the file. Hence for standard-compliant PDF documents this function will
        read only the last part (DEFAULT_BUFFER_SIZE).
        """
        pass

    def _find_startxref_pos(self, stream: StreamType) -> int:
        """
        Find startxref entry - the location of the xref table.

        Args:
            stream:

        Returns:
            The bytes offset
        """
        pass

    @staticmethod
    def _get_xref_issues(stream: StreamType, startxref: int) -> int:
        """
        Return an int which indicates an issue. 0 means there is no issue.

        Args:
            stream:
            startxref:

        Returns:
            0 means no issue, other values represent specific issues.
        """
        pass

    def decrypt(self, password: Union[str, bytes]) -> PasswordType:
        """
        When using an encrypted / secured PDF file with the PDF Standard
        encryption handler, this function will allow the file to be decrypted.
        It checks the given password against the document's user password and
        owner password, and then stores the resulting decryption key if either
        password is correct.

        It does not matter which password was matched. Both passwords provide
        the correct decryption key that will allow the document to be used with
        this library.

        Args:
            password: The password to match.

        Returns:
            An indicator if the document was decrypted and whether it was the
            owner password or the user password.
        """
        pass

    @property
    def is_encrypted(self) -> bool:
        """
        Read-only boolean property showing whether this PDF file is encrypted.

        Note that this property, if true, will remain true even after the
        :meth:`decrypt()<pypdf.PdfReader.decrypt>` method is called.
        """
        pass

    def add_form_topname(self, name: str) -> Optional[DictionaryObject]:
        """
        Add a top level form that groups all form fields below it.

        Args:
            name: text string of the "/T" Attribute of the created object

        Returns:
            The created object. ``None`` means no object was created.
        """
        pass

    def rename_form_topname(self, name: str) -> Optional[DictionaryObject]:
        """
        Rename top level form field that all form fields below it.

        Args:
            name: text string of the "/T" field of the created object

        Returns:
            The modified object. ``None`` means no object was modified.
        """
        pass