FROM python:3.10-slim

# Install dependencies for ffmpeg
RUN apt-get update && apt-get install -y ffmpeg nodejs npm

# Install yt-dlp
RUN pip install yt-dlp

# Workdir
WORKDIR /app

# Install Node dependencies
COPY package.json .
RUN npm install

# Copy app files
COPY . .

EXPOSE 8080
CMD ["npm", "start"]
