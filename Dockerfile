FROM python:3.6-alpine

WORKDIR /app
COPY . /app
RUN pip3 install pipenv==8.3.1 && pipenv install --deploy --system

CMD ["python", "run.py"]
