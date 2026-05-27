from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

#APP SETUP
app = Flask(__name__)

#  Enable CORS for everything (IMPORTANT)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

#LOAD MODEL
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

#PREDICT FUNCTION
def predict(text):
    text_vec = vectorizer.transform([text])

    prob = model.predict_proba(text_vec)[0]
    confidence = max(prob) * 100

    result = model.predict(text_vec)[0]

    label = "Toxic" if result == 1 else "Safe"

    return label, round(confidence, 2)

#API ROUTE
@app.route("/moderate", methods=["POST", "OPTIONS"])
def moderate():
    # Handle preflight request (VERY IMPORTANT)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    text = data.get("text", "")

    print("Received:", text)  # debug

    result, confidence = predict(text)

    return jsonify({
        "result": result,
        "confidence": confidence
    })

#RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)