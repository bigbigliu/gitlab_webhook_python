# 将官方 Python 运行时用作父镜像
FROM python:3.6.8

# 升级pip
RUN python -m pip install --upgrade pip  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 将工作目录设置为 /gitlab_webhook
WORKDIR ./gitlab_webhook

# 将当前目录内容复制到位于 /gitlab_webhook 中的容器中
ADD . .

# 安装 requirements.txt 中的依赖
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

EXPOSE 9091

# 在容器启动时运行 webhook_main.py
CMD ["python", "./webhook_main.py"]
