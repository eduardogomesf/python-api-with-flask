FROM python:3.10

WORKDIR /app

RUN pip install flask

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]