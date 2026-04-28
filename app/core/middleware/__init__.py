from .logging_middleware import log_requests

def register_middlewares(app):
    app.middleware("http")(log_requests)
