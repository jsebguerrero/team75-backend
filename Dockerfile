FROM python:3.8.1-slim

ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
EXPOSE 5050
WORKDIR /app

COPY . ./
RUN pip3 install -r requirements.txt
CMD ["python3", "run.py"]
