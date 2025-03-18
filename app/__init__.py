from fastapi import FastAPI
from apis.apis import router

app = FastAPI()

app.include_router(router)
