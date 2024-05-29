
import requests
import bs4
import json
from PyPDF2 import PdfReader
import concurrent.futures # TODO


def guess_and_load_context(ctx: str) -> str | None:
    raise NotImplementedError("not implemented yet!!")

def get_context_from_url(url: str) -> str | None:

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = bs4.BeautifulSoup(response.content, "html.parser")

    return "\n".join(soup.stripped_strings).replace("{", "{{").replace("}", "}}")

def get_context_from_pdf(file: str) -> str | None:
    reader = PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages)

def load_context(ctx: list[str] | dict[str, str]) -> str | None:

    if isinstance(ctx, str):
        return guess_and_load_context(ctx)

    if not isinstance(ctx, dict):
        raise Exception("Invalid type for context: %r" % type(ctx))

    if not "source" in ctx:
        raise Exception("missing `source' key")

    source = ctx["source"]

    match ctx.get("type"):
        case "web": # load from a web page
            return get_context_from_url(source)
        case "pdf": # load from a pdf
            return get_context_from_pdf(source)
        case "text": # as-is
            return source
        case default:
            raise Exception("Invalid context type: %r" % default)

def get_context_from_file(file: str) -> list[str | None]: # TODO: PARALLELIZE

    with open(file) as fp:
        contexts = json.load(fp)

    return [load_context(ctx) for ctx in contexts]

