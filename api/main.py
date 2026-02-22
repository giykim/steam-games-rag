import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.chat_router import ChatRouter


class App:
    def __init__(self):
        self.app = FastAPI(title="Steam Game Recommender")
        self._register_cors()
        self._register_routers()
        self._register_health()

    def _register_cors(self):
        origins = ["http://localhost:3000"]
        frontend_url = os.getenv("FRONTEND_URL")
        if frontend_url:
            origins.append(frontend_url)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routers(self):
        chat_router = ChatRouter()
        self.app.include_router(chat_router.router, prefix="/api")

    def _register_health(self):
        self.app.add_api_route("/health", self._health)

    def _health(self):
        return {"status": "ok"}


app = App().app
