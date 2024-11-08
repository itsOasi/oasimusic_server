FROM python:latest

WORKDIR /
COPY . /

RUN rm -f /.gitignore /database.db

RUN pip install pipenv
RUN pipenv install

EXPOSE 8080

CMD ["pipenv", "run", "python", "main.py"]
