FROM mcr.microsoft.com/playwright/python:v1.41.2-jammy

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
