import yaml
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class NodeModel(BaseModel):
    id: str
    type: str
    # Catch-all for any other data fields passed from the frontend config panel
    model_config = {"extra": "allow"}

class EdgeModel(BaseModel):
    source: str
    target: str

class WorkflowModel(BaseModel):
    id: str
    nodes: List[NodeModel]
    edges: List[EdgeModel]
    api_keys: Dict[str, str] = {}

def parse_yaml_workflow(yaml_content: str) -> WorkflowModel:
    data = yaml.safe_load(yaml_content)
    workflow_data = data.get("workflow", {})
    
    # Restructure for Pydantic
    parsed = {
        "id": workflow_data.get("id", "default"),
        "nodes": data.get("nodes", []),
        "edges": data.get("edges", []),
        "api_keys": data.get("api_keys", {})
    }
    return WorkflowModel(**parsed)
