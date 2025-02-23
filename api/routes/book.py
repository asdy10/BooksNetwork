from typing import Annotated

from fastapi import APIRouter, Path

book_router = APIRouter()


@book_router.get("/get/{id}")
async def book_get(id: Annotated[str, Path(..., title="ID книги")]):
    print('book_get', id)