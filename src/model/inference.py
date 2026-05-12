import os
import re
import boto3
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from src.utils.logger import get_logger
from typing import Dict, List

load_dotenv()

logger = get_logger(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "./recipe-gpt2-final")
MODEL_BUCKET = os.getenv("MODEL_BUCKET")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 300))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))


def download_model_from_s3():
    if not MODEL_BUCKET:
        logger.info("No S3 bucket configured — using local model path")
        return

    model_dir = Path(MODEL_PATH)
    if model_dir.exists() and any(model_dir.iterdir()):
        logger.info("Model already exists in /tmp — skipping download")
        return

    logger.info(f"Downloading model from s3://{MODEL_BUCKET} to {MODEL_PATH}")
    model_dir.mkdir(parents=True, exist_ok=True)
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=MODEL_BUCKET)

    for obj in response.get("Contents", []):
        key = obj["Key"]
        dest = model_dir / key
        logger.info(f"Downloading {key}...")
        s3.download_file(MODEL_BUCKET, key, str(dest))

    logger.info("Model downloaded successfully from S3")


class RecipeGenerator:

    def __init__(self):
        download_model_from_s3()
        logger.info(f"Loading model from: {MODEL_PATH}")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        logger.info("Tokenizer loaded successfully")
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
        logger.info("Model loaded successfully")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        logger.info("Pipeline created successfully")

    def generate_recipe(self, prompt: str) -> Dict:
        logger.info(f"Generating recipe for prompt: '{prompt}'")
        formatted_prompt = f"Recipe: {prompt}\nIngredients:"
        result = self.generator(
            formatted_prompt,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            pad_token_id=self.tokenizer.eos_token_id
        )
        generated_text = result[0]['generated_text']
        structured = self._parse_output(generated_text, prompt)
        logger.info(f"Recipe parsed — {len(structured['ingredients'])} ingredients, {len(structured['instructions'])} steps")
        return structured

    def _parse_output(self, text: str, prompt: str) -> Dict:
        logger.debug(f"Raw generated text:\n{text}")

        # truncate at endoftext
        if "<|endoftext|>" in text:
            text = text.split("<|endoftext|>")[0]

        # normalize all variations of Instructions marker using regex
        # handles: "Instructions:", "Instructions :", "InstructionsTo", "Instructions\n"
        text = re.sub(r'Instructions\s*:?\s*', 'Instructions: ', text, count=1)

        ingredients: List[str] = []
        instructions: List[str] = []

        has_ingredients = "Ingredients:" in text
        has_instructions = "Instructions:" in text

        # extract ingredients
        if has_ingredients:
            if has_instructions:
                ingredients_raw = text.split("Ingredients:")[1].split("Instructions:")[0]
            else:
                ingredients_raw = text.split("Ingredients:")[1]

            ingredients = [
                i.strip().strip(",;").strip()
                for i in re.split(r'[,\n]', ingredients_raw)
                if i.strip() and len(i.strip()) > 2
            ]
            # cap at 20 ingredients — model sometimes over-generates
            ingredients = ingredients[:20]

        # extract instructions — split by newline AND by "." followed by capital letter
        if has_instructions:
            instructions_raw = text.split("Instructions:")[1]
            raw_lines = instructions_raw.split("\n")
            seen = set()
            for line in raw_lines:
                line = line.strip()
                # split run-on sentences: "Step1.Step2" → ["Step1", "Step2"]
                sentences = re.split(r'\.(?=[A-Z])', line)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and sentence not in seen and len(sentence) > 10:
                        seen.add(sentence)
                        if not sentence.endswith('.'):
                            sentence += '.'
                        instructions.append(sentence)
            # cap at 15 steps
            instructions = instructions[:15]

        # fallback
        if not ingredients and not instructions:
            logger.warning(f"Could not parse recipe for prompt: '{prompt}'")
            return {
                "title": prompt.title(),
                "ingredients": [],
                "instructions": ["Sorry, I could not generate a clear recipe for this dish. Try a more common dish name."]
            }

        return {
            "title": prompt.title(),
            "ingredients": ingredients,
            "instructions": instructions
        }


if __name__ == "__main__":
    generator = RecipeGenerator()
    response = generator.generate_recipe("chicken biryani")
    print(response)
