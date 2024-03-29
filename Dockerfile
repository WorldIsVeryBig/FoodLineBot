#從倉庫拉取帶有 python 3.7 的 Linux 環境
FROM python:3.7

# 創建 code 文件夾並將其設置為工作目錄
RUN mkdir /code
WORKDIR /code

# 將當前目錄覆制到容器的 code 目錄
COPY . /code/

#安裝庫
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--preload"]
