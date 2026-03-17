from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords

# Download once
nltk.download('stopwords', quiet=True)

app = Flask(__name__)
CORS(app)

# Load model safely
try:
    model = joblib.load("phishing_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None
    vectorizer = None

stop_words = set(stopwords.words('english'))


def clean_email(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)


@app.route("/")
def home():
    return jsonify({
        "server": "Email Fraud Detection Server",
        "status": "running"
    })


@app.route("/check-email", methods=["POST"])
def check_email():

    # ✅ Model check
    if model is None or vectorizer is None:
        return jsonify({"error": "Model not loaded"}), 500

    # ✅ File check
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400

    try:
        # ✅ Read file
        email_text = file.read().decode("utf-8", errors="ignore")

        if not email_text.strip():
            return jsonify({"error": "File is empty"}), 400

        # ✅ Clean + Transform
        cleaned = clean_email(email_text)
        vector = vectorizer.transform([cleaned])

        # ✅ Predict
        prediction = model.predict(vector)[0]
        probability = model.predict_proba(vector)[0]

        legit_prob = float(probability[0]) * 100
        fraud_prob = float(probability[1]) * 100

        final_result = (
            "Fraud / Phishing Email"
            if prediction == 1
            else "Legitimate Email"
        )

        return jsonify({
            "filename": file.filename,
            "final_prediction": final_result,
            "fraud_probability_percent": round(fraud_prob, 2),
            "legitimate_probability_percent": round(legit_prob, 2)
        })

    except Exception as e:
        print("❌ Error during prediction:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)