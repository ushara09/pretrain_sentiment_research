from tkinter import ON
from flask import Flask, request, jsonify
from transformers import pipeline
import json

app = Flask(__name__)

# sentimentValue - NEG / Rating - 1,2
# sentimentValue - POS, NEU / Rating 3,4,5
def ratingAndFeedbackMatching(rate, sentimentValue):
    if sentimentValue == "POS" and rate == 1:
        return "reject"
    elif sentimentValue == "POS" and rate == 2:
        return "reject"
    elif sentimentValue == "NEU" and rate == 1:
        return "reject"
    elif sentimentValue == "NEU" and rate == 2:
        return "reject"
    elif sentimentValue == "NEG" and rate == 5:
        return "reject"
    elif sentimentValue == "NEG" and rate == 4:
        return "reject"
    elif sentimentValue == "NEG" and rate == 3:
        return "reject"
    else:
        return "accept"


@app.route("/sentiment", methods = ["POST"])
def feedbackValidation():
    rate = request.json['rate']
    feedback = request.json['feedback']
    specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    result = specific_model(feedback)
    sentimentValue = result[0]['label'] # positive - POS / negative - NEG / Neutral - NEU
    finalValue = ratingAndFeedbackMatching(rate, sentimentValue)
    finalObject = {"sentimentValue": sentimentValue, "finalDisition": finalValue}

    # convert to JSON
    finalJSONObject = json.dumps(finalObject)
    return finalJSONObject

@app.route("/check", methods = ["POST"])
def checkReviews():
    feedback = request.json['review']
    specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
    result = specific_model(feedback)
    return result

if __name__ == "__main__":
    app.run(debug=ON)

## FOR TESTING   

# http://127.0.0.1:5000/sentiment

# {
# 	"rate": 1,
# 	"feedback": "very bad"
# }