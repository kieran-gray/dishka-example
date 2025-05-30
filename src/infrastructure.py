from src.domain import Book, BookId, BookRepository


class InMemoryBookRepository(BookRepository):
    _data: dict[BookId, Book] = {}

    async def save(self, book: Book) -> None:
        self._data[book.id] = book

    async def get_by_id(self, book_id: BookId) -> Book | None:
        return self._data.get(book_id)

    async def delete(self, book: Book) -> None:
        self._data.pop(book.id, None)
