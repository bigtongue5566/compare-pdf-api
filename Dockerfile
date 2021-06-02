FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y python3-opencv

RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
