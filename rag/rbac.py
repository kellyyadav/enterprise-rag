# rag/rbac.py
import json

class RBACManager:
    def __init__(self, policy_path="data/access_policies/rbac.json"):
        with open(policy_path) as f:
            data = json.load(f)
        self.roles = data["roles"]          # role → [departments]
        self.users = {u["id"]: u for u in data["users"]}

    def get_user(self, user_id: str) -> dict:
        return self.users.get(user_id)

    def allowed_departments(self, user_id: str) -> list[str]:
        user = self.get_user(user_id)
        if not user:
            return []
        return self.roles.get(user["role"], [])

    def can_access(self, user_id: str, department: str) -> bool:
        return department in self.allowed_departments(user_id)
