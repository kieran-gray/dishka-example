import uvloop

from src.application import BookDTO, BookService
from src.setup import create_dependency_injection_container


async def main() -> None:
    app_container = create_dependency_injection_container()

    async with app_container() as request_container:
        book_service = await request_container.get(BookService)
        book_1 = await book_service.add_book(title="Stoner", author="John Williams")
        book_2 = await book_service.add_book(title="Sometimes a Great Notion", author="Ken Kesey")

    async with app_container() as request_container:
        book_service = await request_container.get(BookService)
        book_1_get = await book_service.get_book(book_id=book_1.id)
        print(book_1_get)

    async with app_container() as request_container:
        book_service = await request_container.get(BookService)
        book_2_get = await book_service.get_book(book_id=book_2.id)
        assert isinstance(book_2_get, BookDTO)
        print(book_2_get)
        await book_service.remove_book(book_id=book_2_get.id)
        book_2_get = await book_service.get_book(book_id=book_2.id)
        print(book_2_get)

    await app_container.close()


if __name__ == "__main__":
    uvloop.run(main())
