# -*- coding: utf-8 -*-
"""
    main
    ~~~~~~~~~~~~~~

    flask-apiSign-demo

    Docstring conventions:
    http://flask.pocoo.org/docs/0.10/styleguide/#docstrings

    Comments:
    http://flask.pocoo.org/docs/0.10/styleguide/#comments

    :copyright: (c) 2017 by taochengwei.
    :license: MIT, see LICENSE for more details.
"""

__author__  = 'taochengwei'
__doc__     = 'Api签名验证Demo'
__date__    = '2017-11-20'

from flask import Flask, jsonify
from utils.Signature import Signature

# 初始化定义application
app = Flask(__name__)
Sign = Signature()

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(500)
def server_error(error=None):
    message = {
        "msg": "Server error",
        "code": 500
    }
    return jsonify(message), 500

@app.errorhandler(404)
def not_found(error=None):
    message = {
        "msg": "Not found",
        "code": 404
    }
    return jsonify(message), 404

@app.errorhandler(403)
def Permission_denied(error=None):
    message = {
        "msg": "Permission denied",
        "code": 403
    }
    return jsonify(message), 403

@app.route("/")
@Sign.signature_required
def index():
    # 正确请求将返回以下内容，否则将被signature_required拦截，返回请求验证信息： {"msg": "error message", "success": False}
    return jsonify(ping="pong")

if __name__ == '__main__':
    from config import GLOBAL
    Host = GLOBAL["Host"]
    Port = GLOBAL["Port"]
    app.run(host=Host, port=int(Port), debug=True)