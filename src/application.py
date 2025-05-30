from dataclasses import dataclass
from typing import Self
from uuid import UUID

from src.domain import Book, BookId, BookRepository


@dataclass
class BookDTO:
    id: str
    title: str
    author: str

    @classmethod
    def from_domain(cls, book: Book) -> Self:
        return cls(id=str(book.id.value), title=book.title, author=book.author)


class BookService:
    def __init__(self, book_repository: BookRepository):
        self._book_repository = book_repository

    async def add_book(self, title: str, author: str) -> BookDTO:
        book = Book.create(title=title, author=author)

        await self._book_repository.save(book=book)

        return BookDTO.from_domain(book=book)

    async def get_book(self, book_id: str) -> BookDTO | None:
        domain_id = BookId(UUID(book_id))

        book = await self._book_repository.get_by_id(book_id=domain_id)
        if not book:
            return None

        return BookDTO.from_domain(book=book)

    async def remove_book(self, book_id: str) -> None:
        domain_id = BookId(UUID(book_id))

        book = await self._book_repository.get_by_id(book_id=domain_id)
        if not book:
            return None

        await self._book_repository.delete(book=book)
