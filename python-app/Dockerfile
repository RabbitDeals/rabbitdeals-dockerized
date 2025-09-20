FROM python:3.11-slim

# Definindo diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para evitar criação de arquivos .pyc e bufferização de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalando dependências do sistema (caso precise de mais pacotes)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiando o requirements.txt primeiro para otimizar o cache
COPY requirements.txt .

# Instalando as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante do código
COPY . .

# Comando para rodar a aplicação
CMD ["python", "app.py"]
