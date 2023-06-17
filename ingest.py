import os

from langchain.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

if not os.environ.get("OPENAI_API_KEY"):
    raise "OPENAI_API_KEY not set"

# Load and process the text
# loader = UnstructuredMarkdownLoader(
#     "documents/tassa-militare-smpp-di-repubblica-e-cantone-ticino.md"
# )

loader = DirectoryLoader("documents")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=70)
texts = text_splitter.split_documents(documents)

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = "db"

embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
vectordb = Chroma.from_documents(
    documents=texts, embedding=embedding, persist_directory=persist_directory
)

vectordb.persist()
vectordb = None
