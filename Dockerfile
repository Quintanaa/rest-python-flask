FROM python:3.9-slim

# Crear directorio de trabajo
WORKDIR /api

# Copiar código y dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto de la app (ajusta si usás otro)
EXPOSE 5000

# Ejecutar la app
CMD python -m flask run
