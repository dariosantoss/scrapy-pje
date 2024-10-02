FROM ubuntu:22.04

# Defina o maintainer (opcional)
LABEL maintainer="seu-email@exemplo.com"

# Atualize o sistema e instale Python 3, pip e dependências para o Google Chrome
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxtst6 \
    libxss1 \
    libappindicator3-1 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    fonts-liberation \
    libcurl4 \
    libvulkan1 \
    xdg-utils \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instale o Google Chrome
RUN wget https://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_92.0.4515.107-1_amd64.deb && \
    dpkg -i google-chrome-stable_92.0.4515.107-1_amd64.deb && \
    apt-get -f install -y && \
    rm google-chrome-stable_92.0.4515.107-1_amd64.deb

RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver



WORKDIR /app

# Copie e instale as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie o restante dos arquivos da aplicação
COPY . .

# Defina a variável de ambiente
ENV PYTHONPATH=/app

# Comando para rodar o aplicativo FastAPI no Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]