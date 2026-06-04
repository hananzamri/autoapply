cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (required by Reflex)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Initialize Reflex
RUN reflex init

EXPOSE 3000 8000

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0"]
EOF