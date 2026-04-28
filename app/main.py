from fastapi import FastAPI
from app.api.v1.router import api_router
from dotenv import load_dotenv
from app.core.logging import setup_logging
from app.core.middleware import register_middlewares

setup_logging()

app = FastAPI()

register_middlewares(app)

load_dotenv()

app.include_router(api_router, prefix="/api/v1")
