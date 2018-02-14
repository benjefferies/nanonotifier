FROM python:3.6

WORKDIR /app
COPY . /app
RUN pip3 install pipenv==8.3.1 && pipenv install --deploy --system

CMD ["/app/run.sh"]