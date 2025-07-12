import os
import uuid
import streamlit as st
from main import prepare_doc


def upload_file():
    directory = "./files"
    try:
        uploaded_file = st.file_uploader("Upload a new file", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                filename, ext = os.path.splitext(uploaded_file.name)

                # Check for duplicates (any file starting with the same base name)
                is_duplicate = any(
                    f.startswith(filename) for f in os.listdir(directory)
                )

                if is_duplicate:
                    st.warning(
                        f"A file named '{filename}' already exists. Please rename your file or upload a different one."
                    )
                else:
                    # Create new filename with short ID appended add the ID to the meta data useful for deletion
                    # and retrieval
                    original_id = create_short()
                    new_filename = f"{filename}_{original_id}{ext}"
                    file_path = os.path.join(directory, new_filename)

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                        store = prepare_doc(file_path, original_id)
                        print("STORE: ", store)
                        if store:
                            st.toast(
                                f"File prepared and saved as {uploaded_file.name}",
                                icon="😍",
                            )
                        else:
                            delete_file(directory, new_filename)
    except Exception as e:
        delete_file(directory, new_filename)
        st.error(f"Error uploading file: {e}")


def select_file(file_name):
    st.session_state["selected_file"] = file_name


# Extract the ID from the filename (e.g., JJRawlings_a9fce238.pdf -> a9fce238)
def extract_id_from_filename(filename):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    parts = name.rsplit("_", 1)
    return parts[1] if len(parts) == 2 else None


def create_short():
    short_id = uuid.uuid4().hex[:8]
    # print(f"Generated short ID: {short_id}")  # Debugging line
    return short_id


def list_files(directory):
    if os.path.exists(directory):
        files = os.listdir(directory)
        return [f for f in files if os.path.isfile(os.path.join(directory, f))]
    return []


def delete_file(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
