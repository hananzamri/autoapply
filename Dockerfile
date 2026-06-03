FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN reflex export --frontend-only --no-zip 2>/dev/null || true

CMD ["reflex", "deploy"]