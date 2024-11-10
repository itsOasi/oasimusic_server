FROM python:latest

WORKDIR /
COPY . /

RUN rm -f /.gitignore /database.db

RUN pip install pipenv
RUN pipenv install

EXPOSE 8000/udp
EXPOSE 8000/tcp

CMD ["pipenv", "run", "python", "main.py"]
