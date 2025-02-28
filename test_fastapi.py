import json
import random
from datetime import datetime

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(redirect_slashes=False)
dict_ = {}
for i in range(10000):
    data = {
        "id": i,
        "timestamp": datetime.now().isoformat(),
        "data": f"Sample data for record {i}",
        "status": "active" if i % 2 == 0 else "inactive"
    }
    dict_[f"key_{i}"] = json.dumps(data)


@app.get("/get")
async def get1(request: Request):
    key = f"key_{random.randint(0, 9999)}"
    data = dict_.get(key)
    print(data)
    return data


@app.get("/get_many")
async def get1(request: Request):
    key = f"key_{random.randint(0, 9999)}"
    data = dict_.get(key)
    return data

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Только для React-приложения
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Type"]
)



if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000)