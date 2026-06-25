# src/lexiflow/middleware/logging_middleware.py
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Start timer
        start_time = time.perf_counter()

        # Log request
        logger.info(
            f"Request started | {request.method} {request.url.path} | id={request_id}"
        )

        try:
            response = await call_next(request)
        except Exception as e:
            # Log unhandled exceptions
            logger.error(
                f"Request failed | {request.method} {request.url.path} | id={request_id} | error={str(e)}"
            )
            raise

        # Calculate duration
        duration = (time.perf_counter() - start_time) * 1000  # ms

        # Log response
        logger.info(
            f"Request completed | {request.method} {request.url.path} | "
            f"status={response.status_code} | duration={duration:.2f}ms | id={request_id}"
        )

        response.headers["X-Request-ID"] = request_id
        return response