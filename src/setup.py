from collections.abc import AsyncIterator, Iterable
from contextlib import asynccontextmanager
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import setup_dishka
from dishka.dependency_source.composite import CompositeDependencySource
from pydantic import BaseModel, Field

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.application import BookService
from src.domain import BookRepository
from src.infrastructure import InMemoryBookRepository
from src.presentation import EXCEPTION_MAPPING, router


class Settings(BaseModel):
    environment: str = Field(alias="ENVIRONMENT", default="dev")


class InfrastructureProvider(Provider):
    scope = Scope.APP

    settings: CompositeDependencySource = from_context(provides=Settings, scope=Scope.RUNTIME)

    @provide
    def get_book_repository(self) -> BookRepository:
        return InMemoryBookRepository()


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_book_service(self, book_repository: BookRepository) -> BookService:
        return BookService(book_repository=book_repository)


def get_providers() -> Iterable[Provider]:
    return (InfrastructureProvider(), ApplicationProvider())


def create_dependency_injection_container() -> AsyncContainer:
    settings = Settings()
    return make_async_container(*get_providers(), context={Settings: settings})


class ExceptionHandler:
    _EXCEPTION_MAPPING = EXCEPTION_MAPPING

    def __init__(self, app: FastAPI) -> None:
        self._app = app

    async def _handle(self, _: Request, exc: Exception) -> JSONResponse:
        print(f"Exception '{type(exc).__name__}' occurred: '{exc}'.")

        status_code = self._EXCEPTION_MAPPING.get(type(exc), 500)
        message = str(exc) if status_code < 500 else "Internal server error."

        return JSONResponse(status_code=status_code, content={"description": message})

    def setup_handlers(self) -> None:
        for exc_class in self._EXCEPTION_MAPPING:
            self._app.add_exception_handler(exc_class, self._handle)
        self._app.add_exception_handler(Exception, self._handle)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield None
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(title="Library Service", lifespan=lifespan)

    async_container = create_dependency_injection_container()
    setup_dishka(container=async_container, app=app)

    app.include_router(router=router)

    exception_handler = ExceptionHandler(app)
    exception_handler.setup_handlers()

    return app
