FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV GDAL_DATA /usr/share/gdal/3.0
ENV PROJ_LIB /usr/share/proj
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY myproject api manage.py /app/

COPY wait-for-it.sh /wait-for-it.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]