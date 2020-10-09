FROM python:3.8.1

WORKDIR /usr/src/dj_lora

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y
RUN pip install --upgrade pip

COPY ./req.txt .
RUN pip install -r req.txt

COPY ./entrypoint.sh .
COPY . .

ENTRYPOINT ["/usr/src/dj_lora/entrypoint.sh"]

