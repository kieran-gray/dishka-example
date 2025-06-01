from dataclasses import dataclass
from typing import Any, Self
from uuid import UUID

from src.domain import Book, BookId, BookRepository, CheckOutBookService

# Exceptions


class InvalidBookId(Exception):
    def __init__(self, book_id: Any):
        super().__init__(f"Invalid Book ID: {book_id}")


class BookNotFoundById(Exception):
    def __init__(self, book_id: Any):
        super().__init__(f"Book not found by ID: {book_id}")


# DTOs


@dataclass
class BookDTO:
    id: str
    title: str
    author: str

    @classmethod
    def from_domain(cls, book: Book) -> Self:
        return cls(id=str(book.id.value), title=book.title, author=book.author)


# Application Services


class BookService:
    def __init__(self, book_repository: BookRepository):
        self._book_repository = book_repository

    async def _get_book(self, book_id: str) -> Book:
        try:
            domain_id = BookId(UUID(book_id))
        except ValueError:
            raise InvalidBookId(book_id=book_id)

        book = await self._book_repository.get_by_id(book_id=domain_id)
        if not book:
            raise BookNotFoundById(book_id=book_id)

        return book

    async def add_book(self, title: str, author: str) -> BookDTO:
        book = Book.create(title=title, author=author)

        await self._book_repository.save(book=book)

        return BookDTO.from_domain(book=book)

    async def get_book(self, book_id: str) -> BookDTO:
        book = await self._get_book(book_id=book_id)

        return BookDTO.from_domain(book=book)

    async def remove_book(self, book_id: str) -> None:
        book = await self._get_book(book_id=book_id)

        await self._book_repository.delete(book=book)

    async def check_out_book(self, book_id: str) -> BookDTO:
        book = await self._get_book(book_id=book_id)

        book = CheckOutBookService().check_out(book=book)

        await self._book_repository.save(book)

        return BookDTO.from_domain(book=book)
