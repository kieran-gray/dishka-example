import pytest
from src.domain import Book, BookId, CannotCheckoutBook, CheckOutBookService


def test_can_instantiate_book() -> None:
    title = "The Magic Mountain"
    author = "Thomas Mann"

    constructor_book = Book.create(title=title, author=author)
    direct_book = Book(id=constructor_book.id, title=title, author=author, checked_out=False)

    assert constructor_book == direct_book


def test_can_instantiate_book_id() -> None:
    constructor_book_id = BookId.create()
    direct_book_id = BookId(value=constructor_book_id.value)

    assert constructor_book_id == direct_book_id


def test_can_hash_book_id() -> None:
    book_id = BookId.create()
    assert isinstance(book_id.__hash__(), int)


def test_can_check_out_book() -> None:
    book = Book.create(title="The Magic Mountain", author="Thomas Mann")

    assert not book.checked_out

    book = CheckOutBookService().check_out(book=book)

    assert book.checked_out


def test_cannot_check_out_book_twice() -> None:
    book = Book.create(title="The Magic Mountain", author="Thomas Mann")

    book = CheckOutBookService().check_out(book=book)
    assert book.checked_out

    with pytest.raises(CannotCheckoutBook):
        CheckOutBookService().check_out(book=book)
