import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 300))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))


class RecipeGenerator:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        self.generator = pipeline("text-generation",
        model=self.model,
        tokenizer=self.tokenizer)

    def generate_recipe(self, prompt: str) -> str:
        """
        Generate a recipe based on the given prompt.
        """
        formated_prompt = f"Recipe: {prompt}\nIngredients: \nInstructions: \n"
        result = self.generator(formated_prompt, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE,
        do_sample=True, top_p=0.9, pad_token_id=self.tokenizer.eos_token_id)
        return result[0]['generated_text']

if __name__ == "__main__":
    generator = RecipeGenerator()
    response = generator.generate_recipe("chicken briyani")
    print(f"Generated Recipe: {response}")