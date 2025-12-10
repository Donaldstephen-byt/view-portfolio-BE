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



# from turtle import Screen, tracer, color, circle, fd, rt, done
# from colorsys import hsv_to_rgb

# def generate_turtle_image():
#     screen = Screen()
#     screen.setup(width=800, height=600)
#     screen.bgcolor("black")
#     tracer(0)  # draw instantly
#     h = 0
#     for i in range(225):
#         r, g, b = hsv_to_rgb(h, 1, 1)
#         color(int(r*255), int(g*255), int(b*255))
#         h += 0.01
#         for j in range(4):
#             circle(30 + j + 4, -90)
#             fd(300)
#             rt(90)
#             circle(10)
#             rt(10)
#     screen.update()
#     # keep window open
#     done()

# generate_turtle_image()