from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_projects():
    return []

@router.post("/")
async def create_project():
    return {"id": 1, "name": "New Project"}

@router.get("/{project_id}")
async def get_project(project_id: int):
    return {"id": project_id, "name": "Project"}
