import os

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler,
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer always in Italian:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Load and process the text
embedding = OpenAIEmbeddings()
persist_directory = "db"

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Ciao, prova a farmi una domanda riguardo il canton Ticino, proverò a risponderti."
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.text:
        await update.message.reply_text(f"Mi serve una domanda per risponderti.")
    response = qa.run(update.message.text)
    await update.message.reply_text(response)

print("Starting the bot...")
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters=filters.TEXT, callback=answer))
app.run_polling()
