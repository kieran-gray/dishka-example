from collections.abc import Iterable
from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    from_context,
    make_async_container,
    provide,
)
from dishka.dependency_source.composite import CompositeDependencySource
from pydantic import BaseModel, Field

from src.application import BookService
from src.domain import BookRepository
from src.infrastructure import InMemoryBookRepository


class Settings(BaseModel):
    environment: str = Field(alias="ENVIRONMENT", default="dev")


class InfrastructureProvider(Provider):
    scope = Scope.APP

    settings: CompositeDependencySource = from_context(provides=Settings, scope=Scope.RUNTIME)

    @provide
    def get_book_repository(self, settings: Settings) -> BookRepository:
        if settings.environment == "dev":
            return InMemoryBookRepository()
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
