import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routes import user as user_routes
from .core.db import ENGINE, ORM_BASE


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(ORM_BASE.metadata.create_all)
    yield
    await ENGINE.dispose()


app = FastAPI(
    lifespan=lifespan,
    openapi_url="/openapi.json",
    root_path="/api/server",
)

app.include_router(user_routes.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
