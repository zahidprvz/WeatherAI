import requests
import spacy
from flask import Flask, render_template, request, jsonify

nlp = spacy.load("en_core_web_md")

api_key = "35e041b8938a60daf2bad6e6275e626a"

def get_weather(city_name):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    response = requests.get(api_url)
    response_dict = response.json()

    if response.status_code == 200:
        weather = response_dict["weather"][0]["description"]
        return weather
    else:
        return None

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def get_weather_route():
    data = request.get_json()
    statement = data.get("statement")
    response = chatbot(statement)
    return jsonify({"response": response})

def chatbot(statement):
    if not statement:  # Check if statement is empty or None
        return "Please provide a statement."

    weather = nlp("Current weather in a city")
    statement = nlp(statement)
    min_similarity = 0.60

    if weather.similarity(statement) >= min_similarity:
        for ent in statement.ents:
            if ent.label_ == "GPE":  # GeoPolitical Entity
                city = ent.text
                break
        else:
            return "You need to tell me a city to check."

        city_weather = get_weather(city)
        if city_weather is not None:
            return f"In {city}, the current weather is: {city_weather}"
        else:
            return "Something went wrong."
    else:
        return "Sorry, I don't understand that. Please rephrase your statement."

if __name__ == "__main__":
    app.run(debug=True)
