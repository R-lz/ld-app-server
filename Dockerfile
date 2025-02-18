FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install psycopg2-binary

COPY . .
RUN mkdir -p app/static templates uploads

# 创建启动脚本
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'echo "Waiting for database to be ready..."' >> /app/start.sh && \
    echo 'while ! pg_isready -h db -p 5432 > /dev/null 2> /dev/null; do' >> /app/start.sh && \
    echo '  sleep 1' >> /app/start.sh && \
    echo 'done' >> /app/start.sh && \
    echo 'echo "Database is ready!"' >> /app/start.sh && \
    echo 'sleep 2' >> /app/start.sh && \
    echo 'python create_admin.py' >> /app/start.sh && \
    echo 'uvicorn app.main:app --host 0.0.0.0 --port 8000' >> /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"] 