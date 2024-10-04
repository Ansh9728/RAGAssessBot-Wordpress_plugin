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


def get_retriver_tool(docs):
    docs_chunks = get_document_chunks(docs)
    embedding_function = get_embedding_model()

    vector_db = Chroma.from_documents(docs_chunks, embedding_function)
    retriever = vector_db.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "retrieve_documents",
        "Efficiently search and return relevant documents based on the user's query, providing accurate and timely information to support decision-making."
    )

    tools = [retriever_tool]

    return tools




# def create_vector_index(document_chunks, embedding_model):
#     # Initialize the vector index using FAISS
#     vector_index = FAISS.from_documents(document_chunks, embedding_model)
#     return vector_index


# def save_vector_index(file_path, document_chunks, embedding_model):
#     try:
#         index_file = os.path.join(file_path, "index.faiss")
#         if not os.path.exists(index_file):
#             print(f"Vector index creating at location: {file_path}")
#             vector_index = create_vector_index(document_chunks, embedding_model)
#             vector_index.save_local(file_path)
#             print('Saved successfully')
#         else:
#             print(f"Loading Vector index Embedding from: {file_path}")
#             vector_index = FAISS.load_local(file_path, embedding_model, allow_dangerous_deserialization=True)

#         return vector_index

#     except Exception as e:
#         print('Exception occurred:', e)
#         return None


# # Store Content in Vectordb
# def store_posts_in_vectordb(docs):

#     embedding_model_name = "Snowflake/snowflake-arctic-embed-s"

#     directory = os.getenv("DATA_DIRECTORY", os.path.join(os.getcwd(), "Data_Folder"))
#     vector_index_path = os.path.join(directory,"faiss_index")
#     print("Vector Index Path", vector_index_path)

#     embedding_model = get_embedding_model(embedding_model_name)

#     # docs_embeddings = embedding_model.embed_query(docs[0].page_content)
#     document_chunks = create_document_chunks(docs)

#     vector_index = save_vector_index(vector_index_path, document_chunks, embedding_model)
#     print("Vector Index",vector_index)
    
#     return vector_index
