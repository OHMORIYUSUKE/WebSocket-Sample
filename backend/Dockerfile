FROM python:3.8

# コンテナ内で必要なパッケージをインストール
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# __pycache__
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]