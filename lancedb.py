# import lancedb

# # push to lancedb
# def push_to_lancedb(embeddings):
#     db = lancedb.connect("/lancedb")
#     # sample data which will be overwritten when ne dos are uploaded
#     table = db.create_table(
#         "resumes",
#         data=[
#             {
#                 "vector": embeddings.embed_query("Hello World"),
#                 "text": "Hello World",
#                 "id": "1",
#             }
#         ],
#         mode="overwrite",
#     )
#     return table


# def pull_from_lancedb(table, embeddings, docs):
#     docsearch = LanceDB.from_documents(
#         documents=docs, embedding=embeddings, connection=table
#     )
#     return docsearch


# def similar_docs_lancedb(query, table, embeddings, docs):
#     docsearch = pull_from_lancedb(table, embeddings, docs)
#     similar_docs = docsearch.similarity_search(query)
#     return similar_docs


# # Helps us get the summary of a document
# def get_summary(current_doc):
#     llm = OpenAI(temperature=0)
#     # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
#     chain = load_summarize_chain(llm, chain_type="map_reduce")
#     summary = chain.run([current_doc])
#     return summary
