from flask import Flask, jsonify, request
import json, sqlite3

class DATABASE:
    def listItems(self):
        sqlConnection = sqlite3.connect("app.db")
        result = sqlConnection.execute("select * from rifles")
        result = result.fetchall()
        sqlConnection.close()
        return result
    def retrieveItems(self, item):
        for line in self.listItems():
            if item == line[0]:
                return line
    def createItems(self, name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch):
        sqlConnection = sqlite3.connect("app.db")
        CI = sqlConnection.execute("insert into rifles (name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch) values (?, ?, ?, ?, ?, ?, ?, ?)",
        (name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch))
        sqlConnection.commit()
        sqlConnection.close()
        return CI.lastrowid
    def replaceItems(self, name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch, id):
        sqlConnection = sqlite3.connect("app.db")
        RI = sqlConnection.execute('update rifles set name = ?, cartridge = ?, action_type = ?, barrel_length_in = ?, adoption_year = ?, weight_lb = ?, standard_capacity = ?, adoption_branch = ? where id= ?',
        (name, cartridge, action_type, barrel_length_in, adoption_year, weight_lb, standard_capacity, adoption_branch,id))
        sqlConnection.commit()
        sqlConnection.close()
        return self.retrieveItems(id)
    def deleteItems(self, id):
        sqlConnection = sqlite3.connect("app.db")
        DI = sqlConnection.execute('delete from rifles where id= ?', (id,))
        sqlConnection.commit()
        sqlConnection.close()
        return DI.rowcount



database = DATABASE()
app = Flask(__name__)
@app.route("/rifles", methods=["GET"])
def getRifles():
    allItems = database.listItems()
    return jsonify(allItems), 200
@app.route("/rifles/<int:item>", methods=["GET"])
def getARifle(item):
    anItem = database.retrieveItems(item)
    if anItem is None:
        return jsonify({"error": "Rifle not found"}), 404
    return jsonify(anItem), 200

@app.route("/rifles", methods=["POST"])
def addRifle():
    data = request.get_json()
    try:
        newRifle = database.createItems(data["name"], data["cartridge"], data["action_type"], data["barrel_length_in"], data["adoption_year"], data["weight_lb"], data["standard_capacity"], data["adoption_branch"])
    except (KeyError, TypeError):
        return jsonify({"error": "Missing or invalid rifle data"}), 400
    return jsonify(newRifle), 201    
@app.route("/rifles/<int:item>", methods=["PUT"])
def changeRifle(item):
    data = request.get_json()
    try:
        if database.retrieveItems(item) is None:
            return jsonify({"error": "Rifle not found"}), 404
        replRifle = database.replaceItems(data["name"], data["cartridge"], data["action_type"], data["barrel_length_in"], data["adoption_year"], data["weight_lb"], data["standard_capacity"], data["adoption_branch"], item)
    except (KeyError, TypeError):
        return jsonify({"error": "Missing or invalid rifle data"}), 400
    return jsonify(replRifle), 200
@app.route("/rifles/<int:item>", methods=["DELETE"])
def delRifle(item):
    if database.retrieveItems(item) is None:
        return jsonify({"error": "Rifle not found"}), 404
    database.deleteItems(item)
    return '', 204
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

