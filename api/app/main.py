from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.kafka.check_health import check_kafka_health
from app.core.settings import APISettings
from app.database.check_health import check_database_health
from app.api.challenge_1.router import router as challenge_1_router


app = FastAPI(
    title=APISettings.API_NAME,
    version=APISettings.VERSION,
    redoc_url=f"{APISettings.PREFIX}/redoc",
    swagger_ui_oauth2_redirect_url=f"{APISettings.PREFIX}/docs/oauth2-redirect",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APISettings.ORIGINS,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(challenge_1_router, prefix=APISettings.PREFIX)


@app.get("/health")
def health():
    database_health, database_message = check_database_health()
    kafka_health, kafka_message = check_kafka_health()
    return {
        "database": {
            "status": "ok" if database_health else "error",
            "message": database_message,
        },
        "kafka": {
            "status": "ok" if kafka_health else "error",
            "message": kafka_message,
        },
        "general_status": "ok" if all([database_health, kafka_health]) else "error",
    }
