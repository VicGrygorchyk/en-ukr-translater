### Master's thesis, Viktor Hryhorchuk.
The aim of this work is to create an online translator for legal English-Ukrainian translation. 
We will try Transformers models for it. We also learn how to preprocess data for the dataset and create 
a ML pipeline according to MLOps level 1 (aim to achieve 2 in future) principles.

# Project
This is ML project aimed to train NLP Transformer model for English-Ukrainian translation. 
The trained model would be served via API. The front-end would be provided as well.
MLFlow is used to track experiments with training and model performance progress.

## Tech stack
- ML Pipeline: mlflow, pytorch, HuggingFace
- Dataset pipeline: web-crawler to load data (Selenium) + preprocess data pipeline
- Model: Transformer from HuggingFace Hub
- API / back-end: FastAPI
- front-end: React

# Dataset
Raw files with legal text loaded from the various sources in Web, 
e.g. HUDOC database, zakon.rada.gov.ua.
Files are preprocessed and split into JSONs in format 
`{'id': int, 'translation': {'en': string, 'uk': string}}`.
HuggingFace pipeline wrapper is used to convert JSONs into Arrow format 
for later use to train a model.

# Model
Huggingface Transformer, project `Helsinki-NLP/opus-mt-en-uk`.
