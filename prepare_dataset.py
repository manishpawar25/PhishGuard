import pandas as pd

# Read UCI dataset
data = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="latin-1"
)

# Convert labels
data["label"] = data["label"].map({
    "ham": "safe",
    "spam": "phishing"
})

# Remove empty rows
data = data.dropna()

# Save as CSV
data.to_csv("messages.csv", index=False)

print("Dataset prepared successfully!")
print(f"Total messages: {len(data)}")
print("\nLabel distribution:")
print(data["label"].value_counts())