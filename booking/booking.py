from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '127.0.0.1'

with open('{}/databases/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_booking():
   res = make_response(jsonify(bookings, 200))
   return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_userid(userid):
   for booking in bookings:
      if str(booking["userid"]) == str(userid):
         res = make_response(jsonify(booking), 200)
         return res
   return make_response(jsonify({"error":"User ID not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def post_booking(userid):
   req = request.get_json()
   # for booking in bookings:
   #    if str(booking["userid"]) == str(userid):
   #       res = make_response(jsonify({"error":"User ID exist"}), 409)
   #       return res

   lien = str('http://127.0.0.1:3202/showmovies/' + req["date"])
   showtime = requests.get(lien)

   if(showtime.status_code == 200):
      shows = showtime.json()["movies"]
      for movie_id in shows:
         if movie_id == req["movieid"]:
            bookings.append(req)
            res = make_response(jsonify({"message": "booking added"}), 200)
            return res
      res = make_response(jsonify({"message": "Le film n'est pas réservable pour cette date"}), 400)
      return res
   else:
      res = make_response(jsonify({"message": "Date error: no show"}), 400)
      return res






if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
