from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from rag.pipeline import EnterpriseRAGPipeline

app = FastAPI(title="Enterprise RAG API")
rag = EnterpriseRAGPipeline()

class QueryRequest(BaseModel):
    question: str
    user_id: str

# ✅ Root route add kiya
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family:Arial; padding:40px; background:#111; color:white;">
            <h1>🚀 Enterprise RAG System</h1>
            <p>API is running!</p>
            <h3>Available Endpoints:</h3>
            <ul>
                <li><a href="/docs" style="color:cyan">/docs</a> — Swagger UI</li>
                <li><a href="/health" style="color:cyan">/health</a> — Health Check</li>
                <li><a href="/users" style="color:cyan">/users</a> — List Users</li>
            </ul>
        </body>
    </html>
    """

@app.post("/query")
def query(req: QueryRequest):
    return rag.query(req.question, req.user_id)

@app.get("/users")
def list_users():
    return list(rag.rbac.users.values())

@app.get("/health")
def health():
    return {"status": "ok"}
