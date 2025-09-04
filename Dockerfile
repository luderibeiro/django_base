FROM python:3.12-slim-bookworm AS builder
LABEL mantainer="@luderibeiro"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalação de dependências de sistema para psycopg e outras ferramentas
RUN apt update -y && \
    apt install -y --no-install-recommends \
    wget \
    build-essential \
    libc6-dev \
    postgresql-client \
    freetds-dev \
    freetds-bin \
    unixodbc-dev \
    tdsodbc \
    python3-gdal \
    # Limpeza do cache APT para reduzir o tamanho da imagem
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Instalação wkhtmltopdf (se necessário para a imagem final)
# Se wkhtmltopdf for usado apenas durante o build ou em um serviço separado, isso pode ser movido.
# Mantendo aqui por enquanto, assumindo que é necessário no runtime.
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    cp wkhtmltox/bin/wkhtmlto* /usr/bin/ && \
    rm wkhtmltox-0.12.4_linux-generic-amd64.tar.xz

# Configuração FreeTDS ODBC
RUN echo " \n\
[FreeTDS] \n\
Description=TDS driver (Sybase/MS SQL) \n\
Driver=libtdsodbc.so \n\
Setup=libtdsS.so \n\
CPTimeout= \n\
CPReuse= \n\
UsageCount=1 \n\
" >> /etc/odbcinst.ini

# Copiar requirements.txt e instalar dependências Python
COPY project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- IMAGEM FINAL DE EXECUÇÃO ---
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar as dependências do sistema e binários instalados na etapa de build
# Isso é um pouco complexo devido ao wkhtmltopdf e freetds
# Vamos copiar apenas o essencial.
# Copiar binários wkhtmltopdf
COPY --from=builder /usr/bin/wkhtmlto* /usr/bin/
# Copiar configuração ODBC
COPY --from=builder /etc/odbcinst.ini /etc/odbcinst.ini

# Copiar as dependências Python instaladas
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Criar diretórios de dados e usuário appuser
RUN adduser --disabled-password --no-create-home appuser
RUN mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    mkdir -p /app/project/logs && \
    mkdir -p /app/data && \
    chown -R appuser:appuser /data/web/static && \
    chown -R appuser:appuser /data/web/media && \
    chown -R appuser:appuser /app/project/logs && \
    chown -R appuser:appuser /app/data && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R 755 /app/project/logs && \
    chmod -R 755 /app/data

# Copiar o código do projeto e scripts
COPY project/ /app/project
COPY scripts/ /app/scripts

# Dar permissão de execução aos scripts e corrigir permissões
RUN chmod +x /app/scripts/run.sh && \
    chown -R appuser:appuser /app/project && \
    chmod -R 755 /app/project

# Definir PATH para scripts e binários python
ENV PATH="/app/scripts:/usr/local/bin:$PATH"

EXPOSE 8000

USER appuser

ENTRYPOINT [ "/app/scripts/run.sh" ]
