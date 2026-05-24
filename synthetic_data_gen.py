# synthetic_data_gen.py
import json, csv, os, random
from datetime import datetime, timedelta

# ── RBAC config ──────────────────────────────────────────
ROLES = {
    "admin":     ["hr", "finance", "engineering", "legal", "ops"],
    "hr":        ["hr"],
    "finance":   ["finance"],
    "engineer":  ["engineering"],
    "auditor":   ["hr", "finance", "legal"],
}

USERS = [
    {"id": "u001", "name": "Alice",   "role": "admin"},
    {"id": "u002", "name": "Bob",     "role": "hr"},
    {"id": "u003", "name": "Charlie", "role": "finance"},
    {"id": "u004", "name": "Diana",   "role": "engineer"},
    {"id": "u005", "name": "Eve",     "role": "auditor"},
]

# ── Document content ──────────────────────────────────────
DOCS = [
    {
        "filename": "hr_policy_2024.txt",
        "department": "hr",
        "content": """HR POLICY DOCUMENT 2024
Leave Policy: Employees get 18 days paid leave annually.
Maternity leave: 26 weeks. Paternity leave: 2 weeks.
Performance reviews are held every 6 months.
Salary increments are based on performance ratings (1-5 scale).
Remote work policy: Up to 3 days/week with manager approval."""
    },
    {
        "filename": "finance_q1_report.txt",
        "department": "finance",
        "content": """Q1 2024 FINANCIAL REPORT
Total Revenue: $4.2M  |  Operating Costs: $2.8M  |  Net Profit: $1.4M
Department Budgets: Engineering $800K, Marketing $400K, HR $200K
Outstanding invoices: $320K from 3 enterprise clients.
Cash reserves: $2.1M. Runway: 18 months."""
    },
    {
        "filename": "engineering_architecture.txt",
        "department": "engineering",
        "content": """SYSTEM ARCHITECTURE v3.2
Backend: Python FastAPI microservices, PostgreSQL + Redis.
Frontend: React 18, TypeScript, TailwindCSS.
Infrastructure: AWS EKS, Terraform IaC, GitHub Actions CI/CD.
Current sprint: RAG pipeline integration (Sprint 24).
Known issues: Memory leak in worker-node-7, ticket ENG-4821."""
    },
    {
        "filename": "legal_compliance.txt",
        "department": "legal",
        "content": """COMPLIANCE & LEGAL SUMMARY
GDPR compliance: Certified. Last audit: March 2024.
Data retention policy: 7 years for financial, 3 years for operational.
Active contracts: 14 enterprise, 3 government.
NDA violations: 0 reported in 2024.
Pending litigation: None."""
    },
]

# ── JSON logs ─────────────────────────────────────────────
def make_logs(n=20):
    events = ["LOGIN","QUERY","ACCESS_DENIED","DATA_EXPORT","CONFIG_CHANGE"]
    logs = []
    base = datetime(2024, 1, 1)
    for i in range(n):
        user = random.choice(USERS)
        event = random.choice(events)
        logs.append({
            "timestamp": (base + timedelta(hours=i*3)).isoformat(),
            "event": event,
            "user_id": user["id"],
            "user_role": user["role"],
            "resource": random.choice(["hr_policy","finance_report","eng_docs","legal_docs"]),
            "status": "DENIED" if event == "ACCESS_DENIED" else "SUCCESS",
            "ip": f"192.168.1.{random.randint(1,50)}"
        })
    return logs

# ── CSV employee data ─────────────────────────────────────
def make_csv():
    rows = [
        ["emp_id","name","dept","salary","join_date","performance"],
        ["E001","Alice Chen","Engineering","95000","2021-03-15","4.8"],
        ["E002","Bob Kumar","HR","72000","2020-07-01","4.2"],
        ["E003","Carol Singh","Finance","88000","2019-11-20","4.5"],
        ["E004","David Lee","Engineering","102000","2022-01-10","4.9"],
        ["E005","Eva Martinez","Legal","91000","2020-05-14","4.3"],
    ]
    return rows

# ── Generate all files ────────────────────────────────────
def generate():
    os.makedirs("data/documents", exist_ok=True)
    os.makedirs("data/logs",      exist_ok=True)
    os.makedirs("data/structured",exist_ok=True)
    os.makedirs("data/access_policies", exist_ok=True)

    # Text docs
    for doc in DOCS:
        path = f"data/documents/{doc['filename']}"
        with open(path, "w") as f:
            f.write(f"DEPARTMENT: {doc['department'].upper()}\n\n")
            f.write(doc["content"])
        print(f"Created: {path}")

    # JSON logs
    with open("data/logs/audit_logs.json", "w") as f:
        json.dump(make_logs(), f, indent=2)
    print("Created: data/logs/audit_logs.json")

    # CSV employees
    with open("data/structured/employees.csv", "w", newline="") as f:
        csv.writer(f).writerows(make_csv())
    print("Created: data/structured/employees.csv")

    # RBAC policy
    with open("data/access_policies/rbac.json", "w") as f:
        json.dump({"roles": ROLES, "users": USERS}, f, indent=2)
    print("Created: data/access_policies/rbac.json")

if __name__ == "__main__":
    generate()
    print("\n✅ Synthetic enterprise dataset generated!")
