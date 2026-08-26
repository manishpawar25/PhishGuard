import streamlit as st
import pickle
import re


# -----------------------------
# Load trained SVM model
# -----------------------------
with open("phishguard_model.pkl", "rb") as file:
    model = pickle.load(file)


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="PhishGuard",
    page_icon="🔐",
    layout="centered"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🔐 PhishGuard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Based Phishing & Scam Message Detector'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Analyze suspicious SMS, WhatsApp messages and emails "
    "using Machine Learning."
)


# -----------------------------
# Message Input
# -----------------------------
message = st.text_area(
    "📩 Enter your message",
    height=180,
    placeholder="Paste your suspicious message here..."
)


# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🔍 Analyze Message", use_container_width=True):

    if not message.strip():

        st.warning("⚠️ Please enter a message first.")

    else:

        # Prediction
        prediction = model.predict([message])[0]

        # Suspicious indicators
        suspicious_words = [
            "urgent",
            "click",
            "verify",
            "otp",
            "password",
            "pin",
            "prize",
            "winner",
            "lottery",
            "reward",
            "blocked",
            "suspended",
            "claim",
            "fee",
            "bank",
            "kyc",
            "refund",
            "account"
        ]

        found_words = []

        for word in suspicious_words:

            if re.search(
                r"\b" + word + r"\b",
                message.lower()
            ):
                found_words.append(word)


        # -----------------------------
        # Phishing Result
        # -----------------------------
        if prediction == "phishing":

            st.error(
                "🚨 HIGH RISK — POSSIBLE PHISHING / SCAM"
            )

            if found_words:

                st.write("### 🔎 Suspicious Indicators")

                st.write(
                    ", ".join(
                        word.upper()
                        for word in found_words
                    )
                )

            st.warning(
                "🛡️ Safety Advice: Do not click unknown "
                "links or share OTP, PIN, passwords or "
                "banking details."
            )


        # -----------------------------
        # Safe Result
        # -----------------------------
        else:

            st.success(
                "✅ LOW RISK — MESSAGE LOOKS SAFE"
            )

            if found_words:

                st.info(
                    "Some potentially sensitive words "
                    "were detected. Stay cautious."
                )

            else:

                st.info(
                    "No major suspicious indicators "
                    "were detected."
                )


# -----------------------------
# Project Information
# -----------------------------
st.divider()

st.write("### 🤖 Model Information")

st.write(
    "Machine Learning Model: **Linear SVM**"
)

st.write(
    "Test Accuracy: **98.39%**"
)

st.write(
    "Text Processing: **TF-IDF**"
)

st.write(
    "Dataset: **5,572 SMS messages**"
)


st.divider()

st.caption(
    "PhishGuard • Python • NLP • Machine Learning • Streamlit"
)