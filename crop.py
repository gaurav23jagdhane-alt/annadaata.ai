# Crop recommendation with Random Forest.
# Dataset: Kaggle "Crop Recommendation Dataset" -> save as data/crop_data.csv
# Columns: N, P, K, temperature, humidity, ph, rainfall, label
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_FILE = "crop_model.joblib"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def train():
    df = pd.read_csv("data/crop_data.csv")
    X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df["label"], test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Accuracy:", model.score(X_test, y_test))
    joblib.dump(model, MODEL_FILE)


def recommend(n, p, k, temperature, humidity, ph, rainfall, top=3):
    model = joblib.load(MODEL_FILE)
    row = pd.DataFrame([[n, p, k, temperature, humidity, ph, rainfall]], columns=FEATURES)
    probs = model.predict_proba(row)[0]
    best = probs.argsort()[::-1][:top]
    return [(model.classes_[i], float(probs[i])) for i in best]


def model_ready():
    return os.path.exists(MODEL_FILE)


if __name__ == "__main__":
    train()
