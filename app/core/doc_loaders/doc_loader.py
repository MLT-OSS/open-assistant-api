from langchain.document_loaders import Blob
from langchain.document_loaders.parsers import BS4HTMLParser, PyMuPDFParser
from langchain.document_loaders.parsers.generic import MimeTypeBasedParser
from langchain.document_loaders.parsers.txt import TextParser

PARSER_HANDLERS = {
    "application/pdf": PyMuPDFParser(),
    "text/plain": TextParser(),
    "text/html": BS4HTMLParser(),
}

MIMETYPE_PARSER = MimeTypeBasedParser(
    handlers=PARSER_HANDLERS,
    fallback_parser=None,
)


def _get_mimetype(file_bytes: bytes) -> str:
    try:
        import magic
    except ImportError:
        raise ImportError(
            "magic package not found, please install it with `pip install python-magic` and `brew install libmagic`"
        )

    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file_bytes)
    return mime_type


def load(data: bytes) -> str:
    mimetype = _get_mimetype(data)
    blob = Blob.from_data(
        data=data,
        mime_type=mimetype,
    )

    parser = MIMETYPE_PARSER

    docs = []
    for document in parser.lazy_parse(blob):
        docs.append(document)

    return "\n\n".join([doc.page_content for doc in docs])
