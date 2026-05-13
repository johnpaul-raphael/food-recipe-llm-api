# food-recipe-llm-api

A production-ready AI recipe generator that fine-tunes GPT-2 to generate food recipes from a short prompt like `"Chicken Biryani"`. Returns a structured recipe with ingredients and step-by-step instructions. Built with FastAPI, containerized with Docker, and deployed on AWS Lambda with full CI/CD via GitHub Actions.

## Live Demo

```
https://l1iw2m0y3e.execute-api.us-east-1.amazonaws.com/
```

## How it works

```
User types dish name
        ↓
FastAPI receives request
        ↓
Fine-tuned GPT-2 generates recipe text
        ↓
Parser extracts ingredients + instructions
        ↓
Structured JSON returned to UI
```

The GPT-2 model was fine-tuned on an Indian recipes dataset using Hugging Face Transformers. Model artifact is stored in AWS S3 and downloaded to Lambda on cold start.

## Tech Stack

| Layer | Technology |
|---|---|
| Language Model | GPT-2 (fine-tuned, 117M params) |
| API Framework | FastAPI + Mangum |
| ML Framework | Hugging Face Transformers |
| Validation | Pydantic |
| Containerization | Docker |
| Container Registry | AWS ECR |
| Deployment | AWS Lambda (container image) |
| API Gateway | AWS API Gateway HTTP API |
| Model Storage | AWS S3 |
| Infrastructure | AWS SAM + CloudFormation |
| CI/CD | GitHub Actions |
| Monitoring | AWS CloudWatch |

## Architecture

```
GitHub Actions (CI/CD)
        ↓ push image
AWS ECR (container registry)
        ↓ deploy
AWS Lambda (runs FastAPI container)
        ↑ loads model from
AWS S3 (model artifact storage)
        ↑ triggered by
AWS API Gateway (public HTTPS endpoint)
        ↑ logs to
AWS CloudWatch (monitoring)
```

## Project Structure

```
food-recipe-llm-api/
├── .github/
│   └── workflows/
│       ├── ci.yml           # runs tests on every PR
│       └── cd.yml           # deploys on merge to master
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI entry point + Mangum handler
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Pydantic request/response models
│   │   └── static/          # UI (index.html)
│   ├── model/
│   │   └── inference.py     # S3 download + model loading + generation
│   └── utils/
│       └── logger.py        # centralized logger
├── tests/
├── training/                # GPT-2 fine-tuning notebook
├── template.yaml            # SAM infrastructure as code
├── Dockerfile               # Lambda container image
├── .env.example
└── requirements.txt
```

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/johnpaul-raphael/food-recipe-llm-api.git
cd food-recipe-llm-api
```

**2. Fine-tune the GPT-2 model**

The training notebook is included in the repo. Run it on Google Colab (recommended — free GPU):

```
training/recipe_generator_gpt2_finetune.ipynb
```

Steps inside the notebook:
- Loads Indian recipes dataset from HuggingFace
- Fine-tunes GPT-2 on 5,000 recipes
- Saves the model artifact to `recipe-gpt2-final/`

After training, download the `recipe-gpt2-final/` folder and place it in the project root:

```
food-recipe-llm-api/
└── recipe-gpt2-final/
    ├── config.json
    ├── generation_config.json
    ├── model.safetensors
    ├── tokenizer.json
    └── tokenizer_config.json
```

**3. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Configure environment**
```bash
copy .env.example .env       # Windows
cp .env.example .env         # Mac/Linux
```

Edit `.env`:
```
MODEL_PATH=./recipe-gpt2-final
MAX_NEW_TOKENS=200
TEMPERATURE=0.7
```

**6. Run locally**
```bash
uvicorn src.api.main:app --reload
```

Open `http://localhost:8000` to see the UI.

## API Endpoints

### UI
```
GET /
```
Returns the interactive recipe generation UI.

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
  "title": "Chicken Biryani",
  "ingredients": ["500g chicken", "2 cups basmati rice", "..."],
  "instructions": ["Wash and marinate chicken...", "Heat oil in a pan...", "..."]
}
```

### Health Check
```
GET /api/health
```
```json
{"status": "ok"}
```

### Interactive API Docs
```
http://localhost:8000/docs
```

## AWS Deployment

### Prerequisites
- AWS CLI configured
- AWS SAM CLI installed
- Docker running

### Deploy manually
```bash
sam build
sam deploy --guided
```

### Deploy via CI/CD
Push to `master` branch — GitHub Actions handles the rest automatically:
```
git push origin master
```

### Required GitHub Secrets
```
AWS_ACCESS_KEY_ID      → IAM user access key
AWS_SECRET_ACCESS_KEY  → IAM user secret key
```

### Required IAM Permissions
```
AmazonEC2ContainerRegistryFullAccess
AWSLambda_FullAccess
AmazonAPIGatewayAdministrator
AWSCloudFormationFullAccess
AmazonS3FullAccess
IAMFullAccess
```

## Model Training

The GPT-2 model was fine-tuned on an Indian recipes dataset:

| Config | Value |
|---|---|
| Base model | `gpt2` (117M parameters) |
| Dataset | 5,000 Indian recipes |
| Epochs | 3 |
| Max token length | 512 |
| Final validation loss | 1.684 |
| Perplexity | ~6.3 |

Training notebook is available in the `training/` folder.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `./recipe-gpt2-final` | Local path to fine-tuned model |
| `MODEL_BUCKET` | `None` | S3 bucket name for model download on Lambda |
| `MAX_NEW_TOKENS` | `200` | Max tokens to generate |
| `TEMPERATURE` | `0.7` | Generation creativity (0.1–1.0) |

## CI/CD Pipeline

```
PR opened    → ci.yml → validates schemas + SAM template → blocks merge if failing
Merge to master → cd.yml → sam build → sam deploy → live on AWS Lambda
```

## License

MIT License — free to use, modify, and distribute.
