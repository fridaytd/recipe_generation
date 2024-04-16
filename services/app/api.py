from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
async def hello():
    return "Hello"

def make_app(*routers) -> FastAPI:
    app = FastAPI()
    for router in routers:
        app.include_router(router)
    return app