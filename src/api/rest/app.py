from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.data.clients.postgress_client import init_async_engine, dispose_async_engine
from src.core.exception import handlers as exception_handlers
from src.api.rest.routes.project_routes import router as project_router
from src.api.middleware.cors import setup_cors
from src.api.rest.routes.task_routes import router as task_router
from src.api.rest.routes.sse_routes import router as sse_router
import src.data.models 
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_async_engine()
    yield
    await dispose_async_engine()

def get_app():
    app=FastAPI(lifespan=lifespan)
    setup_cors(app)
    app.include_router(project_router)
    app.include_router(task_router)
    app.include_router(sse_router)
    exception_handlers.register_exception_handlers(app)
    return app