from uuid import uuid4
import pytest
import pytest_asyncio

from src.application import BookDTO, BookNotFoundById, BookService, InvalidBookId
from src.domain import Book, BookId, BookRepository, CannotCheckoutBook


class MockBookRepository:
    _data: dict[BookId, Book] = {}

    async def save(self, book: Book) -> None:
        self._data[book.id] = book

    async def get_by_id(self, book_id: BookId) -> Book | None:
        return self._data.get(book_id)

    async def delete(self, book: Book) -> None:
        self._data.pop(book.id, None)


@pytest_asyncio.fixture
async def book_repository() -> BookRepository:
    return MockBookRepository()


@pytest_asyncio.fixture
async def book_service(book_repository: BookRepository) -> BookService:
    return BookService(book_repository=book_repository)


def test_can_instantiate_book_dto() -> None:
    book = Book.create(title="The Magic Mountain", author="Thomas Mann")
    dto = BookDTO.from_domain(book)
    assert dto.author == book.author
    assert dto.title == book.title


async def test_can_add_book(book_service: BookService) -> None:
    book = await book_service.add_book(title="The Trial", author="Franz Kafka")
    assert isinstance(book, BookDTO)


async def test_can_get_book(book_service: BookService) -> None:
    book = await book_service.add_book(title="The Trial", author="Franz Kafka")
    get_book = await book_service.get_book(book_id=book.id)
    assert isinstance(get_book, BookDTO)


async def test_cannot_get_book_invalid_id(book_service: BookService) -> None:
    with pytest.raises(InvalidBookId):
        await book_service.get_book(book_id="invalid")


async def test_cannot_get_book_id_not_found(book_service: BookService) -> None:
    with pytest.raises(BookNotFoundById):
        await book_service.get_book(book_id=str(uuid4()))


async def test_can_remove_book(book_service: BookService) -> None:
    book = await book_service.add_book(title="The Trial", author="Franz Kafka")
    await book_service.remove_book(book_id=book.id)

    with pytest.raises(BookNotFoundById):
        await book_service.get_book(book_id=book.id)


async def test_can_check_out_book(book_service: BookService) -> None:
    book = await book_service.add_book(title="The Trial", author="Franz Kafka")
    checked_out_book = await book_service.check_out_book(book_id=book.id)
    assert isinstance(checked_out_book, BookDTO)


async def test_cannot_check_out_book_twice(book_service: BookService) -> None:
    book = await book_service.add_book(title="The Trial", author="Franz Kafka")
    checked_out_book = await book_service.check_out_book(book_id=book.id)
    assert isinstance(checked_out_book, BookDTO)

    with pytest.raises(CannotCheckoutBook):
        await book_service.check_out_book(book_id=book.id)
