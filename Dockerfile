FROM python:3.12 as base

ENV TZ=America/Bogota
ENV DIR /app

RUN mkdir $DIR
WORKDIR $DIR

COPY requirements.txt $DIR

RUN pip install -r requirements.txt

COPY . $DIR

CMD [ "python", "template/main.py" ]