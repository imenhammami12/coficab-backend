from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import user  # noqa: F401 (nécessaire pour créer la table)
from app.routers import auth, users, chatbot

# Crée les tables dans SQL Server si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coficab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ton app Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chatbot.router)

@app.get("/")
def root():
    return {"message": "Coficab API is running"}