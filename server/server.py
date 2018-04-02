#!/usr/bin/python3
from __future__ import print_function
from flask import Flask, url_for
from pymongo import MongoClient
from flask_cors import CORS
import pymongo
import json
import re


#   All parameter checks
import serverParameterChecks


__author__      = "Szymon Bialkowski"
__email__       = "bialkowski.sz@gmail.com"
__license__     = "MIT"


"""
    RESTful API built using Flask.
    Connects to local MongoDB database and
    returns movies, credits and actors
    depending on parameters.
"""

db_initialise_check = True
db = ""

def db_initialise():
    #   Connect to MongoDB
    client = MongoClient()

    #   Select IMDB collection
    global db
    db      = client['imdb']

    db_init_check = False




#   Flask app
app = Flask(__name__)
CORS(app)

#   GLOBAL VARIABLES
welcome = ["Welcome to my simple RESTful movie API.", {
    "endpoints": {
    "/movies": "Generates a random movie.",
    "/movies/title/title": "Selects specific movie using title. Title can include letters, numbers and dots.",
    "/movies/id/id": "Selects specific movie using ID, ID must only consist of positive integers.",
    "/movies/rating/rating" : "Selects random movie above the specified rating.",
    "/movies/rating/range/range" : "Selects random movie within the specified rating range.",
    "/movies/year/year": "Selects random movie released in specified year.",
    "/movies/decade/decade": "Selects random movie released in specified decade. Input is any year within the desired decade. 2010s = 2010-2019",
    "/credits/title/title": "Selects specific movie credits using movie title. Title can include letters, numbers and dots.",
    "/credits/id/id":"Selects specific movie credits using movie ID, ID must only consist of positive integers.",
    "/actors/name/name":"Selects specific actor details using name. Name can include letters, numbers and dots.",
    "/actors/id/id":"Selects specific actor details using ID, ID must only consist of positive integers."
    }
}]
welcomingMessage    = json.dumps(welcome)
del welcome

max_ID_length       = 10
min_release_year    = 1800
max_release_year    = 3000
longest_movie_name  = 100


#   Error handler outputs to log file for future debugging
@app.errorhandler(Exception)
def allExceptionHandler(error):
    with open("errorlog", "a") as errorFile:
        print(error, file=errorFile)
    return("SERVER ERROR")


#   Initialize database inside container
@app.route("/database/initialize", methods=['GET'])
def dbInit():
    if db_initialise_check:
        db_initialise()
    return("Initialized.")


#   Home
@app.route("/", methods=['GET'])
def home():
    return(welcomingMessage)



# Generate random movie
@app.route("/movies")
def movies():
    try:
        movie = db.movies.aggregate([{ "$sample": { "size": 1 }}])
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
         movie = json.dumps({"error": "No movies found in Database."})
    return(movie)




#   Find movie using title
@app.route("/movies/title/<title>", methods=['GET'])
def movies_title(title):
    if serverParameterChecks.isStringParameterInvalid(title):
        movie = json.dumps({"error": "Movie title length invalid or contains invalid characters."})
        return(movie)

    try:
        movie = db.movies.find({"title":title})
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
        movie = json.dumps({"error": "No movie with this title found in database."})

    return(movie)


#   Find movie using id
@app.route("/movies/id/<id>", methods=['GET'])
def movies_id(id):
    if serverParameterChecks.isIDInvalid(id):
        movie = json.dumps({"error": "Movie ID has to be a number. Ensure it is greater than 0 and smaller than 1{}".format("0" * max_ID_length)})
        return(movie)

    try:
        movie = db.movies.find({"id": int(id)})
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
        movie = json.dumps({"error": "No movie with this ID found in database."})

    return(movie)


#   Find movie above specified rating
@app.route("/movies/rating/<rating>", methods=['GET'])
def movies_rating(rating):
    if serverParameterChecks.isRatingInvalid(rating):
        movie = json.dumps({"error": "Movie rating has to be a integer/decimal number between 0 and 10."})
        return(movie)
    try:
        movie = db.movies.aggregate([{ "$match": {"vote_average": {"$gte": float(rating)}}}, {"$sample": {"size": 1}}])
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
        movie = json.dumps({"error": "No movies above this rating found in Database."})

    return(movie)


#   Find movie above specified rating
@app.route("/movies/rating/range/<ratingRange>", methods=['GET'])
def movies_rating_range(ratingRange):

    ratingRange = serverParameterChecks.isRatingRangeInvalid(ratingRange)
    if ratingRange is True:
        movie = json.dumps({"error": "Movie range has to be in the following format: 0.0-10"})
        return(movie)
    try:
        movie = db.movies.aggregate([{ "$match": {"vote_average": {"$gte": ratingRange[0], "$lte": ratingRange[1]}}}, {"$sample": {"size": 1}}])
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
        movie = json.dumps({"error": "No movies found in the range specified."})

    return(movie)


#   Find movie in specified year
@app.route("/movies/year/<year>", methods=['GET'])
def movies_year(year):
    year = serverParameterChecks.isYearInvalid(year)
    if year is True:
        movie = json.dumps({"error": "Movie release year has to be a number between {0}-{1}".format(min_release_year, max_release_year)})
        return(movie)

    try:
        regx = re.compile("^{}".format(year))
        movie = db.movies.aggregate([{ "$match": {"release_date": regx}}, {"$sample": {"size": 1}}])
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except Exception as e:
        print(e)
        movie = json.dumps({"error": "No movies found in the specified year."})

    return(movie)


#   Find movie in specified decade
@app.route("/movies/decade/<decade>", methods=['GET'])
def movies_decade(decade):
    decade = serverParameterChecks.isYearInvalid(decade)
    if decade is True:
        movie = json.dumps({"error": "Please enter in any year part of a specific decade. 2010s = 2010-2019"})
        return(movie)

    decade = int(str(decade)[:3])

    try:
        regx = re.compile("^{}".format(decade))
        movie = db.movies.aggregate([{ "$match": {"release_date": regx}}, {"$sample": {"size": 1}}])
        movie = movie.next()
        movie = serverParameterChecks.JSONEncoder().encode(movie)
    except:
        movie = json.dumps({"error": "No movies found in the specified year."})

    return(movie)


#   Find credits using title
@app.route("/credits/title/<title>", methods=['GET'])
def credits_title(title):
    credits = ""

    if serverParameterChecks.isStringParameterInvalid(title):
        movie = json.dumps({"error": "Movie title length invalid or contains invalid characters."})
        return(movie)

    try:
        credits = db.credits.find({"title":title})
        credits = credits.next()
        credits = serverParameterChecks.JSONEncoder().encode(credits)
    except:
        credits = json.dumps({"error": "No credits with this title found in database."})

    return(credits)


#   Find credits using id
@app.route("/credits/id/<id>", methods=['GET'])
def credits_id(id):
    credits = ""

    if serverParameterChecks.isIDInvalid(id):
        credits = json.dumps({"error": "Movie ID has to be a number. Ensure it is greater than 0 and smaller than 1{}".format("0" * max_ID_length)})
        return(credits)

    try:
        credits = db.credits.find({"movie_id": int(id)})
        credits = credits.next()
        credits = serverParameterChecks.JSONEncoder().encode(credits)
    except:
        credits = json.dumps({"error": "No credits with this ID found in database."})

    return(credits)


#   Find actor using name
@app.route("/actors/name/<name>", methods=['GET'])
def actors_name(name):
    actor = ""

    if serverParameterChecks.isStringParameterInvalid(name):
        actor = json.dumps({"error": "Actor name length invalid or contains invalid characters."})
        return(actor)

    try:
        print(name)
        actor = db.actors.find({"name": name})
        actor = actor.next()
        actor = serverParameterChecks.JSONEncoder().encode(actor)
    except Exception:
        actor = json.dumps({"error": "No actor with this name found in database."})

    return(actor)


#   Find actor using id
@app.route("/actors/id/<id>", methods=['GET'])
def actors_id(id):
    actor = ""

    if serverParameterChecks.isIDInvalid(id):
        actor = json.dumps({"error": "Actor ID has to be a number. Ensure it is greater than 0 and smaller than 1{}".format("0" * max_ID_length)})
        return(actor)

    try:
        actor = db.actors.find({"actor_id": int(id)})
        actor = actor.next()
        actor = serverParameterChecks.JSONEncoder().encode(actor)
    except:
        actor = json.dumps({"error": "No actor with this ID found in database."})
    return(actor)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
