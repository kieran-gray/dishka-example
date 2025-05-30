from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.presentation import router
from src.setup import create_dependency_injection_container


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="Library Service", lifespan=lifespan)
    async_container = create_dependency_injection_container()
    setup_dishka(container=async_container, app=app)
    app.include_router(router=router)
    return app


app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="run_http:app", host="0.0.0.0", port=8000, loop="uvloop")
