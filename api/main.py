from fastapi import FastAPI
from api.routers.chat_router import ChatRouter


class App:
    def __init__(self):
        self.app = FastAPI(title="Steam Game Recommender")
        self._register_routers()
        self._register_health()

    def _register_routers(self):
        chat_router = ChatRouter()
        self.app.include_router(chat_router.router, prefix="/api")

    def _register_health(self):
        self.app.add_api_route("/health", self._health)

    def _health(self):
        return {"status": "ok"}


app = App().app
