# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

WORKDIR /app

COPY . /app/

# 安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 7860

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "evaluate.py"]
