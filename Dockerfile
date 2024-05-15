FROM python:3.10 as base

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y python3-dev python3-pip python3-venv python3-setuptools python3-wheel netcat-traditional \
    && apt -y install default-jre libreoffice-java-common libreoffice-writer \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

WORKDIR /opt/app

COPY requirements.txt ./

RUN pip --no-cache-dir install --upgrade pip setuptools \
    && pip --no-cache-dir install gunicorn==20.1.0 \
    && pip --no-cache-dir install -r ./requirements.txt

COPY . /opt/app/
RUN python manage.py collectstatic --noinput
CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "--timeout", "180", "--workers", "3", "config.wsgi:application"]
EXPOSE 8000