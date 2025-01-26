# GPT+Galilei

Feel free to fork this repo, please star it tho!

## Index

- [Features](#features)
- [Usage](#usage)
- - [Frontend use](#frontend)
- - [CLI use](#cli)
- [Authors](#authors)

## Features

- Automatic Google Search
- Fetch context from urls
- Additional custom text context

## Usage

There are 2 main ways to use this project: [CLI](#cli) and [Frontend](#frontend)

### Frontend

Install dependencies:

```bash
pip install -r ./requirements.txt
cd ./galilei-pt
npm -ci install
```

Build and run the frontend:

```bash
npm run build && npm run start
```

or start it in dev mode (slower load times):

```bash
npm run dev
```

Now open a separate terminal in the project directory and run the following to start the REST server:

```bash
cd ./src
fastapi run index.py
```

### CLI

Fix allucinations using `fixes.json` file:

```bash
python3 src/main.py \
    --load fixes.json \
    "What is LangChain?"
```

Fix allucinations using one or more URLs:

```bash
python3 src/main.py \
    --url https://sites.uclouvain.be/SystInfo/usr/include/bits/ioctls.h.html \
    'Which linux IOCTL correspond to the number 0x8942?'
```

Fix allucinations using one or more PDFs:

```bash
python3 src/main.py \
    --pdf samples/WEA025664A.pdf \
    "What is a WEA025664A?"
```

Fix allucinations using one or more raw texts:

```bash
python3 src/main.py \
    --raw "Doday is the 24-01-2030" \
    "Che giorno è oggi?"
```

Fix allucinations using one or more FixFiles

```bash
python3 src/main.py \
    --load fixes.json \
    "Chi è Ilenia Fronza?"
```

Fix allucinations using the Google Search Engine

```bash
python3 src/main.py \
    --google \
    "Chi è Ilenia Fronza?"
```

Fix allucinations using a different model

```bash
python3 src/main.py \
    --url "http://www.bassano.eu/Lingua-Veneta-VOCABOLARIO-veneto-italiano.htm" \
    --model "gpt-4-turbo" \
    "Come si dice 'setaccio' in dialetto veneto?"
```

## Authors

- [SysWhiteDev](https://github.com/syswhitedev) | Frontend and Backend development
- [Tesohh](https://github.com/tesohh) | Fixes configs
- [Resonanceee](https://github.com/resonanceee) | General help
- [Mat12143](https://github.com/mat12143) | General help
- [LalloS](https://github.com/lallos) | Created the functions to request info to OpenAI
