# 基础镜像
FROM python:3.8-slim-buster

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到镜像中
COPY app.py .

# 安装依赖项
RUN pip install flask

# 设置环境变量
ENV FLASK_APP=app.py

# 暴露端口
EXPOSE 4396

# 启动应用程序
CMD ["flask", "run", "--host", "0.0.0.0"]