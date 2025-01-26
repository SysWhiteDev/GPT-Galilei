
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated

from main import main, load_dotenv

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

load_dotenv()


@app.post("/")
async def read_root(temp: float = 0.0, model: str = "gpt-3.5-turbo-1106",urls: Annotated[list[str] | None, Query()] = None, text: str = "", question: str = "chi è il presidente della repubblica italiana?", google: Optional[bool] = False):

    ## call the openai api
    answer = main(model       = model,
                  temperature = temp,
                  dry_mode    = False,
                  ctx_files   = [],
                  ctx_pfds    = [],
                  ctx_urls    = urls or [],
                  ctx_texts   = [text],
                  use_google  = bool(google),
                  questions   = [question])

    return {"autor": "model", # author ??
            "text":  answer}

