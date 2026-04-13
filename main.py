# --- Fix encoding issue (for Windows) ---
import sys
sys.stdout.reconfigure(encoding='utf-8')

# --- Import Libraries ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# --- Load Data ---
def load_data(filepath):
    df = pd.read_csv(filepath)
    print("SUCCESS: Data loaded -", df.shape[0], "rows")
    return df

# --- Train Model ---
def train_model(df):
    print("\nTraining model...")

    X = df[['temp', 'pressure', 'vibration', 'operational_hours']]
    y = df['failure']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Accuracy check
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("SUCCESS: Model trained")
    print("Accuracy:", round(acc, 2))

    # Save model
    joblib.dump(model, "model.pkl")
    print("Model saved as model.pkl")

    return model

# --- Load Model ---
def load_model():
    if os.path.exists("model.pkl"):
        print("Loading saved model...")
        model = joblib.load("model.pkl")
        print("SUCCESS: Model loaded")
        return model
    else:
        print("WARNING: No saved model found. Training new model...")
        df = load_data("E:/Projects/machine-failure-prediction/sensor_data.csv")
        return train_model(df)

# --- Get User Input ---
def get_input():
    print("\nEnter Machine Details:")

    while True:
        try:
            temp = float(input("Temperature: "))
            pressure = float(input("Pressure: "))
            vibration = float(input("Vibration: "))
            hours = float(input("Operational Hours: "))

            return [[temp, pressure, vibration, hours]]

        except ValueError:
            print("ERROR: Please enter valid numeric values")

# --- Prediction ---
def predict(model):
    data = get_input()

    result = model.predict(data)[0]
    prob = model.predict_proba(data)[0][1]

    print("\nPrediction Result:")

    if result == 1:
        print("FAILURE LIKELY")
        print("Probability:", round(prob * 100, 2), "%")
        print("Action: Check machine immediately")
    else:
        print("MACHINE SAFE")
        print("Failure Risk:", round(prob * 100, 2), "%")
        print("Action: Normal operation")

# --- Main ---
if __name__ == "__main__":

    model = load_model()

    while True:
        predict(model)

        choice = input("\nDo you want to continue? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting program...")
            break