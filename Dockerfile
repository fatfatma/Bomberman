# Bomberman Game Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for pygame and MySQL)
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY bomberman/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY bomberman/ .

# Set SDL to use dummy video driver (headless mode for server)
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy
ENV PYTHONUNBUFFERED=1

# Expose port for server
EXPOSE 5000

# Run the game server
CMD ["python", "-c", "from network.server import GameServer; server = GameServer(); server.start()"]
