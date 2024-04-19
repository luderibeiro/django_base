FROM python:3.12
LABEL mantainer="@luderibeiro"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY project/ /project
COPY scripts/ /scripts

WORKDIR /project

EXPOSE 8000

RUN apt update -y
RUN apt install -y wget \
    build-essential \
    libc6-dev
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz && \
    cp wkhtmltox/bin/wkhtmlto* /usr/bin/
RUN wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-1.1.20.tar.gz -T 360 && \
    tar -xvf freetds-1.1.20.tar.gz && \
    cd freetds-1.1.20/ && \
    ./configure --prefix=/usr/local --with-tdsver=7.4 && \
    make && \
    make install
RUN apt-get install freetds-dev freetds-bin unixodbc-dev tdsodbc python3-gdal -y
RUN echo " \n\
[FreeTDS] \n\
Description=TDS driver (Sybase/MS SQL) \n\
Driver=libtdsodbc.so \n\
Setup=libtdsS.so \n\
CPTimeout= \n\
CPReuse= \n\
UsageCount=1 \n\
" >> /etc/odbcinst.ini
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r /project/requirements.txt \
    && adduser --disabled-password --no-create-home appuser \
    && mkdir -p /data/web/static \
    && mkdir -p /data/web/media \
    && chown -R appuser:appuser /venv \
    && chown -R appuser:appuser /data/web/static \
    && chown -R appuser:appuser /data/web/media \
    && chmod -R 755 /data/web/static \
    && chmod -R 755 /data/web/media \
    && chmod -R +x /scripts \
    && chmod +rx /scripts/run.sh

ENV PATH="/scripts:/venv/bin:$PATH"

USER appuser

ENTRYPOINT [ "run.sh" ]
