from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import streamlit as st

# from file_utils import extract_id_from_filename

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = st.session_state.get("vector_store")


# ADD DOCUMENTS TO VECTOR STORE ON INITIAL UPLOAD
def add_documents_to_store(texts):
    if vector_store is None:
        return
    vector_store.add_documents(documents=texts)
    return vector_store


def create_retriever():
    if vector_store is not None:
        retriever = vector_store.as_retriever(
            search_type="mmr", search_kwargs={"k": 2, "fetch_k": 5}
        )
        return retriever


def delete_docs_by_original_id(vector_store, filename):
    from file_utils import extract_id_from_filename

    original_doc_id = extract_id_from_filename(filename)

    data = vector_store.get(include=["metadatas"])  # don't include 'ids'

    print("original_doc_id:", original_doc_id)

    ids_to_delete = []
    for doc_id, metadata in zip(data["ids"], data["metadatas"]):
        if metadata.get("original_doc_id") == original_doc_id:
            ids_to_delete.append(doc_id)

    print("ids_to_delete:", ids_to_delete)

    if ids_to_delete:
        vector_store.delete(ids=ids_to_delete)
        print(
            f"Deleted {len(ids_to_delete)} chunks for original_doc_id: {original_doc_id}"
        )
        return True
    else:
        print("No chunks found for deletion.")
