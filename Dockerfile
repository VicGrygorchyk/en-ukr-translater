FROM python:3.10.8-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY webapp/server/ $APP_HOME/
COPY webapp/app/temp/ $APP_HOME/build/
COPY requirements.txt $APP_HOME
COPY models/en_uk/ $APP_HOME/en_uk/
COPY models/uk_en/ $APP_HOME/uk_en/
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir -r requirements.txt

ENV MODEL_EN_ABS_PATH $APP_HOME/en_uk
ENV MODEL_UK_ABS_PATH $APP_HOME/uk_en

CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1
