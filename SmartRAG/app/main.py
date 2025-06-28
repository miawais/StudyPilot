from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as ask_router
from app.auth.routes_auth import router as auth_router

app = FastAPI(
    title="AI Tutor Chatbot",
    description="RAG-based AI tutor for 9th grade Computer Science",
    version="1.0.0"
)

# CORS setup (for frontend or external dashboard access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Mount routers (auth comes before chatbot for clarity)
app.include_router(auth_router)     
app.include_router(ask_router)      