import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List

# Load environment variables
load_dotenv()

class MovieRecommender:
    def __init__(self):
        # Configure the Gemini API
        API_KEY = "AIzaSyA4-r_R9SPW5LX1hSfPCxG-gBgNX3X8Zxs"
        genai.configure(api_key=API_KEY)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_recommendations(self, preferences: str) -> str:
        # Construct the prompt
        prompt = f"""
        Act as a movie recommendation expert. Based on the following preferences, 
        recommend 10 movies with a brief explanation for each. Format exactly as shown:

        User preferences: {preferences}

        Please format each recommendation exactly like this:
        1. **Movie Title** - Brief explanation about the movie and why it matches the preferences.
        2. **Movie Title** - Brief explanation about the movie and why it matches the preferences.
        etc.

        Provide exactly 10 recommendations, numbered from 1 to 10.
        """
        
        try:
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Print for debugging
            print("API Response:", response.text)
            
            return response.text
        except Exception as e:
            print(f"Error in get_recommendations: {str(e)}")
            return f"An error occurred: {str(e)}"

def main():
    try:
        recommender = MovieRecommender()
        
        print("\n" + "="*50)
        print("Welcome to the Movie Recommender System!")
        print("="*50 + "\n")
        
        print("Please tell me about your movie preferences.")
        print("For example: genres you like, favorite actors, mood, or any specific themes")
        
        user_preferences = input("\nYour preferences: ")
        
        print("\nGenerating recommendations...")
        recommendations = recommender.get_recommendations(user_preferences)
        
        print("\nHere are your personalized movie recommendations:\n")
        print(recommendations)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
