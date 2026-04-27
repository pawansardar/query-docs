from fastapi import FastAPI
from app.api.v1.router import api_router
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

app.include_router(api_router, prefix="/api/v1")
