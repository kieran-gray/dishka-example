from typing import Iterator
from fastapi.testclient import TestClient
import pytest

from src.setup import create_app


@pytest.fixture(scope="session")
def test_client() -> Iterator[TestClient]:
    app = create_app()
    with TestClient(app) as client:
        yield client


async def test_can_add_book(test_client: TestClient) -> None:
    response = test_client.post("/book/", json={"title": "The Plague", "author": "Albert Camus"})
    assert response.status_code == 201


async def test_can_get_book(test_client: TestClient) -> None:
    response = test_client.post("/book/", json={"title": "The Plague", "author": "Albert Camus"})
    book = response.json()

    response = test_client.get(f"/book/{book['id']}")
    assert response.status_code == 200


async def test_cannot_get_book_invalid_id(test_client: TestClient) -> None:
    response = test_client.get("/book/invalid")
    assert response.status_code == 400


async def test_can_remove_book(test_client: TestClient) -> None:
    response = test_client.post("/book/", json={"title": "The Plague", "author": "Albert Camus"})
    book = response.json()

    response = test_client.delete(f"/book/{book['id']}")
    assert response.status_code == 204


async def test_can_check_out_book(test_client: TestClient) -> None:
    response = test_client.post("/book/", json={"title": "The Plague", "author": "Albert Camus"})
    book = response.json()

    response = test_client.put(f"/book/check-out/{book['id']}")
    assert response.status_code == 200
