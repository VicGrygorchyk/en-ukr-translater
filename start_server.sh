#!/bin/bash

export MODEL_EN_ABS_PATH=/home/mudro/Documents/Projects/en-ukr-translater/models/saved/en_uk_legal_translater
export MODEL_UK_ABS_PATH=/home/mudro/Documents/Projects/en-ukr-translater/models/saved_ukr/uk_en_legal_translater
python webapp/server/app.py
