import pandas as pd
import re
import nltk
import joblib

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_email(text):

    text = str(text).lower()
    text = re.sub(r'<.*?>',' ',text)
    text = re.sub(r'http\S+',' ',text)
    text = re.sub(r'[^a-zA-Z]',' ',text)

    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)


# Load datasets
ceas = pd.read_csv("CEAS_08.csv")
fraud = pd.read_csv("fraud_email_.csv")


# Prepare CEAS dataset
ceas["text"] = ceas["subject"].fillna("") + " " + ceas["body"].fillna("")
ceas = ceas[["text","label"]]


# Prepare fraud dataset
fraud = fraud.rename(columns={
"Text":"text",
"Class":"label"
})

fraud = fraud[["text","label"]]


# Merge datasets
data = pd.concat([ceas,fraud], ignore_index=True)


# Clean text
data["text"] = data["text"].apply(clean_email)


X = data["text"]
y = data["label"]


# Feature extraction
vectorizer = TfidfVectorizer(max_features=5000)

X_vector = vectorizer.fit_transform(X)


# Train test split
X_train, X_test, y_train, y_test = train_test_split(
X_vector,
y,
test_size=0.2,
random_state=42
)


# Model
model = LogisticRegression(max_iter=1000)

model.fit(X_train,y_train)


# Evaluate
pred = model.predict(X_test)

accuracy = accuracy_score(y_test,pred)

print("Model Accuracy:",accuracy)


# Save model
joblib.dump(model,"phishing_model.pkl")
joblib.dump(vectorizer,"vectorizer.pkl")

print("Model trained and saved successfully")