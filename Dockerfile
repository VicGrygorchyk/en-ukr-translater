FROM python:3.10-slim
WORKDIR ~/app
COPY ./webapp/server .
COPY ./webapp/app/build ./build
COPY ./models/saved/modelv_2 ./model_en
COPY ./models/saved_ukr/modelv_2 ./model_ukr
RUN pip install -U transformers==4.23.1 fastapi==0.85.1 pydantic==1.10.2 uvicorn==0.19.0 translate_toolkit==3.7.4 torch==1.12.1
ARG MODEL_EN_ABS_PATH=./model_en
ARG MODEL_UK_ABS_PATH=./model_ukr
EXPOSE 8007
CMD ["python"]