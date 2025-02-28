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
    data = []
    for i in range(1000):
        data.append({'id': 'a40ddc73-b923-4c02-9d4e-262802505cb1_2025-02-14', 'date': 'datetime.date(2025, 2, 14)', 'wbacc_id': 'a40ddc73-b923-4c02-9d4e-262802505cb1', 'orders': 1971, 'buyouts': 643, 'returns': 36, 'cancels': 972, 'fact_orders': 0, 'fact_cancels': 0, 'fact_returns': 0, 'fact_buyouts': 0, 'orders_sum': 6980751.0, 'buyouts_sum': 2005346.0, 'returns_sum': 127715.0, 'supply_quantity': 0, 'profit': 1086345.0, 'ost': {'quantity': 0, 'way_to': 0, 'way_from': 0, 'full': 0}, 'ms_transfer': 0, 'store_cost': 28090.0, 'delivery_cost': 0.0, 'supply_cost': 0.0, 'other_services_cost': 0.0, 'budget': 187076.0, 'penalty': 0.0, 'nalog': 87870.0, 'sebes_buyouts': 0.0, 'ff_cost': 0.0, 'budget_other': 0.0, 'nacenka_unit': 211.02, 'marzha_unit': 67.59, 'profit_unit': 1978.35, 'price_with_discount': 3390, 'views': 2201163, 'clicks': 39699, 'add_to_cart': 1914, 'adv_orders': 258, 'adv_orders_sum': 730065.0, 'ctr': 1.98, 'cpc': 4.08, 'cpo': 956.64, 'drr': 2.68, 'orders_per_day': 1742.0, 'buyouts_per_day': 0.0, 'oborot_orders': 0.0, 'oborot_buyouts': 0.0, 'oborot_buyouts_transfer': 0.0, 'oborot_sebes': 0.0, 'buyout_percent': 0.0}
)

    return {'data': data}

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
    uvicorn.run("test_fastapi:app", host="0.0.0.0", port=8000)