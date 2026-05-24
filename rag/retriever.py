# rag/retriever.py
from rag.rbac import RBACManager

class SecureRetriever:
    def __init__(self, vectorstore, rbac: RBACManager):
        self.vs   = vectorstore
        self.rbac = rbac

    def retrieve(self, query: str, user_id: str, k: int = 5) -> list:
        allowed = self.rbac.allowed_departments(user_id)
        if not allowed:
            return []

        # semantic search → then filter by RBAC
        candidates = self.vs.similarity_search(query, k=k*3)
        results = [
            doc for doc in candidates
            if doc.metadata.get("department") in allowed
        ][:k]

        print(f"  [{user_id}] allowed={allowed} | retrieved={len(results)} chunks")
        return results
