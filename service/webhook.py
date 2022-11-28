# -*- coding: utf-8 -*-
import requests
import json
from flask import request, Blueprint, jsonify, abort

webhook_controller = Blueprint('webhook_controller', __name__, url_prefix="/webhook")

WEBHOOK_VERIFY_TOKEN = "123"

@webhook_controller.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        verify_token = request.headers.get('X-Gitlab-Token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            gitlab_msg_data = request.get_json() # 接收gitlab消息

            # 发送钉钉webhook消息
            push_msg(gitlab_msg_data)

            retcode = 0
            if retcode == 0:
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'git pull error'}), 503
        else:
            return jsonify({'status': 'bad token'}), 401

    else:
        abort(400)

def push_msg(data):
    # 测试群
    ding_robot_test = "https://oapi.dingtalk.com/robot/send?access_token=86312ca29dec70688619ffff1e6509de0a21308754312ae1378aed5fdca5a862"
    # 开发组群
    dev_group_robot = "https://oapi.dingtalk.com/robot/send?access_token=942349cacc096290f3a88a439d96e5eb4fbd30cc8236d079fbaf7620fc18ca53"

    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    req_url = ""
    if  data["project"]["name"] == "mp-auto-mation":
        req_url = dev_group_robot
    elif data["project"]["name"] == "robot_dispatch_v5":
        req_url = ding_robot_test

    apple_emoji = "\ud83c\udf4e" * 3

    branch = "master"
    branch_str = data["ref"].split("/")
    if len(branch_str) == 3:
        branch = branch_str[2]

    msg = "Moonpac 代码推送" + apple_emoji + "\n"
    msg += "仓库名: " + data["project"]["name"] + "\n"
    msg += "仓库描述: " + data["project"]["description"] + "\n"
    msg += "仓库地址: " + data["repository"]["homepage"] + "\n"
    msg += "用户名: " + data["user_name"] + "\n"
    msg += "操作: " + data["event_name"] + "\n"
    msg += "branch: " + branch + "\n"
    msg += "commit_msg: " + data["commits"][0]["message"].replace("“", "").replace("”", "").replace("\n", "") + "\n"
    msg += "commit_url: " + data["commits"][0]["url"] + "\n"

    # 构建请求数据
    message ={
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            # "atMobiles":[
            #     "13510236914",
            # ],
            "isAtAll": "false" # 是否@全员
        }
    }

    info = requests.post(url=req_url, data=json.dumps(message), headers=header)
    # 判断钉钉群机器人消息是否发送成功
    if json.loads(info.text)['errmsg'] == "ok":
        print("发送成功!")
    else:
        print(json.loads(info.text))


if __name__ == '__main__':
    pass