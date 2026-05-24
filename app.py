import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Enterprise RAG API")

# Pipeline ko try-catch mein load karo
try:
    from rag.pipeline import EnterpriseRAGPipeline
    rag = EnterpriseRAGPipeline()
    pipeline_loaded = True
except Exception as e:
    pipeline_loaded = False
    pipeline_error = str(e)

class QueryRequest(BaseModel):
    question: str
    user_id: str

@app.get("/", response_class=HTMLResponse)
def home():
    status = "✅ Pipeline Ready" if pipeline_loaded else f"⚠️ Pipeline Error: {pipeline_error}"
    return f"""
    <html>
        <body style="font-family:Arial; padding:40px; background:#111; color:white;">
            <h1>🚀 Enterprise RAG System</h1>
            <p>Status: {status}</p>
            <h3>Endpoints:</h3>
            <ul>
                <li><a href="/docs" style="color:cyan">/docs</a> — Swagger UI</li>
                <li><a href="/health" style="color:cyan">/health</a></li>
                <li><a href="/users" style="color:cyan">/users</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {
        "status": "ok",
        "pipeline": pipeline_loaded
    }

@app.post("/query")
def query(req: QueryRequest):
    if not pipeline_loaded:
        return {"error": pipeline_error}
    return rag.query(req.question, req.user_id)

@app.get("/users")
def list_users():
    if not pipeline_loaded:
        return {"error": pipeline_error}
    return list(rag.rbac.users.values())
