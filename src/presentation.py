from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status
from pydantic import BaseModel, ValidationError

from src.application import BookDTO, BookService, InvalidBookId, BookNotFoundById
from src.domain import CannotCheckoutBook


EXCEPTION_MAPPING: dict[type[Exception], int] = {
    ValidationError: status.HTTP_400_BAD_REQUEST,
    InvalidBookId: status.HTTP_400_BAD_REQUEST,
    BookNotFoundById: status.HTTP_404_NOT_FOUND,
    CannotCheckoutBook: status.HTTP_400_BAD_REQUEST,
}


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


@router.get("/{book_id}", response_model=BookDTO, status_code=status.HTTP_200_OK)
@inject
async def get_book(
    book_id: str, book_service: Annotated[BookService, FromComponent("")]
) -> BookDTO:
    return await book_service.get_book(book_id=book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_book(
    book_id: str, book_service: Annotated[BookService, FromComponent("")]
) -> None:
    return await book_service.remove_book(book_id=book_id)


@router.put("/check-out/{book_id}", status_code=status.HTTP_200_OK)
@inject
async def check_out_book(
    book_id: str, book_service: Annotated[BookService, FromComponent("")]
) -> BookDTO:
    return await book_service.check_out_book(book_id=book_id)
