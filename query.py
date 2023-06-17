import random

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
Answer always in Italian:"""

# Load and process the text
embedding = OpenAIEmbeddings()
persist_directory = "db"

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
)

questions = [
    "A quanto ammonta la tassa militare?",
    "Quanto devo pagare per la tassa militare?",
    "A quanto ammonta la tassa militare?",
    "è obbligatoria la tassa militare?",
    "esiste una tassa militare in ticino?",
]

query = random.sample(questions, 1)[0]
print(qa.run(query))
