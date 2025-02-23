import os
from datetime import datetime

from jose import jwt, JWTError

SECRET_KEY = os.environ.get("SECRET_KEY")


async def get_current_user(jwttoken: str):
    try:
        payload = jwt.decode(jwttoken, SECRET_KEY, algorithms=['HS256'])
    except JWTError:
        return None

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire))
    if (not expire) or (expire_time < datetime.now()):
        return None
    user_id = payload.get('id')
    if not user_id:
        return None
    user = DBUser.get(user_id)
    return user