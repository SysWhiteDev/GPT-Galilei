
from enum import Enum
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import argparse
import time
import os

from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from get_context import get_context_from_url, get_context_from_pdf, get_context_from_file
import websearch


DEFAULT_PREAMBLE = "If necessary, use this context to response: "

class MessageAuthor(Enum):
    SYSTEM = "system"
    HUMAN  = "human"
    AI     = "ai"

class ContextModel:

    def __init__(self, base_model: ChatOpenAI, *, dry_mode: bool = False) -> None:
        self.model = base_model
        self.contexts: list[tuple[str, str]] = []
        self.dry_mode = dry_mode

    def add_context(
        self,
        context: str,
        preamble: str = DEFAULT_PREAMBLE,
        author: MessageAuthor = MessageAuthor.SYSTEM,
    ) -> None:
        self.contexts.append((author.value, preamble + context))

    def _invoke(self, contexts: list[tuple[str, str]]) -> str:

        if self.dry_mode:
            return "dummy response due to dry-run"

        ctx = ChatPromptTemplate.from_messages(contexts)
        chain = ctx | self.model | StrOutputParser()
        return chain.invoke({})

    def ask(self, question: str) -> str:
        return self._invoke(self.contexts + [(MessageAuthor.HUMAN.value, question)])

    def ask_without_contexts(self, question: str) -> str:
        return self._invoke([(MessageAuthor.HUMAN.value, question)])

def log(msg: str) -> None:
    print("\x1b[93m" + msg + "\033[0m")

def ask(model: ContextModel, question: str, pretty: bool = False) -> str:

    if pretty:
        print(f"\033[32;1m{question}\033[0m: ", end="", flush=True)

    response = model.ask(question)

    if not pretty:
        return response

    for c in response:
        print(c, end="", flush=True)
        time.sleep(0.01)

    print()

    return response

def main(api_key: str | None, model: str, temperature: float, dry_mode: bool,
         ctx_files: list[str], ctx_pfds: list[str], ctx_urls: list[str],
         ctx_texts: list[str], use_google: bool, questions: list[str]) -> str | None:

    base_model = ChatOpenAI(model       = model,
                            temperature = temperature,
                            api_key     = api_key) # type: ignore

    ctx_model = ContextModel(base_model = base_model,
                             dry_mode   = dry_mode)

    for file in ctx_files:
        log(f"Loading context from file {file} ...")

        for ctx in get_context_from_file(file):

            if ctx:
                ctx_model.add_context(ctx)

    for url in ctx_urls:
        log(f"Loading context from url {url} ...")

        if ctx := get_context_from_url(url):
            ctx_model.add_context(ctx)

    for pdf in ctx_pfds:
        log(f"Loading context from pdf {pdf} ...")

        if ctx := get_context_from_pdf(pdf):
            ctx_model.add_context(ctx)

    for text in ctx_texts:
        ctx_model.add_context(text)

    if use_google:

        for question in questions:
            log(f"Searching '{question}' ...")

            query = ctx_model.ask_without_contexts(websearch.create_partial_query(question)).replace("site:google.com", "") # avoid google results

            log(f"Using query '{query}' ...")

            for url in websearch.search(query):
                if (url):
                    log(f"Loading context from url {url} ...")
                    ctx_model.add_context(get_context_from_url(url) or "")

    if not questions:
        while question := input("> "):
            ask(ctx_model, question, True)

        return None

    try:
        return "\n\n".join(ask(ctx_model, question) for question in questions)
    except Exception as err:
        print(err)
        return None

if __name__ == "__main__":

    ## parse the command-line arguments
    parser = argparse.ArgumentParser("langchain-gpt")

    parser.add_argument("questions", nargs="*", help="questions to ask")
    parser.add_argument("-t", "--temperature", type=float, help="set the temperature value", default=0.0)
    parser.add_argument("-m", "--model", help="set the model name", default="gpt-3.5-turbo-1106")
    parser.add_argument("--url", metavar="URL", action="append", help="use the informations found in this url to answer the questions", default=[])
    parser.add_argument("--pdf", metavar="FILE", action="append", help="use the informations found in this pdf to answer the questions", default=[])
    parser.add_argument("--raw", metavar="TEXT", action="append", help="use this informations to answer the questions", default=[])
    parser.add_argument("--load", metavar="FILE", action="append", help="load the sources from a json file", default=[])
    parser.add_argument("--google", action="store_true", help="use the google search engine to search informations")
    parser.add_argument("-d", "--dry-run", action="store_true", help="do not connect to ChatGPT and avoid using tokens")

    args = parser.parse_args()

    ## load the .env file
    load_dotenv()

    ## execute the main program
    result = main(api_key     = os.getenv("API_KEY"),
                  model       = args.model,
                  temperature = args.temperature,
                  dry_mode    = args.dry_run,
                  ctx_files   = args.load,
                  ctx_pfds    = args.pdf,
                  ctx_urls    = args.url,
                  ctx_texts   = args.raw,
                  use_google  = args.google,
                  questions   = args.questions)

    ## print the answers, only when in non-interactive mode
    if args.questions:
        print(result)

