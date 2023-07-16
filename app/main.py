from app.api.routes import get_routers
from app.core.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


class App:
    """"Entry point"""
    app = FastAPI(
        version=get_settings().PROJECT_VERSION,
        openapi_url="/api/v1/openapi.json"
    )

    def add_cors(self):
        origins = [
            "http://localhost",
            "http://localhost:8080",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    def start_application(self) -> FastAPI:
        get_routers(self.app)
        self.add_cors()
        return self.app


app = App().start_application()
