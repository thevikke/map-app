FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

ENV GDAL_DATA /usr/share/gdal/3.0
ENV PROJ_LIB /usr/share/proj

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

COPY wait-for-it.sh /wait-for-it.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]