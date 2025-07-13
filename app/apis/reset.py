from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ResetRequest(BaseModel):
    user_id: Optional[str] = None

@router.post("/")
def reset_memory(data: ResetRequest):
    if data.user_id:
        return {"message": f"Memory cleared for user {data.user_id}"}
    return {"message": "Global memory cleared"}
