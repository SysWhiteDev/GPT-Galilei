
import os
from enum import Enum
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import argparse
import time
import sys

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

def ask(model: ContextModel, question: str, pretty: bool = False) -> None:
    print(f"\033[32;1m{question}\033[0m: ", end="", flush=True)

    response = model.ask(question)

    if not pretty:
        print(response)
        return

    for c in response:
        print(c, end="", flush=True)
        time.sleep(0.05)

    print()

parser = argparse.ArgumentParser("langchain-gpt")

parser.add_argument("questions", nargs="*", help="questions to ask")

parser.add_argument("-t", "--temperature", type=float, help="set the temperature value", default=0.0)
parser.add_argument("-m", "--model", help="set the model name", default="gpt-3.5-turbo")
parser.add_argument("--url", metavar="URL", action="append", help="use the informations found in this url to answer the questions", default=[])
parser.add_argument("--pdf", metavar="FILE", action="append", help="use the informations found in this pdf to answer the questions", default=[])
parser.add_argument("--raw", metavar="TEXT", action="append", help="use this informations to answer the questions", default=[])
parser.add_argument("--load", metavar="FILE", action="append", help="load the sources from a json file", default=[])
# parser.add_argument("--context", metavar="CTX", action="append", help="use this information to answer the questions", default=[])
parser.add_argument("--google", action="store_true", help="use the google search engine to search informations")
parser.add_argument("-d", "--dry-run", action="store_true", help="do not connect to ChatGPT and avoid using tokens")
# parser.add_argument("-i", "--interactive", action="store_true", help="run in interactive mode")

args = parser.parse_args()

load_dotenv()

KEY = os.getenv("API_KEY")

if KEY is None:
    raise Exception("API_KEY variable not found!")

base_model = ChatOpenAI(model       = args.model,
                        temperature = args.temperature,
                        api_key     = KEY) # type: ignore

model = ContextModel(base_model = base_model,
                     dry_mode   = args.dry_run)

for file in args.load:
    log(f"Loading context from file {file} ...")

    for ctx in get_context_from_file(file):

        if ctx:
            model.add_context(ctx)

for url in args.url:
#    log(f"Loading context from url {url} ...")

    if ctx := get_context_from_url(url):
        model.add_context(ctx)

for pdf in args.pdf:
    log(f"Loading context from pdf {pdf} ...")

    if ctx := get_context_from_pdf(pdf):
        model.add_context(ctx)

for text in args.raw:
    model.add_context(text)

if args.google:

    for question in args.questions:
        log(f"Searching '{question}' ...")

        query = model.ask_without_contexts(websearch.create_partial_query(question)).replace("site:google.com", "") # avoid google results

        log(f"Using query '{query}' ...")

        for url in websearch.search(query): # FIXME
            log(f"Loading context from url {url} ...")
            model.add_context(get_context_from_url(url) or "")

if not args.questions:
    while question := input("> "):
        ask(model, question, True)

    sys.exit(0)

for question in args.questions:
    ask(model, question)

# fixes = read_config("fixes.json")
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     for item in fixes:
#         # print("getting context")
#         executor.submit(lambda: model.add_context(item_to_context(item)))
