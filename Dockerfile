FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Deno JavaScript runtime for yt-dlp YouTube extraction
RUN curl -fsSL https://deno.land/install.sh | sh

ENV PATH="/root/.deno/bin:$PATH"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 10000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
