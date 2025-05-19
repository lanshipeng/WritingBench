FROM registry.ap-southeast-1.aliyuncs.com/python-base-image:1.0.1 AS build

WORKDIR /app

COPY . /app/

EXPOSE 7860

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "evaluate.py"]
