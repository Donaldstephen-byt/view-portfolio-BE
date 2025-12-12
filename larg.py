# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Hello Donald, your backend is live!"}

# from turtle import *
# from colorsys import *
# setpos(40, 50)
# tracer(30)
# bgcolor('black')
# h = 0
# for i in range(225):
#     color(hsv_to_rgb(h, 1, 1))
#     h+=0.01
#     for j in range(4):
#         circle(30+j+4, -90)
#         fd(300)
#         rt(90)
#         circle(10)
#     rt(10)
# done()
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import FileResponse
from turtle import Screen, circle, fd, rt, color, tracer
from colorsys import hsv_to_rgb
from PIL import Image

def generate_turtle_image():
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black")
    tracer(30)
    h = 0
    for i in range(225):
        color(hsv_to_rgb(h, 1, 1))
        h += 0.01
        for j in range(4):
            circle(30 + j + 4, -90)
            fd(300)
            rt(90)
            circle(10)
            rt(10)
    screen.update()
    canvas = screen.getcanvas()
    canvas.postscript(file="output.ps", colormode="color")
    img = Image.open("output.ps")
    img.save("output.png")

# Generate image before starting FastAPI
generate_turtle_image()

app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL like ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, your FastAPI backend is live!"}

@app.get("/background")
def get_background_image():
    return FileResponse("output.png")
