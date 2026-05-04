FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=employee_project.settings
ENV USE_SQLITE=False

EXPOSE 8000

CMD ["python", "-m", "gunicorn", "employee_project.wsgi:application", \
     "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
