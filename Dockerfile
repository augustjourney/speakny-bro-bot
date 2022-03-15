FROM python:3.9-alpine

ENV CONTAINER_HOME=/var/www
ENV PYTHONUNBUFFERED 1

WORKDIR $CONTAINER_HOME

COPY ./requirements.txt $CONTAINER_HOME/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $CONTAINER_HOME/requirements.txt

ADD . $CONTAINER_HOME

RUN apk add ffmpeg

CMD ["uvicorn", "src.app:create_app", "--host", "0.0.0.0", "--port", "8000"]