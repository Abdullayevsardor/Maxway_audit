FROM python:3.12-slim

# Muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="Asia/Tashkent"
WORKDIR /app

# Tizim paketlari
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Kutubxonalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Loyihani ko'chirish
COPY . .

# Static fayllarni yig'ish
RUN python manage.py collectstatic --noinput

# Gunicorn orqali ishga tushirish
CMD python manage.py makemigrations && python manage.py migrate --noinput && gunicorn project.wsgi:application --bind 0.0.0.0:8000
