from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import json, sqlite3, secrets

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
    def createUser(self, fname, lname, email, pswrd):
        sqlConnection = sqlite3.connect("app.db")
        try:
            CU = sqlConnection.execute("insert into users (fname, lname, email, pass) values (?, ?, ?, ?)",
            (fname, lname, email, pswrd))
            sqlConnection.commit()
        finally:
            sqlConnection.close()
        return CU.lastrowid
    def retrieveUser(self, email):
        sqlConnection = sqlite3.connect("app.db")
        RU = sqlConnection.execute("select * from users where email = ?", (email,))
        RU = RU.fetchone()
        sqlConnection.close()
        return RU
    def retrieveUserID(self, id):
        sqlConnection = sqlite3.connect("app.db")
        RU = sqlConnection.execute("select * from users where id = ?", (id,))
        RU = RU.fetchone()
        sqlConnection.close()
        return RU

sessions = {}        

database = DATABASE()
app = Flask(__name__)
@app.route("/rifles", methods=["GET"])
def getRifles():
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return jsonify({"error":"Not authenticated"}), 401
    allItems = database.listItems()
    return jsonify(allItems), 200
@app.route("/rifles/<int:item>", methods=["GET"])
def getARifle(item):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return jsonify({"error":"Not authenticated"}), 401
    anItem = database.retrieveItems(item)
    if anItem is None:
        return jsonify({"error": "Rifle not found"}), 404
    return jsonify(anItem), 200

@app.route("/rifles", methods=["POST"])
def addRifle():
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return jsonify({"error":"Not authenticated"}), 401
    data = request.get_json()
    try:
        newRifle = database.createItems(data["name"], data["cartridge"], data["action_type"], data["barrel_length_in"], data["adoption_year"], data["weight_lb"], data["standard_capacity"], data["adoption_branch"])
    except (KeyError, TypeError):
        return jsonify({"error": "Missing or invalid rifle data"}), 400
    return jsonify(newRifle), 201    
@app.route("/rifles/<int:item>", methods=["PUT"])
def changeRifle(item):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return jsonify({"error":"Not authenticated"}), 401
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
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        return jsonify({"error":"Not authenticated"}), 401
    if database.retrieveItems(item) is None:
        return jsonify({"error": "Rifle not found"}), 404
    database.deleteItems(item)
    return '', 204
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5500"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Credentials"] = 'true'
    return response

@app.route("/users", methods=["POST"])
def addUser():
    data = request.get_json()
    try:
        if not isinstance(data['fname'], str) or not isinstance(data['lname'], str) or not isinstance(data['email'], str) or not isinstance(data['pswrd'], str):
            return jsonify({"error":"Missing or invalid User data"}), 400
        if not data['fname'].strip() or not data['lname'].strip() or not data['email'].strip() or not data['pswrd']:
            return jsonify({"error":"Missing or invalid User data"}), 400
        if database.retrieveUser(data['email']):
            return jsonify({"error":"Email already exists"}), 409
        hpswrd = generate_password_hash(data['pswrd'])
        newUser = database.createUser(data['fname'], data['lname'], data['email'], hpswrd)
    except (KeyError, TypeError):
        return jsonify({"error": "Missing or invalid User data"}), 400
    except sqlite3.IntegrityError:
        return jsonify({"error":"Email already exists"}), 409
    
    return jsonify(newUser), 201

@app.route("/login", methods=["POST"])
def loginUser():
    data = request.get_json()
    try:
        if not isinstance(data['email'], str) or not isinstance(data['pswrd'], str):
            return jsonify({"error":"Missing or invalid Email or Password"}), 400
        if not data['email'].strip() or not data['pswrd']:
            return jsonify({"error":"Missing or invalid Email or Password"}), 400
        usr = database.retrieveUser(data['email'])
        if usr:
            h = usr[4]
            pwd = check_password_hash(h, data['pswrd'])
            if pwd:
                session_id = secrets.token_urlsafe(32)
                sessions[session_id] = usr[0]
                usr_data = [usr[0], usr[1], usr[2], usr[3]]
                response = jsonify({"message":"Logged in", "user":usr_data})
                response.set_cookie("session_id", session_id, httponly=True, samesite="Lax")
                return response, 200
    except (KeyError, TypeError):
        return jsonify({"error":"Missing or invalid Email or Password"}), 400
    return jsonify({"error":"Not able to log in check Email or Password"}), 401

@app.route("/users", methods=["GET"])
def authUser():
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        usr = sessions[session_id]
        usr = database.retrieveUserID(usr)
        if usr:
            usr_data = [usr[0], usr[1], usr[2], usr[3]]
            response = jsonify({"message":"Authenticated", "user":usr_data})
            return response, 200
    return jsonify({"error":"Not able to authenticate user"}), 401       

@app.route("/sessions/current", methods=["DELETE"])
def logoutUser():
    session_id = request.cookies.get("session_id")
    response = jsonify({"message":"Successfully logged out"})
    if session_id in sessions:
        response.delete_cookie("session_id")
        del(sessions[session_id])
        return response, 200
    return jsonify({"error":"Log out was not successful"}), 401


