FROM python:3.12-slim

# instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# crear carpeta de app
WORKDIR /app

# copiar requirements e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar todo lo demás
COPY . .

# exponer puerto
ENV PORT=8000
EXPOSE 8000

# correr uvicorn
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
