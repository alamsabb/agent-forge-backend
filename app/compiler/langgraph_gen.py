from jinja2 import Environment, FileSystemLoader
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_langgraph(workflow) -> str:
    template = env.get_template("graph.py.j2")
    return template.render(nodes=workflow.nodes, edges=workflow.edges)

def generate_fastapi(workflow) -> str:
    template = env.get_template("main.py.j2")
    return template.render(workflow_id=workflow.id)

def generate_dockerfile(workflow) -> str:
    template = env.get_template("Dockerfile.j2")
    return template.render()

def generate_docker_compose(workflow) -> str:
    template = env.get_template("docker-compose.yml.j2")
    return template.render()

def generate_requirements(workflow) -> str:
    template = env.get_template("requirements.txt.j2")
    return template.render()
