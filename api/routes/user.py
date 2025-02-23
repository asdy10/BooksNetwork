from typing import Annotated

from fastapi import Depends, APIRouter, Query, Body

from ..schemas.user import UserCreate, UserApi

user_router = APIRouter()


@user_router.post("/add")
async def user_add(user: Annotated[
    UserCreate,
    Body(..., example={
        'name': 'Alex',
        'email': 'user@example.com',
        'password': '123456',
    })
]) -> Annotated[
    UserApi,
    Body(..., example={
        'name': 'Alex',
        'email': 'user@example.com',
        'id': 'asdf'}
         )]:
    print(user)
    new_user = UserApi(id='asdf', name='alex', email='user@example.com')
    return new_user


@user_router.get("/get")
async def user_get(user_id: Annotated[str, Query(..., title="User ID")]):
    print('user_get', user_id)
