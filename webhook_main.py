# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_cors import CORS
from service.webhook import webhook_controller

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/webhook/health', methods=['GET'])
def health():
    return jsonify({"code": 0, "mag": "Success", "data":None}), 200

app.register_blueprint(webhook_controller)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug = True, port = 8085)