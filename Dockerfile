FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system aceest && adduser --system --ingroup aceest aceest

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app.py pytest.ini ./
COPY src ./src
COPY tests ./tests

USER aceest

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]