from pydantic import BaseModel

class TitleInput(BaseModel):
    url: str

class IngredientsInput(BaseModel):
    url: str
    title: str

class InstructionsInput(BaseModel):
    url: str
    title: str
    ingredients: str