FROM python:3.10-slim

WORKDIR /app

# Copiar requirements primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto
EXPOSE 8080

# Ejecutar con gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
