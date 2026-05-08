from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.orchestrator import AgentOrchestrator
from app.schemas import GenerateRequest, GenerateResponse

app = FastAPI(title="AI Short Video Director Agent API", version="1.0.0")
orchestrator = AgentOrchestrator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_video(payload: GenerateRequest) -> GenerateResponse:
    return await orchestrator.generate(payload)
