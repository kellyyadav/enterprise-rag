# rag/pipeline.py
from rag.rbac       import RBACManager
from rag.retriever  import SecureRetriever
from rag.generator  import generate_answer
from rag.ingestion  import load_vectorstore, build_vectorstore
import os

class EnterpriseRAGPipeline:
    def __init__(self, rebuild=False):
        self.rbac = RBACManager()
        if rebuild or not os.path.exists("./chroma_db"):
            vs = build_vectorstore()
        else:
            vs = load_vectorstore()
        self.retriever = SecureRetriever(vs, self.rbac)

    def query(self, question: str, user_id: str) -> dict:
        user = self.rbac.get_user(user_id)
        if not user:
            return {"error": "Unknown user", "answer": "Unauthorized"}

        docs   = self.retriever.retrieve(question, user_id)
        result = generate_answer(question, docs, user_id)
        result["user_name"] = user["name"]
        result["user_role"] = user["role"]
        return result
