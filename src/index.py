import subprocess
from fastapi import FastAPI, Query
from typing import Optional
import re
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/")
async def read_root(temp: float = 0.0, model: str = "gpt-4-turbo",urls: Annotated[list[str] | None, Query()] = None, text: str = "", question: str = "chi è il presidente della repubblica italiana?", google: Optional[bool] = False):
    
    command = ["python3", "main.py", "-t", str(temp), "-m", str(model), "--raw", str(text)]
    if google:
       command.append("--google")
    if urls:
        for url in urls:
            command.append("--url")
            command.append(url)
    command.append("--")
    command.append(question)


    result = subprocess.run(command, 
                            capture_output=True, text=True)
    
  
    
    stripped_output = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', result.stdout)
    print(result)
    answer_start = stripped_output.find(": ") + 2  
    answer_end = stripped_output.rfind("\n")  
    
    if answer_start!= -1 and answer_end!= -1:
        actual_answer = stripped_output[answer_start:answer_end].strip()
        print(actual_answer)
        return {"autor": "model", "text": actual_answer}
    else:
        print("No answer found.")
        return None
