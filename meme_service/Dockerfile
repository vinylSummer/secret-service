FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
