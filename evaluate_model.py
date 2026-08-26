import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load dataset
data = pd.read_csv("messages.csv")

X = data["message"]
y = data["label"]

# Same split used for testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Load trained model
with open("phishguard_model.pkl", "rb") as file:
    model = pickle.load(file)

# Predict test data
predictions = model.predict(X_test)

# Metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(
    y_test,
    predictions,
    pos_label="phishing"
)
recall = recall_score(
    y_test,
    predictions,
    pos_label="phishing"
)
f1 = f1_score(
    y_test,
    predictions,
    pos_label="phishing"
)

print("\n===== PhishGuard Model Evaluation =====")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1 Score  : {f1 * 100:.2f}%")

print("\n===== Confusion Matrix =====")
print(confusion_matrix(
    y_test,
    predictions,
    labels=["safe", "phishing"]
))

print("\n===== Classification Report =====")
print(classification_report(y_test, predictions))