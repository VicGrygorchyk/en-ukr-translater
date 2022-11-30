#!/bin/bash

export MODEL_EN_ABS_PATH=/home/mudro/Documents/Projects/en-ukr-translater/models/saved/modelv_2
export MODEL_UK_ABS_PATH=/home/mudro/Documents/Projects/en-ukr-translater/models/saved_ukr/modelv_2
python webapp/server/app.py
