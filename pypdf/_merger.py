from io import BytesIO, FileIO, IOBase
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, Union, cast
from ._encryption import Encryption
from ._page import PageObject
from ._reader import PdfReader
from ._utils import StrByteType, deprecate_with_replacement, str_
from ._writer import PdfWriter
from .constants import GoToActionArguments, TypArguments, TypFitArguments
from .constants import PagesAttributes as PA
from .generic import PAGE_FIT, ArrayObject, Destination, DictionaryObject, Fit, FloatObject, IndirectObject, NameObject, NullObject, NumberObject, OutlineItem, TextStringObject, TreeObject
from .pagerange import PageRange, PageRangeSpec
from .types import LayoutType, OutlineType, PagemodeType
ERR_CLOSED_WRITER = 'close() was called and thus the writer cannot be used anymore'

class _MergedPage:
    """Collect necessary information on each page that is being merged."""

    def __init__(self, pagedata: PageObject, src: PdfReader, id: int) -> None:
        self.src = src
        self.pagedata = pagedata
        self.out_pagedata = None
        self.id = id

class PdfMerger:
    """
    Use :class:`PdfWriter` instead.

    .. deprecated:: 5.0.0
    """

    def __init__(self, strict: bool=False, fileobj: Union[Path, StrByteType]='') -> None:
        deprecate_with_replacement('PdfMerger', 'PdfWriter', '5.0.0')
        self.inputs: List[Tuple[Any, PdfReader]] = []
        self.pages: List[Any] = []
        self.output: Optional[PdfWriter] = PdfWriter()
        self.outline: OutlineType = []
        self.named_dests: List[Any] = []
        self.id_count = 0
        self.fileobj = fileobj
        self.strict = strict

    def __enter__(self) -> 'PdfMerger':
        deprecate_with_replacement('PdfMerger', 'PdfWriter', '5.0.0')
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], traceback: Optional[TracebackType]) -> None:
        """Write to the fileobj and close the merger."""
        if self.fileobj:
            self.write(self.fileobj)
        self.close()

    def merge(self, page_number: int, fileobj: Union[Path, StrByteType, PdfReader], outline_item: Optional[str]=None, pages: Optional[PageRangeSpec]=None, import_outline: bool=True) -> None:
        """
        Merge the pages from the given file into the output file at the
        specified page number.

        Args:
            page_number: The *page number* to insert this file. File will
                be inserted after the given number.
            fileobj: A File Object or an object that supports the standard
                read and seek methods similar to a File Object. Could also be a
                string representing a path to a PDF file.
            outline_item: Optionally, you may specify an outline item
                (previously referred to as a 'bookmark') to be applied at the
                beginning of the included file by supplying the text of the outline item.
            pages: can be a :class:`PageRange<pypdf.pagerange.PageRange>`
                or a ``(start, stop[, step])`` tuple
                to merge only the specified range of pages from the source
                document into the output document.
                Can also be a list of pages to merge.
           import_outline: You may prevent the source document's
                outline (collection of outline items, previously referred to as
                'bookmarks') from being imported by specifying this as ``False``.
        """
        pass

    def append(self, fileobj: Union[StrByteType, PdfReader, Path], outline_item: Optional[str]=None, pages: Union[None, PageRange, Tuple[int, int], Tuple[int, int, int], List[int]]=None, import_outline: bool=True) -> None:
        """
        Identical to the :meth:`merge()<merge>` method, but assumes you want to
        concatenate all pages onto the end of the file instead of specifying a
        position.

        Args:
            fileobj: A File Object or an object that supports the standard
                read and seek methods similar to a File Object. Could also be a
                string representing a path to a PDF file.
            outline_item: Optionally, you may specify an outline item
                (previously referred to as a 'bookmark') to be applied at the
                beginning of the included file by supplying the text of the outline item.
            pages: can be a :class:`PageRange<pypdf.pagerange.PageRange>`
                or a ``(start, stop[, step])`` tuple
                to merge only the specified range of pages from the source
                document into the output document.
                Can also be a list of pages to append.
            import_outline: You may prevent the source document's
                outline (collection of outline items, previously referred to as
                'bookmarks') from being imported by specifying this as ``False``.
        """
        pass

    def write(self, fileobj: Union[Path, StrByteType]) -> None:
        """
        Write all data that has been merged to the given output file.

        Args:
            fileobj: Output file. Can be a filename or any kind of
                file-like object.
        """
        pass

    def close(self) -> None:
        """Shut all file descriptors (input and output) and clear all memory usage."""
        pass

    def add_metadata(self, infos: Dict[str, Any]) -> None:
        """
        Add custom metadata to the output.

        Args:
            infos: a Python dictionary where each key is a field
                and each value is your new metadata.
                An example is ``{'/Title': 'My title'}``
        """
        pass

    def set_page_layout(self, layout: LayoutType) -> None:
        """
        Set the page layout.

        Args:
            layout: The page layout to be used

        .. list-table:: Valid ``layout`` arguments
           :widths: 50 200

           * - /NoLayout
             - Layout explicitly not specified
           * - /SinglePage
             - Show one page at a time
           * - /OneColumn
             - Show one column at a time
           * - /TwoColumnLeft
             - Show pages in two columns, odd-numbered pages on the left
           * - /TwoColumnRight
             - Show pages in two columns, odd-numbered pages on the right
           * - /TwoPageLeft
             - Show two pages at a time, odd-numbered pages on the left
           * - /TwoPageRight
             - Show two pages at a time, odd-numbered pages on the right
        """
        pass

    def set_page_mode(self, mode: PagemodeType) -> None:
        """
        Set the page mode.

        Args:
            mode: The page mode to use.

        .. list-table:: Valid ``mode`` arguments
           :widths: 50 200

           * - /UseNone
             - Do not show outline or thumbnails panels
           * - /UseOutlines
             - Show outline (aka bookmarks) panel
           * - /UseThumbs
             - Show page thumbnails panel
           * - /FullScreen
             - Fullscreen view
           * - /UseOC
             - Show Optional Content Group (OCG) panel
           * - /UseAttachments
             - Show attachments panel
        """
        pass

    @property
    def page_mode(self) -> Optional[PagemodeType]:
        """
        Set the page mode.

        Args:
            mode: The page mode to use.

        .. list-table:: Valid ``mode`` arguments
           :widths: 50 200

           * - /UseNone
             - Do not show outline or thumbnails panels
           * - /UseOutlines
             - Show outline (aka bookmarks) panel
           * - /UseThumbs
             - Show page thumbnails panel
           * - /FullScreen
             - Fullscreen view
           * - /UseOC
             - Show Optional Content Group (OCG) panel
           * - /UseAttachments
             - Show attachments panel
        """
        pass

    def _trim_dests(self, pdf: PdfReader, dests: Dict[str, Dict[str, Any]], pages: Union[Tuple[int, int], Tuple[int, int, int], List[int]]) -> List[Dict[str, Any]]:
        """
        Remove named destinations that are not a part of the specified page set.

        Args:
            pdf:
            dests:
            pages:
        """
        pass

    def _trim_outline(self, pdf: PdfReader, outline: OutlineType, pages: Union[Tuple[int, int], Tuple[int, int, int], List[int]]) -> OutlineType:
        """
        Remove outline item entries that are not a part of the specified page set.

        Args:
            pdf:
            outline:
            pages:

        Returns:
            An outline type
        """
        pass

    def add_outline_item(self, title: str, page_number: int, parent: Union[None, TreeObject, IndirectObject]=None, color: Optional[Tuple[float, float, float]]=None, bold: bool=False, italic: bool=False, fit: Fit=PAGE_FIT) -> IndirectObject:
        """
        Add an outline item (commonly referred to as a "Bookmark") to this PDF file.

        Args:
            title: Title to use for this outline item.
            page_number: Page number this outline item will point to.
            parent: A reference to a parent outline item to create nested
                outline items.
            color: Color of the outline item's font as a red, green, blue tuple
                from 0.0 to 1.0
            bold: Outline item font is bold
            italic: Outline item font is italic
            fit: The fit of the destination page.
        """
        pass

    def add_named_destination(self, title: str, page_number: int) -> None:
        """
        Add a destination to the output.

        Args:
            title: Title to use
            page_number: Page number this destination points at.
        """
        pass