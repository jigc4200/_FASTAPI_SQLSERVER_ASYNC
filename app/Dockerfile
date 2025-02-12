# Usar una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /V1/app

# Instalar dependencias del sistema y el driver ODBC de SQL Server
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    gpg \
    software-properties-common \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/microsoft.gpg \
    && echo "deb [arch=amd64] https://packages.microsoft.com/ubuntu/24.04/prod noble main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python 3.12 y pip
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# Crear un entorno virtual
RUN python3 -m venv /venv

# Actualizar pip
RUN /venv/bin/pip install --upgrade pip

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar las dependencias de Python dentro del entorno virtual
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de la carpeta actual al contenedor
COPY . .

# Añadir el directorio raíz del proyecto al PYTHONPATH
ENV PYTHONPATH="/V1"

# Establecer el entorno virtual como la ruta de ejecución
ENV PATH="/venv/bin:$PATH"

# Exponer el puerto 8000 (el puerto que usa FastAPI por defecto)
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
