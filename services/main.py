from app.api import make_app
import uvicorn

my_app = make_app()

if __name__ == "__main__":
    uvicorn.run("main:my_app", reload=True)