from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as ask_router

app = FastAPI(
    title="AI Tutor Chatbot",
    description="RAG-based AI tutor for 9th grade Computer Science",
    version="1.0.0"
)

# CORS setup (for frontend/dashboard access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(ask_router, prefix="/api")
