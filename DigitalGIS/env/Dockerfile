# За базу используем официальный image питона
FROM python:3.8

# Отключаем буферизацию логов
ENV PYTHONUNBUFFERED 1

# Обновляем пакетный менеджер
RUN apt-get update -y && apt-get upgrade -y
#RUN apt install software-properties-common
#RUN  add-apt-repository ppa:ubuntugis/ppa -y

RUN apt-get install postgresql-13 -y
RUN apt-get install postgresql-13-postgis-3 -y
RUN apt-get install postgis -y
# Ставим зависимости GDAL, PROJ
RUN apt-get install -y gdal-bin libgdal-dev
RUN apt-get install -y python3-gdal
RUN apt-get install -y binutils libproj-dev
#RUN apt-get install -y build-dep python-psycopg2
RUN pip3 install psycopg2-binary
RUN pip3 install django
RUN pip3 install rasterio geopandas minio # s3
RUN pip3 install psycopg2 sqlalchemy geoalchemy2==0.10.2 # s3


# Копируем все файлы приложения в рабочую директорию в контейнере
COPY . /srv/html/app
WORKDIR /srv/html/app