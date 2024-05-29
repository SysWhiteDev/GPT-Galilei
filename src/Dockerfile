
## base image
FROM python:alpine3.18 AS backend

WORKDIR /app

## copy and install the requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

## copy the source
COPY src .

## set the default run command
CMD [ "fastapi", "run", "index.py" ]
