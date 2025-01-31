ARG PYTHON_VERSION=3.11.9
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Add these lines to copy initial data
COPY ./storage /data/storage
COPY ./model_cache /data/model_cache

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

ENV STORAGE_PATH=/data/storage
ENV MODEL_CACHE_PATH=/data/model_cache

VOLUME [ "/data/storage", "/data/model_cache" ]

EXPOSE 8000

CMD gunicorn 'app:app' --bind=0.0.0.0:8000
