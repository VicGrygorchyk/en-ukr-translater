from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-en-uk"
translator = pipeline("translation", model=model_checkpoint)
result = translator('Viktor is my name')
print(result)
