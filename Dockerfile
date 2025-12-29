FROM python:3.14-slim

WORKDIR /app
EXPOSE 8080

COPY main.py ./
COPY requirements.txt ./
COPY ./src ./src

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD [ "python", "main.py" ]