# ParlaTI

Chatbot based on Knowledge base from ti.ch.

## Setup

```
poetry shell
poetry install
```

## Crawl data

This will run scrapy and fetch the data, that will be converted and saved as Markdown.

```
python -m scrapy runspider crawler.py
```

## Generate embeddings

This ingest script will fetch all the documents in `documents` folder and compute the embeddings.
Embeddings will be store in ChromaDB and persisted in the `db` folder.

```
python ingest.py
```

## Test your data

Modify the file as you wish, just test your data with:

```
python query.py
```

## Run the bot

This will run your telegram bot. Be sure to have a valid telegram token.

```
python bot.py
```
