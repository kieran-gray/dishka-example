from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from pydantic import BaseModel

from src.application import BookDTO, BookService


class AddBookRequest(BaseModel):
    title: str
    author: str


router = APIRouter(prefix="/book")


@router.post("/", response_model=BookDTO, status_code=status.HTTP_201_CREATED)
@inject
async def add_book(
    request_data: AddBookRequest,
    book_service: Annotated[BookService, FromComponent("")],
) -> BookDTO:
    return await book_service.add_book(title=request_data.title, author=request_data.author)


@router.get("/{book_id}", response_model=BookDTO | None, status_code=status.HTTP_200_OK)
@inject
async def get_book(
    book_id: str, book_service: Annotated[BookService, FromComponent("")]
) -> BookDTO | None:
    return await book_service.get_book(book_id=book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_book(
    book_id: str, book_service: Annotated[BookService, FromComponent("")]
) -> None:
    return await book_service.remove_book(book_id=book_id)
