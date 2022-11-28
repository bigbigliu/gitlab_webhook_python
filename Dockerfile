FROM python:3.6.8

RUN python -m pip install --upgrade pip  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 将工作目录设置为 /myapps
WORKDIR ./gitlab_webhook

# 将当前目录内容复制到位于 /myapps 中的容器中
ADD . .

# 安装 requirements.txt 中指定的任何所需软件包
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

EXPOSE 8085

# 在容器启动时运行 app.py
CMD ["python", "./webhook_main.py"]
