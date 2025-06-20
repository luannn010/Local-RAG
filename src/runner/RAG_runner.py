# src/runner/rag_runner.py

from src.preprocessor.folder_loader import FolderLoader
from src.vectorstore.collections import Qdrant
from src.embedder import Embedder
from src.trigger import TriggerDetector
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from src.history.history_manager import HistoryManager
import os
import uuid

model = os.getenv("LLAMA_MODEL", "mistral:7b")  # Default to mistral:7b if not set

class RAGRunner:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.vectorstore = Qdrant()
        self.embedder = Embedder()
        self.llm = ChatOllama(model=model)
        self.session_id = str(uuid.uuid4())  # Unique session ID

    def chat(self):
        print("🧠 Chat with your knowledge base (type 'exit' to quit)")
        print(f"Using collection: '{self.collection_name}'")

        if not self.vectorstore.collection_exists(self.collection_name):
            print(f"❌ Collection '{self.collection_name}' does not exist.")
            return

        messages = [SystemMessage(content="You are a helpful assistant.")]
        HistoryManager.save_to_redis(self.session_id, "system", "You are a helpful assistant.")

        while True:
            try:
                query = input("\nYou: ")
                if query.lower() == "exit":
                    print("💾 Flushing chat to Postgres...")
                    HistoryManager.flush_to_postgres(self.session_id)
                    break

                if TriggerDetector.should_trigger(query):
                    query_vector = self.embedder.embed_query(query)
                    results = self.vectorstore.search(self.collection_name, query_vector)
                    context = "\n\n".join(
                        f"Source: {match.payload.get('source')}\nContent: {match.payload.get('content', '')}"
                        for match in results
                    )
                    messages.append(SystemMessage(content=f"Use the following context to answer the question.\n\n{context}"))
                    HistoryManager.save_to_redis(self.session_id, "system", context)

                messages.append(HumanMessage(content=query))
                HistoryManager.save_to_redis(self.session_id, "user", query)

                response = self.llm.invoke(messages)
                print("\n🤖 LLM Answer:")
                print(response.content)

                messages.append(response)
                HistoryManager.save_to_redis(self.session_id, "assistant", response.content)

            except Exception as e:
                print(f"❗ Error during chat: {e}")