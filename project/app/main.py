from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from app.config import init_firebase
from app.routers import users, groups, products, catalog, chat
from app.realtime import sio


init_firebase()

app = FastAPI(
    title="Provisio API",
    description="Group shopping organization backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(groups.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(catalog.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Provisio API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path="/ws"
)
