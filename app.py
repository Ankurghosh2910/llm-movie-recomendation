from flask import Flask, render_template, request, jsonify
from movie_recommender import MovieRecommender
import os
import requests

app = Flask(__name__)
recommender = MovieRecommender()

# Your OMDB API key
OMDB_API_KEY = "4ed7e217"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_movie_poster', methods=['GET'])
def get_movie_poster():
    movie_title = request.args.get('title')
    if not movie_title:
        return jsonify({'error': 'No title provided'})
    
    try:
        response = requests.get(
            f'http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}'
        )
        data = response.json()
        
        if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
            return jsonify({
                'poster': data['Poster'],
                'year': data.get('Year', ''),
                'rating': data.get('imdbRating', '')
            })
        else:
            return jsonify({'error': 'Poster not found'})
    except Exception as e:
        print(f"Error fetching poster: {str(e)}")
        return jsonify({'error': str(e)})

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    preferences = request.form.get('preferences')
    if not preferences:
        return jsonify({'error': 'No preferences provided'})
    
    try:
        print(f"Received preferences: {preferences}")
        recommendations = recommender.get_recommendations(preferences)
        print(f"Got recommendations: {recommendations}")
        return jsonify({'recommendations': recommendations})
    except Exception as e:
        print(f"Error in recommendations: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)