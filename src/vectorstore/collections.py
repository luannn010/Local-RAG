# qdrant/collections.py
from src.vectorstore.client import client as default_client
from qdrant_client.models import VectorParams, Distance


class Qdrant:
    def __init__(self, client=None):
        # Use the provided client or fall back to the default one
        self._client = client if client is not None else default_client

    def create_collection(self, collection_name, vector_size=100, distance=Distance.COSINE):
        if not self._client.collection_exists(collection_name):
            self._client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
        print(f"Collection '{collection_name}' is ready.")

    def delete_collection(self, collection_name):
        if self._client.collection_exists(collection_name):
            self._client.delete_collection(collection_name)
            print(f"Collection '{collection_name}' has been deleted.")
        else:
            print(f"Collection '{collection_name}' does not exist.")

    def list_collections(self):
        collections = self._client.get_collections().collections
        if collections:
            print("Collections:")
            for collection in collections:
                print(f"- {collection.name}")
        else:
            print("Collections list is empty.")

    def collection_exists(self, collection_name):
        exists = self._client.collection_exists(collection_name)
        print(f"Collection '{collection_name}' exists." if exists else f"Collection '{collection_name}' does not exist.")
        return exists

    def search(self, collection_name, query_vector, limit=5):
        if self._client.collection_exists(collection_name):
            results = self._client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return results
        else:
            print(f"Collection '{collection_name}' does not exist.")
            return []

    def search_with_filter(self, collection_name, query_vector, filter=None, limit=5):
        if self._client.collection_exists(collection_name):
            results = self._client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                query_filter=filter,
                limit=limit
            )
            return results
        else:
            print(f"Collection '{collection_name}' does not exist.")
            return []
# # # Example usage:
# if __name__ == "__main__":
#     manager = Qdrant()
#     manager.collection_exists("obsidiant")
#     manager.list_collections()
#     # Simple example: embed a query and search
#     from src.embedder import Embedder

#     embedder = Embedder()

#     query = "What is on note 20-11-2024?"
#     query_vector = embedder.embed_query(query)
#     results = manager.search("obsidiant", query_vector)
#     print("Search results:", results)