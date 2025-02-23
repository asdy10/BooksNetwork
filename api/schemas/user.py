from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: Annotated[str, Field(..., title='Имя пользователя', min_length=3, max_length=100)]
    email: Annotated[str, Field(..., title='Email пользователя', min_length=6, max_length=100)]


class UserCreate(UserBase):
    password: Annotated[str, Field(..., title='Пароль пользователя', min_length=4, max_length=128)]


class UserApi(UserBase):
    id: Annotated[str, Field(..., title='ID пользователя')]
