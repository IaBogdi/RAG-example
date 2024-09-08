from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import docx2txt
from pathlib import Path


class RAG():
    def __init__(self):
        self._retriever = None
        self._filename = None
        self._embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5"
        )
        self._llm = ChatOllama(
            model="llama3.1",
            temperature=0.1,
        )
        self._prompt_rag = ChatPromptTemplate.from_messages(
        [
        (
            "system",
            """Use the following pieces of retrieved context to answer "
            the question. If you don't know the answer, say that you
            don't know. Context:
            {context}
            
            Do not ask 'Would you like to know more' question."""
        ),
        ("human", "{input}"),
        ]
        )

    def _split_text_into_chunks(self,text, chunk_size=500, overlap=50):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len
        )
        return text_splitter.split_text(text)

    def _format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def GetAnswer(self, filename: str, question: str) -> str:
        if filename != self._filename:
            ext = Path(filename).suffix
            if ext == ".docx":
                text = docx2txt.process(filename)
            chunks = self._split_text_into_chunks(text)
            db = FAISS.from_texts(chunks,self._embeddings)
            self._retriever = db.as_retriever(search_kwargs={"k": 7})
            rag_chain = ({"context": self._retriever | self._format_docs, "input": RunnablePassthrough()} | self._prompt_rag | self._llm)
            return rag_chain.invoke(question).content
