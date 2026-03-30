from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="SMART on FHIR Backend")

app.include_router(router)