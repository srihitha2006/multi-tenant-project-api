from fastapi import Depends
from app.dependencies.auth import require_role

# Any logged-in user (Admin/Manager/Member)
def get_current_user():
    return require_role(["Admin", "Manager", "Member"])
