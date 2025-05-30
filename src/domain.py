from dataclasses import dataclass
from typing import Protocol, Self
from uuid import UUID, uuid4


@dataclass
class BookId:
    value: UUID

    def __hash__(self) -> int:
        return hash(str(self.value))


@dataclass
class Book:
    id: BookId
    title: str
    author: str

    @classmethod
    def create(cls, title: str, author: str) -> Self:
        return cls(id=BookId(uuid4()), title=title, author=author)


class BookRepository(Protocol):
    async def save(self, book: Book) -> None: ...

    async def get_by_id(self, book_id: BookId) -> Book | None: ...

    async def delete(self, book: Book) -> None: ...
