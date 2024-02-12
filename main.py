from fastapi import FastAPI
from routes.route import router

# app = FastAPI()
app = FastAPI(trust_env=True)

app.include_router(router)

