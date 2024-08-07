FROM python:3.11-slim

WORKDIR /app

# Install postgresql-client
RUN apt-get update && apt-get install -y bash postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]
