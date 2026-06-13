from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from app.compiler.parser import parse_yaml_workflow
from app.compiler.validator import validate_workflow, ValidationError
from app.compiler.langgraph_gen import generate_langgraph, generate_fastapi
from app.compiler.project_gen import export_project_zip

router = APIRouter()

class WorkflowRequest(BaseModel):
    yaml: str

@router.post("/save")
async def save_workflow(request: WorkflowRequest):
    # Stub for future DB integration
    return {"status": "success", "message": "Saved to cloud"}

@router.post("/validate")
async def validate_workflow_endpoint(request: WorkflowRequest):
    try:
        workflow = parse_yaml_workflow(request.yaml)
        validate_workflow(workflow)
        return {"valid": True}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

@router.post("/generate")
async def generate_workflow(request: WorkflowRequest):
    try:
        workflow = parse_yaml_workflow(request.yaml)
        graph_code = generate_langgraph(workflow)
        main_code = generate_fastapi(workflow)
        return {"status": "success", "graph_code": graph_code, "main_code": main_code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export")
async def export_workflow(request: WorkflowRequest):
    try:
        zip_bytes = export_project_zip(request.yaml)
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=agentforge-project.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
