from fastapi import Request
import time
from app.core.logging import get_logger

logger = get_logger(__name__)

async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        "HTTP Request",
        extra = {
            "path": request.url.path,
            "method": request.method,
            "duration": round(duration, 3),
            "status_code": response.status_code
        }
        
    )

    return response
