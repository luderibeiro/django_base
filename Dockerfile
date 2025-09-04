# Multi-stage build para otimização
FROM python:3.12-slim-bookworm AS builder
LABEL maintainer="@luderibeiro"

# Variáveis de ambiente para otimização
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependências de sistema em uma única camada
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libc6-dev \
        libpq-dev \
        freetds-dev \
        freetds-bin \
        unixodbc-dev \
        tdsodbc \
        wget \
        ca-certificates && \
    # Instalar wkhtmltopdf
    wget -q https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    tar xf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    cp wkhtmltox/bin/wkhtmlto* /usr/bin/ && \
    # Configurar FreeTDS ODBC
    echo "[FreeTDS]\nDescription=TDS driver (Sybase/MS SQL)\nDriver=libtdsodbc.so\nSetup=libtdsS.so\nCPTimeout=\nCPReuse=\nUsageCount=1" >> /etc/odbcinst.ini && \
    # Limpeza completa
    rm -rf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz wkhtmltox && \
    apt-get purge -y build-essential libc6-dev wget && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copiar e instalar dependências Python
COPY project/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- IMAGEM FINAL OTIMIZADA ---
FROM python:3.12-slim-bookworm

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/scripts:/usr/local/bin:$PATH"

WORKDIR /app

# Instalar apenas dependências runtime essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        freetds-bin \
        unixodbc \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copiar binários e configurações do builder
COPY --from=builder /usr/bin/wkhtmlto* /usr/bin/
COPY --from=builder /etc/odbcinst.ini /etc/odbcinst.ini
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Criar usuário e diretórios em uma única camada
RUN adduser --disabled-password --no-create-home --gecos "" appuser && \
    mkdir -p /data/web/static /data/web/media /app/project/logs /app/data && \
    chown -R appuser:appuser /data /app && \
    chmod -R 755 /data /app

# Copiar código do projeto
COPY --chown=appuser:appuser project/ /app/project/
COPY --chown=appuser:appuser scripts/ /app/scripts/

# Dar permissões de execução
RUN chmod +x /app/scripts/run.sh

EXPOSE 8000

USER appuser

ENTRYPOINT ["/app/scripts/run.sh"]
