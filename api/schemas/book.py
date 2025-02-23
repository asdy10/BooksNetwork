from typing import Annotated

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: Annotated[str, Field(..., title='Название книги', min_length=3, max_length=100)]
    description: Annotated[str, Field(title='Описание книги', max_length=300)]


class BookCreate(BookBase):
    pass


class BookApi(BookBase):
    id: Annotated[str, Field(..., title='ID книги')]
