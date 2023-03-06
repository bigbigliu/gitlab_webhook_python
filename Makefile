.PHONY : build

run:
	python3 webhook_main.py

pip:
	pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

nohup:
	nohup python3 webhook_main.py &

docker-build:
	docker build -t gitlab_webhook:v1 .

docker-run:
	docker run -d --restart=unless-stopped -p 9091:9091 --name=gitlab_webhook gitlab_webhook:v1