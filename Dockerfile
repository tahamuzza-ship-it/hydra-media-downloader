FROM python:3.10-slim

# Install yt-dlp
RUN pip install yt-dlp

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# App directory
WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 8080
CMD ["npm", "start"]
