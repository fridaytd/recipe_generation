from app.api import make_app, router
import uvicorn

my_app = make_app(router)

if __name__ == "__main__":
    uvicorn.run("main:my_app", reload=True)