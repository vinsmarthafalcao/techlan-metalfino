# Use uma imagem base com Python
FROM python:3.12-slim

# Instale dependências do sistema necessárias para pyodbc e SQL Server
RUN apt-get update && apt-get install -y \
    build-essential \
    unixodbc-dev \
    gcc \
    curl \
    libssl-dev \
    libffi-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y \
        msodbcsql17 \
        unixodbc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt primeiro (para aproveitar cache)
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do projeto para dentro do container
COPY . .

# Coleta arquivos estáticos (caso necessário)
RUN python manage.py collectstatic --noinput

# Expõe a porta 8000 (Django)
EXPOSE 8000

# Comando padrão para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
