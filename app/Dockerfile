# Utiliza una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY app/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY ./app /app/app
COPY ./trading /app/trading

# Expone el puerto que usará la API
EXPOSE 8000

# Comando para ejecutar la API
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]