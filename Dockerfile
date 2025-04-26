FROM python:3.9-slim

# Crear directorio de trabajo
WORKDIR /api

# Copiar código y dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pymysql

COPY . .

CMD python -m flask run --host 0.0.0.0