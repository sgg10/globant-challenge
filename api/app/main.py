from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import APISettings

from app.api.general.router import router as general_router
from app.api.challenge_1.router import router as challenge_1_router
from app.api.challenge_2.router import router as challenge_2_router


app = FastAPI(
    title=APISettings.API_NAME,
    version=APISettings.VERSION,
    redoc_url=f"{APISettings.PREFIX}/redoc",
    swagger_ui_oauth2_redirect_url=f"{APISettings.PREFIX}/docs/oauth2-redirect",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=APISettings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router, prefix=APISettings.PREFIX)
app.include_router(challenge_1_router, prefix=APISettings.PREFIX)
app.include_router(challenge_2_router, prefix=APISettings.PREFIX)
