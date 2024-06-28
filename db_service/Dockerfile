FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

# deps for psycopg2
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN \
  pip install --no-cache-dir -r requirements.txt && \
  apk --purge del .build-deps

COPY . .

EXPOSE 8081

CMD ["uvicorn", "main:app", "--port", "8081", "--host", "0.0.0.0"]
