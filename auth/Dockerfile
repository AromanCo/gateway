FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libpq-dev curl

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
