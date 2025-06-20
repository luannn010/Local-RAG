from embedder import Embedder
from src.vectorstore import Qdrant
from src.runner import RAGRunner


if __name__ == "__main__":
    runner = RAGRunner("obsidiant")
    runner.chat()