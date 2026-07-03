from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

POSTCODE_ENDPOINT = "https://api.postcodes.io/postcodes/" #constants
WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather?"

def postcode_lookup(postcode): #function to accept poostcode
    response = requests.get(POSTCODE_ENDPOINT + postcode) #get request to postcode api
    if response.status_code == 200: #if request ok
        result = response.json()["result"] #json response into python dict
        return result["latitude"], result["longitude"] #returns as tuple = fixed
    return None #if not found return none


def get_weather(latitude, longitude):#get weather data using lat and long
    api_key = os.environ.get("WEATHER_API_KEY") #
    # with open("/Users/kyramngoma/Tech610/DevOpsPython/Requests/weather exercise/weather_api_key") as file: #open file with api key
    #     api_key = file.readline().strip() #more secure
    response = requests.get(WEATHER_ENDPOINT +f"lat={latitude}&lon={longitude}&appid={api_key}&units=metric")
    #api request and send get request - units changed to metric at the end
    if response.status_code == 200: #checks weather request successful
        return response.json() # converts json into python dict
    return None
#################

@app.route('/') #home endpoint
def home():
    return render_template('index.html')
#######################
@app.route("/weather/<postcode>") #single postcode #path parameter
def weather_api(postcode):
    coordinates = postcode_lookup(postcode) #sends postcode to postcode api
    if not coordinates:
        return jsonify({"ERROR": "Postcode not found"})

    latitude, longitude = coordinates #tuple into 2 variables
    weather = get_weather(latitude, longitude) #call weather api
    if not weather:
        return jsonify({"ERROR": "Weather data unavailable" })

    return jsonify({
        "postcode": postcode,
        "region": weather["name"],
        "temperature": weather["main"]["temp"],
        "feels_like": weather["main"]["feels_like"],
        "humidity": weather["main"]["humidity"],
        "conditions": weather["weather"][0]["description"]
    })

######################################

#multiple postcodes




###################
if __name__ == "__main__":
    app.run(debug=True, port=5000)



