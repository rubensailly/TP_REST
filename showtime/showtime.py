from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3202
HOST = '127.0.0.1'

with open('{}/databases/times.json'.format("."), "r") as jsf:
   schedule = json.load(jsf)["schedule"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def get_json():
   res = make_response(jsonify(schedule, 200))
   return res

@app.route("/showmovies/<date>", methods=['GET'])
def get_date(date):
   for i in schedule:
      if str(date) == str(i["date"]):
         res = make_response(jsonify(i), 200)
         return res
   return make_response(jsonify({"error": "Date not found"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
