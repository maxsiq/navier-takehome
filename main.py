from api.products import products_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(products_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
