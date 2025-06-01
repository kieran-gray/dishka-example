from dataclasses import dataclass
from typing import Any, Protocol, Self
from uuid import UUID, uuid4


# Exceptions


class CannotCheckoutBook(Exception):
    def __init__(self, book_id: Any):
        super().__init__(f"Cannot checkout Book {book_id=}")


# Value Objects


@dataclass
class BookId:
    value: UUID

    @classmethod
    def create(cls) -> Self:
        return cls(value=uuid4())

    def __hash__(self) -> int:
        return hash(str(self.value))


# Entities


@dataclass
class Book:
    id: BookId
    title: str
    author: str
    checked_out: bool

    @classmethod
    def create(cls, title: str, author: str) -> Self:
        return cls(id=BookId.create(), title=title, author=author, checked_out=False)

    def check_out(self) -> None:
        self.checked_out = True


# Repositories


class BookRepository(Protocol):
    async def save(self, book: Book) -> None: ...

    async def get_by_id(self, book_id: BookId) -> Book | None: ...

    async def delete(self, book: Book) -> None: ...


# Domain Services


class CheckOutBookService:
    def check_out(self, book: Book) -> Book:
        if book.checked_out:
            raise CannotCheckoutBook(book_id=book.id)

        book.check_out()

        return book
