# # store data in chroma vector Database
# import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document



# Embedding Model
def get_embedding_model(model_name):
    # model_name = "Snowflake/snowflake-arctic-embed-l"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    base_embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        # model_kwargs={'device': device},
        encode_kwargs=encode_kwargs
    )

    return base_embedding_model


def create_document_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_splitter.split_documents(documents)
    return docs


def get_documents(posts, site_url):
    documents = []
    for post in posts:
        doc = Document(
            page_content=post.get('content'),
            metadata={"source":site_url,"title": post.get('title')}
        )
        documents.append(doc)

    documents = create_document_chunks(documents)

    return documents



def store_posts_in_vectordb(docs):

    embedding_model_name = "Snowflake/snowflake-arctic-embed-s"
    embedding_model = get_embedding_model(embedding_model_name)

    docs_embeddings = embedding_model.embed_query(docs[0].page_content)

    return docs_embeddings
