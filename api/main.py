from fastapi import FastAPI

# from db.base import database
# from routers import router

app = FastAPI()
# app.include_router(router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()