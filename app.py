import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routes.user_auth_routes import router as user_auth_routers
from src.routes.route import router as employee_recog_router

app = FastAPI(description='Employee attandance using face recognition system', title='Face Recognition', version='1.0.0')

# Add route for APIs
app.include_router(employee_recog_router)
app.include_router(user_auth_routers)


@app.get("/")
async def index():
    return "User Auth Service is running."


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! Something went wrong..."},
    )
