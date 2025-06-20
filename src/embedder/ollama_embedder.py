from langchain_ollama import OllamaEmbeddings

class Embedder:
    def __init__(self, model_name="nomic-embed-text:latest", temperature=0.1):
        self.model = OllamaEmbeddings(model=model_name, temperature=temperature)

    def embed_text(self, text: str):
        return self.model.embed_documents([text])[0]

    def embed_query(self, query: str):
        return self.model.embed_query(query)