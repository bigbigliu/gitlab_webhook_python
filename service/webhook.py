# -*- coding: utf-8 -*-
import requests
import json
from flask import request, Blueprint, jsonify, abort
import traceback

webhook_controller = Blueprint('webhook_controller', __name__, url_prefix="/webhook")

WEBHOOK_VERIFY_TOKEN = "123"

@webhook_controller.route('/', methods=['POST'])
def webhook():
    try:
        if request.method == 'POST':
            verify_token = request.headers.get('X-Gitlab-Token')
            if verify_token == WEBHOOK_VERIFY_TOKEN:
                gitlab_msg_data = request.get_json() # 接收gitlab消息

                # 发送钉钉webhook消息
                push_msg(gitlab_msg_data)
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'bad token'}), 401

        else:
            return jsonify({'status': 'bad request'}), 405
    except Exception as e:
        print("发送通知失败:{} 行数:{}".format(traceback.format_exc(), e.__traceback__.tb_lineno))
        return jsonify({'status': 'Failed'}), 500
        

def push_msg(data):
    # 机器人测试群
    test_notify_group = "https://oapi.dingtalk.com/robot/send?access_token=24aaa49669e47d7c35d7c88ca9c74412a2f5c813e3d7abafa5e3f4fd46bdb8a9"

    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    # req_url = ""
    # if  data["project"]["name"] == "mp-auto-mation":
    #     req_url = dev_group_robot
    # elif data["project"]["name"] == "robot_dispatch_v5":
    #     req_url = ding_robot_test

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
            "content": msg.replace("gitlab.example.com", "10.173.26.101:8081")
        },
        "at": {
            # "atMobiles":[
            #     "13510236914",
            # ],
            "isAtAll": "false" # 是否@全员
        }
    }

    info = requests.post(url=test_notify_group, data=json.dumps(message), headers=header)
    # 判断钉钉群机器人消息是否发送成功
    if json.loads(info.text)['errmsg'] == "ok":
        print("发送成功!")
    else:
        print(json.loads(info.text))

@webhook_controller.route('/jenkins', methods=['POST'])
def webhook_jenkins():
    try:
        if request.method == 'POST':
            gitlab_msg_data = request.get_json()
            print("gitlab_msg_data: ", gitlab_msg_data)
            jenkins_push_msg(gitlab_msg_data)
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad request'}), 405
    except Exception as e:
        print("发送通知失败:{} 行数:{}".format(traceback.format_exc(), e.__traceback__.tb_lineno))
        return jsonify({'status': 'Failed'}), 500

def jenkins_push_msg(data):
    msg = ""
    if data["status"] == "Success":
        apple_emoji = "\ud83c\udf4e" * 3
        msg = "Moonpac 推送通知" + apple_emoji + "\n"
        msg += data["service_name"] + " " + "构建成功" + "\n"
        msg += "镜像版本: " +  data["image"] + "\n"
        msg += "Jenkins地址: " + data["jenkins_url"]
    elif data["status"] == "Failed":
        apple_emoji = "\ud83c\udf4e" * 3
        msg = "Moonpac 推送通知" + apple_emoji + "\n"
        msg += data["service_name"] + " " + "构建失败" + "\n"
        msg += "Jenkins地址: " + data["jenkins_url"]

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

    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    req_url = "https://oapi.dingtalk.com/robot/send?access_token=19e2d46029e4d605e39fb74da281b934eaa0d4a4cf70f4b15f9d5c32f2c7da24"
    info = requests.post(url=req_url, data=json.dumps(message), headers=header)
    # 判断钉钉群机器人消息是否发送成功
    if json.loads(info.text)['errmsg'] == "ok":
        print("发送成功!")
    else:
        print(json.loads(info.text))

if __name__ == '__main__':
    pass