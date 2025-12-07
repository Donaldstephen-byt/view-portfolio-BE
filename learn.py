from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os
DATA_FILE = "items.json"

app = FastAPI()
class Item(BaseModel):
    name: str

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f)

@app.post("/items")
def create_item(item: Item):
    items = load_items()
    items.append(item.dict())
    save_items(items)
    return {"message": "Item saved", "item": item}
