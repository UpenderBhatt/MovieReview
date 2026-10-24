import os
import requests
import json
from flask import Flask, redirect, request,render_template, jsonify
from werkzeug.security import generate_password_hash

# TMDB API read access token - set this in your environment or a local .env file (never commit it)
TMDB_API_TOKEN = os.environ.get("TMDB_API_TOKEN", "")

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

#region API Interaction

#Takes a perameter used to sort which movies are collected by the GET request
def fetchMoviesByType(sort_by):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by={sort_by}"

    #Stores the API Key
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"
    }

    #Makes a get request using the url and the API Key
    response = requests.get(url, headers=headers)
    #If the API sends back the corrct data the status code will be 200
    if response.status_code == 200:
        #If the data in the correct for is sent it stores it as JSON in data
        data = response.json()
        #returns the API data in JSON form
        return data['results']
    #If no data was sent or the data didnt send 
    #correctly it will default to sending nothing
    return []


def fetchMovieDetails(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/search')
def search():
    #Every time the user types in the search box they are sent here and 
    #this code sends a request to the API and if it returns something 
    #then it will send that back to the html to be displayed to the user
    query = request.args.get('query', '')
    if query:
        movies = search_movies(query)
        #Sends id so that when the user clicks on the movie it directs them correctly
        results = [{'title': movie['title'], 'id': movie['id']} for movie in movies]
        return jsonify(results)
    return jsonify([])

def search_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def fetchMovieReviews(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"  
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def fetchMovieTrailers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US" 

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"   
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #Only sends videos that are dispalyed on youtube and are listed as trailers
        return [video for video in data['results'] if video['site'] == 'YouTube' and video['type'] == 'Trailer']
    return []
    
def fetchMovieCast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API_TOKEN}"   
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #Sending data about the cast but is limited to only 20
        return data['cast'][:20]
    return []


#Simple function used to get specifc movie type
def fetchMostPopular():
    return fetchMoviesByType(sort_by="popularity.desc")

def fetchHighestGrossing():
    return fetchMoviesByType(sort_by="revenue.desc")

def fetchMostRated():
    return fetchMoviesByType(sort_by="vote_count.desc")

#endregion

#region Rendering_Templates


@app.route('/Base')
def homePage():
    #Sends out three requests for each of the sections of movies
    most_popular_movies = fetchMostPopular()
    highest_grossing_movies = fetchHighestGrossing()
    most_rated_movies = fetchMostRated()

    #Return all three request to HomePage.html
    return render_template(
        'HomePage.html',
        most_popular=most_popular_movies,
        highest_grossing=highest_grossing_movies,
        most_rated=most_rated_movies
    )

#Movie id is stored with the webpage in the URL
@app.route("/MoviePage/<int:movie_id>")
def moviePage(movie_id):
    #Making a GET request from the API and sending this to the correct html
    movie_details = fetchMovieDetails(movie_id)
    return render_template('MoviePage.html', movie=movie_details)

@app.route("/Reviews/<int:movie_id>")
def reviews(movie_id):
    reviews_data = fetchMovieReviews(movie_id)
    movie_details = fetchMovieDetails(movie_id)
    return render_template('Reviews.html', reviews=reviews_data, movie=movie_details)

@app.route("/trailer/<int:movie_id>")
def trailer(movie_id):
    movie = fetchMovieDetails(movie_id)
    trailers = fetchMovieTrailers(movie_id)
    #Makes sure that there is a video to show before sending it
    if not movie:
        return "Movie not found", 404

    return render_template('Trailer.html', movie=movie, trailers=trailers)

@app.route("/cast/<int:movie_id>")
def cast(movie_id):
    movie = fetchMovieDetails(movie_id)
    cast = fetchMovieCast(movie_id)
    return render_template('Cast.html', movie=movie, cast=cast)

#Simple render when the page loads, needed to be able to extend html pages
@app.route("/LeaveReview/<int:movie_id>")
def leaveReview(movie_id):
    movie = fetchMovieDetails(movie_id)
    return render_template('LeaveReview.html', movie=movie)

@app.route("/Login")
def login():
    return render_template('Login.html')

@app.route("/")
def footer():
    return render_template('Footer.html')

#endregion


@app.route('/save_login', methods=['POST'])
def save_login():
    email = request.form.get('email')
    password = request.form.get('password')

    with open('loginDetails.txt', 'a') as f:
        # Never store plain-text passwords - store a salted hash instead
        f.write(f"Email: {email}\nPasswordHash: {generate_password_hash(password)}\n")

    return "Login Successful"

if __name__ == "__main__":
    # Debug mode is off unless FLASK_DEBUG=1 is set (the debugger allows code execution)
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")