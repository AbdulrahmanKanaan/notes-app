from fastapi import FastAPI
from config.settings import get_settings
from routers import notes, trusted_api, auth

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)
app.include_router(notes.router)
app.include_router(auth.router)
app.include_router(trusted_api.router)
