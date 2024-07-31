# # store data in chroma vector Database
# import os
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# # class WeaviateServices:

# #     def __init__(self) -> None:
# #         self.client



# # device = (
# #     "cuda"
# #     if torch.cuda.is_available()
# #     else "mps"
# #     if torch.backends.mps.is_available()
# #     else "cpu"
# # )
# # print(f"Using {device} device")


# # Embedding Model
# # model_name = "Snowflake/snowflake-arctic-embed-l"
# model_name = "Snowflake/snowflake-arctic-embed-m"
# encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

# arctic_base_embedding_model = HuggingFaceEmbeddings(
#     model_name=model_name,
#     # model_kwargs={'device': device},
#     encode_kwargs=encode_kwargs
# )


# def create_vector_index(document_chunks, embedding_model):
#     # Initialize the vector index using FAISS
#     vector_index = FAISS.from_documents(document_chunks, embedding_model)
#     return vector_index


# def save_vector_index(file_path, document_chunks, embedding_model):
#     # Save the vector index to the specified file path
#     try:
#       if not os.path.exists(file_path):

#           print(f"Vector_index_creating at location : {file_path}")

#           vector_index = create_vector_index(document_chunks, embedding_model)

#           vector_index.save_local(file_path)
#           print('Saved Succusfully')

#       # Load the vector index from the saved file

#       print(f"Loading Vector_index Embedding Present")

#       new_vector_index = FAISS.load_local(file_path, embedding_model, allow_dangerous_deserialization=True)

#       return new_vector_index

#     except Exception as e:
#       print('Exception occured ',e)
#       # vector_index.save_local(file_path)


# def get_chunk_docs(documents):
#     text_splitter = RecursiveCharacterTextSplitter(
#         # Set a really small chunk size, just to show.
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len,
#         is_separator_regex=False,
#     )
#     docs = text_splitter.split_documents(documents)
#     return docs
     


# def store_posts_in_vectordb(posts):
#    pass
import os
print(os.getcwd())