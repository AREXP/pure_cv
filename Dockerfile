FROM python:3.7.5

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
ADD . /app

EXPOSE 8080
