import json
import re
from bson import ObjectId

max_ID_length       = 10
min_release_year    = 1800
max_release_year    = 3000
longest_movie_name  = 100

#   JSON Encoder for ObjectId error
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#   Checks title of movie, returns boolean
def isStringParameterInvalid(title):

    #   If title length greater than 0 but smaller than longest_movie_name
    if not 0 < len(title) < longest_movie_name:
        return(True)

    #   Regex check for illegal characters
    check = re.search('[;\$!@\#\^&\*()_+=`"~\]\[]', title)
    if check:
        return(True)

    return(False)


#   Checks id of movie, returns boolean
def isIDInvalid(id):
    if not 0 < len(id) < max_ID_length:
        return(True)
    try:
        id = int(id)
        return(id < 1)
    except:
        return(True)


#   Checks rating of movie, returns boolean
def isRatingInvalid(rating):
    if not 0 < len(rating) < 4:
        return(True)
    try:
        rating = float(rating)
        return(not -1 < rating < 11)
    except Exception as e:
        return(True)


#   Checks ratings range of movie, returns boolean or rating array if valid
def isRatingRangeInvalid(ratingRange):
    if not 2 < len(ratingRange) < 8:
        return(True)
    try:
        ratingRange = ratingRange.split('-')
        print(ratingRange)
        if len(ratingRange) != 2:
            return(True)

        ratingRange[0] = float(ratingRange[0])
        ratingRange[1] = float(ratingRange[1])
        if not 0 <= ratingRange[0] <= 10:
            return(True)
        elif not 0 <= ratingRange[1] <= 10:
            return(True)

        return(ratingRange)
    except:
        return(True)


#   Checks year of movie, returns boolean or year if valid
def isYearInvalid(year):
    if len(year) != 4:
        return(True)
    try:
        year = int(year)
        if not min_release_year < year < max_release_year:
            return(True)
        return(year)
    except:
        return(True)
