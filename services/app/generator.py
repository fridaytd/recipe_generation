import torch
from transformers import BlipForConditionalGeneration, BlipForQuestionAnswering, AutoProcessor
from PIL import Image

class TitleGenerator:
    model_id: str = "thdangtr/blip_recipe1m_title_v1"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained(self.model_id)

    def __enter__(self):
        self.model.to(self.device)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.model.to("cpu")
        torch.cuda.empty_cache()

    def generate(self, img: Image) -> str:
       
        inputs = self.processor(
            images=img,
            return_tensors="pt"
        )
        output = self.model.generate(**inputs.to(self.device), max_new_tokens=20)
        decoded = self.processor.decode(output.cpu().squeeze(), skip_special_tokens=True)
        return decoded
    

class IngredientsGenerator:
    model_id: str = "thdangtr/blip_recipe1m_ingredients_v2"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-capfilt-large")
        self.model = BlipForQuestionAnswering.from_pretrained(self.model_id)

    def __enter__(self):
        self.model.to(self.device)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.model.to("cpu")
        torch.cuda.empty_cache()

    def generate(self, img: Image, title: str) -> str:
        
        inputs = self.processor(
            images=img,
            text=title,
            return_tensors="pt"
        )
        output = self.model.generate(**inputs.to(self.device), max_new_tokens=256, penalty_alpha=0.4)
        decoded = self.processor.decode(output.cpu().squeeze(), skip_special_tokens=True)
        return decoded
    
class InstructionsGenerator:
    model_id: str = "thdangtr/blip_recipe1m_instructions_v2"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-capfilt-large")
        self.model = BlipForQuestionAnswering.from_pretrained(self.model_id)

    def __enter__(self):
        self.model.to(self.device)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.model.to("cpu")
        torch.cuda.empty_cache()

    def generate(self, img: Image, title: str, ingredients: str) -> str:
        text = f"""Title: {title}. Ingredients: {ingredients}"""
        inputs = self.processor(
            images=img,
            text=text,
            return_tensors="pt"
        )
        output = self.model.generate(**inputs.to(self.device), max_new_tokens=256, penalty_alpha=0.3)
        decoded = self.processor.decode(output.cpu().squeeze(), skip_special_tokens=True)
        return decoded