FROM python:3.6

WORKDIR /app

RUN pip install pipenv
RUN adduser examineur --gecos "" --disabled-password --uid 65500

ADD Pipfile Pipfile.lock ./

USER examineur
RUN pipenv install

USER root
ADD examineur.py ./

USER examineur
ENTRYPOINT ["pipenv", "run", "/app/examineur.py"]
