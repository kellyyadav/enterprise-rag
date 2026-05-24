# rag/ingestion.py
import json, csv, os
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

EMBED_MODEL = "all-MiniLM-L6-v2"   # free, local
CHROMA_DIR  = "./chroma_db"

def load_text_documents(folder="data/documents"):
    docs = []
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        with open(fpath) as f:
            text = f.read()
        # infer department from first line
        dept = text.split("\n")[0].replace("DEPARTMENT:","").strip().lower()
        docs.append(Document(
            page_content=text,
            metadata={"source": fname, "department": dept, "type": "document"}
        ))
    return docs

def load_json_logs(path="data/logs/audit_logs.json"):
    with open(path) as f:
        logs = json.load(f)
    docs = []
    for log in logs:
        content = (f"[{log['timestamp']}] Event: {log['event']} | "
                   f"User: {log['user_id']} ({log['user_role']}) | "
                   f"Resource: {log['resource']} | Status: {log['status']}")
        docs.append(Document(
            page_content=content,
            metadata={"source": "audit_logs.json", "department": "ops",
                      "type": "log", "event": log["event"]}
        ))
    return docs

def load_csv(path="data/structured/employees.csv"):
    docs = []
    with open(path) as f:
        rows = list(csv.DictReader(f))
    # embed each row + a summary
    summary = "Employee records: " + "; ".join(
        f"{r['name']} ({r['dept']}, salary ${r['salary']}, perf {r['performance']})"
        for r in rows
    )
    docs.append(Document(
        page_content=summary,
        metadata={"source": "employees.csv", "department": "hr", "type": "csv"}
    ))
    return docs

def build_vectorstore():
    print("Loading documents...")
    all_docs = (
        load_text_documents() +
        load_json_logs() +
        load_csv()
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks   = splitter.split_documents(all_docs)
    print(f"  {len(chunks)} chunks from {len(all_docs)} source documents")

    print("Building vector store...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_DIR
    )
    vectorstore.persist()
    print(f"✅ Vector store saved to {CHROMA_DIR}")
    return vectorstore

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
