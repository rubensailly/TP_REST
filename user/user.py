from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '127.0.0.1'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/user/", methods=['GET'])
def get_users():
   res = make_response(jsonify(users), 200)
   return res

@app.route("/user/<id>", methods=['GET'])
def get_userid(id):
   for user in users:
      if str(user["id"]) == str(id):
         res = make_response(jsonify(user))
         return res
   res = make_response(jsonify("message: user not found"), 200)
   return res


@app.route("/reservations/<userid>", methods=['GET'])
def get_reservation(userid):
   user = requests.get("http://127.0.0.1:3203/user/" + userid)
   if user.status_code == 200:
      data = {
         "reservations": []
      }
      user = user.json()
      reservations = requests.get("http://127.0.0.1:3201/bookings/" + userid).json()
      for reservation in reservations["dates"]:
         date_entry = {"date": reservation["date"], "movies": []}
         for movie in reservation["movies"]:
            film = requests.get("http://127.0.0.1:3200/movies/" + movie).json()
            date_entry["movies"].append(film)
         data["reservations"].append(date_entry)

      return jsonify(data), 200
   res = make_response(jsonify("message: user not found"), 200)
   return res


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
