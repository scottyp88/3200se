from flask import Flask, jsonify, request
import json

app = Flask(__name__)
@app.route("/messages", methods=["GET"])
def getmsgs():
    msgs = []
    try:
        with open("messages.json", "r", encoding="utf-8") as file:
            for line in file:
                msg = json.loads(line)
                msgs.append(msg)
    except FileNotFoundError:
        pass
    return jsonify(msgs), 200

@app.route("/messages", methods=["POST"])
def postmsgs():
    data = request.get_json()
    msg = data['message']
    with open("messages.json", "a", encoding="utf-8") as file:
        file.write(json.dumps(msg) + "\n")   
    return '', 201    

@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
