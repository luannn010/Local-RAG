# from src.embedder import Embedder
# from src.vectorstore import Qdrant
from src.runner import RAGRunner


if __name__ == "__main__":
    runner = RAGRunner("obsidian")
    runner.chat()