FROM registry.ap-southeast-1.aliyuncs.com/dev-shengshi/python-base-image:1.0.1

WORKDIR /app

COPY . /app/

EXPOSE 7860

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "evaluate.py"]