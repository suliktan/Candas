FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости для сборки psycopg2 и Pillow
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику при создании образа
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "gandas_uniforms.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
