FROM mcr.microsoft.com/playwright/python:v1.51.0-jammy

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
