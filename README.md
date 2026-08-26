# 🛡️ PhishGuard

### AI-Based Phishing and Scam Message Detector

PhishGuard is a Machine Learning based application designed to detect whether an SMS or message is **Safe** or **Phishing**.

It uses Natural Language Processing (NLP) and Machine Learning techniques to analyze message content and classify potentially harmful messages.

---

## 🚀 Features

* 🔍 Detects Safe and Phishing messages
* 🤖 Machine Learning based classification
* 🧠 NLP-based text processing
* 📊 Multiple Machine Learning models
* 📈 Model performance evaluation
* 🌐 Interactive Streamlit web application
* ⚡ Fast message prediction

---

## 🧠 Machine Learning Models

The project compares:

* Logistic Regression
* Naive Bayes
* Linear Support Vector Machine (SVM)

### 🏆 Best Model

**Linear SVM**

**Accuracy: 98.39%**

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Natural Language Processing
* TF-IDF
* Linear SVM
* Streamlit
* Git & GitHub

---

## 📂 Project Structure

```text
PhishGuard/
├── app.py
├── train_model.py
├── compare_models.py
├── evaluate_model.py
├── prepare_dataset.py
├── messages.csv
├── phishguard_model.pkl
├── SMSSpamCollection
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/manishpawar25/PhishGuard.git
cd PhishGuard
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

The application will open in your browser.

Enter an SMS or message and PhishGuard will classify it as:

**✅ Safe** or **⚠️ Phishing**

---

## 📊 Model Evaluation

The model is evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
* Classification Report

The current best model, **Linear SVM**, achieved **98.39% accuracy**.

---

## 🎯 Future Improvements

* 📸 Screenshot-based message detection using OCR
* 🔗 Real-time URL analysis
* 📧 Email phishing detection
* 🌍 Multilingual message detection
* 🧠 Deep Learning based classification
* 🌐 Browser extension

---

## 👨‍💻 Author

**Manish Pawar**

Computer Engineering Student

---

⭐ If you find PhishGuard useful, consider giving the repository a star.
