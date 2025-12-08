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

# exponer puerto dinámico (Railway lo asigna)
ENV PORT=${PORT}
EXPOSE ${PORT}

# ejecutar uvicorn con el puerto que Railway asigna
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
