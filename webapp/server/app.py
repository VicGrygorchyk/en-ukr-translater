from typing import List
import sys

import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from transformers import pipeline

sys.path.append('/home/mudro/Documents/Projects/en-ukr-translater')
from globals import MODEL_ABS_PATH


app = FastAPI()

model_checkpoint = MODEL_ABS_PATH
translator = pipeline("translation", model=model_checkpoint)


class TranslateInput(BaseModel):
    input: str = 'TranslateInput'


class TranslatedText(BaseModel):
    translation_text: str = 'TranslatedText'


@app.post('/translate', response_model=List[TranslatedText])
def translate(translate_input: TranslateInput) -> List[TranslatedText]:
    print(translate_input.dict())
    input_to_translate = translate_input.input
    result = translator(input_to_translate)
    print(result)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
