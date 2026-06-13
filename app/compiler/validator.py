from app.compiler.parser import WorkflowModel

class ValidationError(Exception):
    pass

def validate_workflow(workflow: WorkflowModel):
    node_ids = {node.id for node in workflow.nodes}
    
    if not workflow.nodes:
        raise ValidationError("Workflow cannot be empty. Add some nodes.")

    # Validate Edges
    adjacency_list = {node.id: [] for node in workflow.nodes}
    for edge in workflow.edges:
        if edge.source not in node_ids:
            raise ValidationError(f"Edge source '{edge.source}' not found in nodes.")
        if edge.target not in node_ids:
            raise ValidationError(f"Edge target '{edge.target}' not found in nodes.")
        adjacency_list[edge.source].append(edge.target)

    # Cycle Detection (DFS)
    visited = set()
    rec_stack = set()
    
    def dfs(node_id):
        visited.add(node_id)
        rec_stack.add(node_id)
        for neighbor in adjacency_list[node_id]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                # Cycle detected
                # Check if the cycle contains a 'loop' node, otherwise fail
                cycle_nodes = [n for n in workflow.nodes if n.id in rec_stack]
                if not any(n.type == 'loop' for n in cycle_nodes):
                    raise ValidationError(f"Cycle detected involving node '{neighbor}'. Cycles are only allowed if a 'Loop' node is present in the path.")
                return False
        rec_stack.remove(node_id)
        return False

    for node_id in node_ids:
        if node_id not in visited:
            dfs(node_id)

    # Node-specific Config Validation
    for node in workflow.nodes:
        config = node.model_config
        
        if node.type in ['openai', 'anthropic', 'gemini']:
            if not config.get('model'):
                raise ValidationError(f"Node '{node.id}' ({node.type}) is missing required 'model' configuration.")
        
        if node.type in ['react_agent', 'tool_calling_agent']:
            if not config.get('agent_prompt'):
                raise ValidationError(f"Agent Node '{node.id}' is missing required 'agent_prompt'.")
                
        if node.type in ['prompt_template']:
            if not config.get('template'):
                raise ValidationError(f"Prompt Node '{node.id}' is missing required 'template'.")

    return True
