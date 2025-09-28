import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Load your dataset
df = pd.read_csv('../finall.csv')

# Separate features and target
X = df.drop(columns=["next_difficulty"])
y = df["next_difficulty"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Save the trained model
joblib.dump(clf, "model/next_difficulty_model.pkl")

print("Model trained and saved successfully!")

