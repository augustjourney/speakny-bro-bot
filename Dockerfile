FROM python:3.9-alpine
ENV CONTAINER_HOME=/var/www
ENV PYTHONUNBUFFERED 1
ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME
RUN pip install -r $CONTAINER_HOME/requirements.txt
RUN apk add ffmpeg
RUN apk add tzdata
ENV TZ "Europe/Moscow"