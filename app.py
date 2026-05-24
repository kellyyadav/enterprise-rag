# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag.pipeline import EnterpriseRAGPipeline

app = FastAPI(title="Enterprise RAG API")
rag = EnterpriseRAGPipeline()

class QueryRequest(BaseModel):
    question: str
    user_id: str

@app.post("/query")
def query(req: QueryRequest):
    return rag.query(req.question, req.user_id)

@app.get("/users")
def list_users():
    return list(rag.rbac.users.values())

@app.get("/health")
def health():
    return {"status": "ok"}
