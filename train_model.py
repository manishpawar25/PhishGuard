import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score


# ==================================================
# LOAD DATASET
# ==================================================

data = pd.read_csv("messages.csv")

X = data["message"]
y = data["label"]


# ==================================================
# SPLIT DATASET
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==================================================
# LINEAR SVM
# ==================================================

svm = LinearSVC()


# ==================================================
# CALIBRATED SVM
# ==================================================
# Calibration gives us probability estimates
# using predict_proba()

calibrated_svm = CalibratedClassifierCV(
    svm,
    method="sigmoid",
    cv=5
)


# ==================================================
# COMPLETE MODEL
# ==================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        calibrated_svm
    )
])


# ==================================================
# TRAIN MODEL
# ==================================================

print("Training PhishGuard model...")

model.fit(
    X_train,
    y_train
)


# ==================================================
# TEST MODEL
# ==================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"Linear SVM Accuracy: {accuracy * 100:.2f}%"
)


# ==================================================
# TEST PROBABILITY
# ==================================================

probabilities = model.predict_proba(
    X_test
)

print("Probability calibration: SUCCESS")


# ==================================================
# SAVE MODEL
# ==================================================

with open(
    "phishguard_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print(
    "PhishGuard calibrated model saved successfully!"
)