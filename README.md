# food-recipe-llm-api

A production-ready REST API that generates food recipes using a fine-tuned GPT-2 language model. Give it a short prompt like `"Chicken Biryani"` and it returns a full recipe with ingredients and instructions.

## How it works

```
User sends prompt → FastAPI → Fine-tuned GPT-2 → Generated Recipe
```

The GPT-2 model was fine-tuned on an Indian recipes dataset using Hugging Face Transformers. The API is built with FastAPI and designed for cloud deployment on AWS ECS Fargate.

## Tech Stack

| Layer | Technology |
|---|---|
| Language Model | GPT-2 (fine-tuned) |
| API Framework | FastAPI |
| ML Framework | Hugging Face Transformers |
| Validation | Pydantic |
| Deployment | Docker + AWS ECS Fargate |
| CI/CD | GitHub Actions |

## Project Structure

```
food-recipe-llm-api/
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── routes/          # API endpoints
│   │   └── schemas/         # Request/response models
│   ├── model/
│   │   └── inference.py     # Model loading and generation
│   └── utils/
├── tests/
├── training/                # GPT-2 fine-tuning notebook
├── Dockerfile
├── .env.example
└── requirements.txt
```

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/johnpaul-raphael/food-recipe-llm-api.git
cd food-recipe-llm-api
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**
```bash
copy .env.example .env       # Windows
cp .env.example .env         # Mac/Linux
```

Edit `.env`:
```
MODEL_PATH=./recipe-gpt2-final
MAX_NEW_TOKENS=300
TEMPERATURE=0.7
```

**5. Run the API**
```bash
uvicorn src.api.main:app --reload
```

## API Endpoints

### Generate Recipe
```
POST /api/generate
```

Request:
```json
{
  "prompt": "Chicken Biryani"
}
```

Response:
```json
{
  "prompt": "Chicken Biryani",
  "generated_recipe": "Recipe: Chicken Biryani\nIngredients: ..."
}
```

### Health Check
```
GET /api/health
```
Response:
```json
{"status": "ok"}
```

### Interactive API Docs
```
http://localhost:8000/docs
```

## Model Training

The GPT-2 model was fine-tuned on an Indian recipes dataset with the following setup:

- Base model: `gpt2` (117M parameters)
- Dataset: 5,000 recipes
- Epochs: 3
- Max token length: 512
- Final validation loss: 1.684

Training notebook is available in the `training/` folder.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `./recipe-gpt2-final` | Path to fine-tuned model |
| `MAX_NEW_TOKENS` | `300` | Max tokens to generate |
| `TEMPERATURE` | `0.7` | Generation creativity (0.1–1.0) |

## License

MIT License — free to use, modify, and distribute.
