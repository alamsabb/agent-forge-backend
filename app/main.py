from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.auth import google
from app.config import settings

app = FastAPI(title="AgentForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import projects, workflows

app.include_router(google.router, prefix="/auth/google", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(workflows.router, prefix="/workflow", tags=["workflows"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to AgentForge API"}
