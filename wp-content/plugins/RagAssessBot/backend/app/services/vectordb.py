import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document
from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import Chroma

# Embedding Model
def get_embedding_model(model_name="Snowflake/snowflake-arctic-embed-s"):
    # model_name = "Snowflake/snowflake-arctic-embed-l"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    base_embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        # model_kwargs={'device': device},
        encode_kwargs=encode_kwargs
    )

    return base_embedding_model


# Create Document Chunks
def get_document_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_splitter.split_documents(documents)
    return docs

# convert the post content into the langchain Document Object
def get_documents(posts, site_url):
    documents = []
    for post in posts:
        doc = Document(
            page_content=post.get('content'),
            metadata={"source":site_url,"title": post.get('title')}
        )
        documents.append(doc)

    documents = get_document_chunks(documents)

    return documents


# def get_retriver_tool(docs):
#     # docs_chunks = get_document_chunks(docs)
#     # print(docs_chunks)
#     embedding_function = get_embedding_model()
#     print("final_doc for store in chroma db",docs)

#     vector_db = Chroma.from_documents(docs, embedding_function)
#     retriever = vector_db.as_retriever()

#     retriever_tool = create_retriever_tool(
#         retriever,
#         "retrieve_documents",
#         "Efficiently search and return relevant documents based on the user's query, providing accurate and timely information to support decision-making."
#     )

#     tools = [retriever_tool]

#     return tools

def get_retriver(docs):
    # docs_chunks = get_document_chunks(docs)
    # print(docs_chunks)
    embedding_function = get_embedding_model()
    print("final_doc for store in chroma db",docs)

    vector_db = Chroma.from_documents(docs, embedding_function)
    retriever = vector_db.as_retriever()

    return retriever
