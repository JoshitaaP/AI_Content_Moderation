import pickle

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def predict(text):
    text_vec = vectorizer.transform([text])

    prob = model.predict_proba(text_vec)[0]
    confidence = max(prob) * 100

    result = model.predict(text_vec)[0]

    label = "Toxic" if result == 1 else "Safe"

    return label, round(confidence, 2)

if __name__ == "__main__":
    user_input = input("Enter text: ")
    print(predict(user_input))