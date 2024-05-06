from fastapi import FastAPI, APIRouter
from app.cuslog import create_logger
from app.generator import TitleGenerator, IngredientsGenerator, InstructionsGenerator
from app.model import TitleInput, IngredientsInput, InstructionsInput
import requests
from PIL import Image

logger = create_logger("app")

router = APIRouter(
    prefix="/generate",
    tags=["generate"]
)

@router.post("/title")
async def title(input: TitleInput):
    logger.info("Loading title generator...")
    title = ""
    with TitleGenerator() as title_generator:
        logger.info("Done")

        img_url = input.url

        img = Image.open(requests.get(img_url, stream=True).raw)
        title = title_generator.generate(img)

    return {
        "title": title
    }

@router.post("/ingredients")
async def ingredients(input: IngredientsInput):
    logger.info("Loading ingredients generator...")
    ingredients = ""
    with IngredientsGenerator() as ingredients_generator:
        logger.info("Done")

        img_url = input.url
        title = input.title

        img = Image.open(requests.get(img_url, stream=True).raw)
        ingredients = ingredients_generator.generate(img, title)

    return {
        "ingredients": ingredients
    }

@router.post("/instructions")
async def instructions(input: InstructionsInput):
    logger.info("Loading instructions generator...")
    instructions = ""
    with InstructionsGenerator() as instructions_generator:
        logger.info("Done")

        img_url = input.url
        title = input.title
        ingredients = input.ingredients

        img = Image.open(requests.get(img_url, stream=True).raw)
        instructions = instructions_generator.generate(img, title, ingredients)

    return {
        "instructions": instructions
    }


def make_app() -> FastAPI:

    app = FastAPI()
    app.include_router(router)
    return app