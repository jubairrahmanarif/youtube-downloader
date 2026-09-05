FROM python:3.12-slim

# Install FFmpeg, curl and unzip
RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Deno JavaScript runtime for yt-dlp
RUN curl -fsSL https://deno.land/install.sh | sh \
    && /root/.deno/bin/deno --version

# Add Deno to PATH
ENV PATH="/root/.deno/bin:$PATH"

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

EXPOSE 10000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
