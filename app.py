import streamlit as st
import pickle
import re
import math
from pathlib import Path

from PIL import Image
import pytesseract
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="PhishGuard",
    page_icon="🛡️",
    layout="centered",
)


# ============================================================
# LOAD MODEL
# ============================================================
MODEL_FILE = Path("phishguard_model.pkl")

if not MODEL_FILE.exists():
    st.error("❌ phishguard_model.pkl was not found.")
    st.info("Keep phishguard_model.pkl in the same folder as app.py.")
    st.stop()

try:
    with MODEL_FILE.open("rb") as file:
        model = pickle.load(file)
except Exception as e:
    st.error("❌ Unable to load phishguard_model.pkl")
    st.code(str(e))
    st.stop()


# ============================================================
# TESSERACT OCR CONFIGURATION
# ============================================================
possible_tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

for tesseract_path in possible_tesseract_paths:
    if Path(tesseract_path).exists():
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        break


# ============================================================
# SESSION STATE
# ============================================================
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(59,130,246,0.28), transparent 28%),
            radial-gradient(circle at 90% 20%, rgba(236,72,153,0.20), transparent 28%),
            radial-gradient(circle at 50% 100%, rgba(139,92,246,0.25), transparent 35%),
            linear-gradient(135deg, #020617 0%, #172554 40%, #312e81 72%, #581c87 100%);
    }

    .block-container {
        max-width: 950px;
        padding-top: 35px;
        padding-bottom: 60px;
    }

    .brand-icon {
        text-align: center;
        font-size: 65px;
        margin-bottom: 0;
    }

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-subtitle {
        text-align: center;
        color: #e2e8f0;
        font-size: 21px;
        font-weight: 800;
    }

    .description {
        text-align: center;
        color: #cbd5e1;
        font-size: 15px;
        margin-top: 10px;
        margin-bottom: 25px;
    }

    .stTextArea textarea {
        background-color: rgba(15,23,42,0.96) !important;
        color: white !important;
        border-radius: 16px !important;
        border: 2px solid #6366f1 !important;
        font-size: 16px !important;
    }

    .stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 15px;
        font-size: 17px;
        font-weight: 800;
    }

    .result-card {
        padding: 30px;
        margin-top: 25px;
        margin-bottom: 25px;
        border-radius: 25px;
        text-align: center;
        background: rgba(15,23,42,0.92);
        border: 2px solid rgba(255,255,255,0.12);
        box-shadow: 0 15px 45px rgba(0,0,0,0.35);
    }

    .result-icon {
        font-size: 52px;
    }

    .result-title {
        font-size: 31px;
        font-weight: 900;
        margin-top: 5px;
    }

    .result-subtitle {
        font-size: 19px;
        font-weight: 800;
        color: #cbd5e1;
        margin-top: 5px;
    }

    .result-description {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.6;
        margin-top: 15px;
    }

    .high-risk {
        border-color: #ef4444;
        box-shadow: 0 0 35px rgba(239,68,68,0.25);
    }

    .high-risk .result-title {
        color: #f87171;
    }

    .medium-risk {
        border-color: #f59e0b;
        box-shadow: 0 0 35px rgba(245,158,11,0.20);
    }

    .medium-risk .result-title {
        color: #fbbf24;
    }

    .low-risk {
        border-color: #22c55e;
        box-shadow: 0 0 35px rgba(34,197,94,0.20);
    }

    .low-risk .result-title {
        color: #4ade80;
    }

    [data-testid="stMetric"] {
        background: rgba(15,23,42,0.92);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 10px 25px rgba(0,0,0,0.22);
    }

    .indicator-box {
        padding: 18px;
        border-radius: 18px;
        background: rgba(15,23,42,0.90);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
    }

    .safety-box {
        padding: 22px;
        border-radius: 20px;
        background: rgba(15,23,42,0.90);
        border: 1px solid #3b82f6;
        color: #cbd5e1;
        line-height: 1.7;
        margin-top: 25px;
    }

    .dashboard-card {
        padding: 22px;
        border-radius: 20px;
        background: rgba(15,23,42,0.90);
        border: 1px solid rgba(255,255,255,0.12);
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.20);
    }

    .dashboard-number {
        font-size: 32px;
        font-weight: 900;
        color: white;
    }

    .dashboard-label {
        color: #cbd5e1;
        font-size: 14px;
        margin-top: 5px;
    }

    .info-card {
        padding: 22px;
        border-radius: 20px;
        background: rgba(15,23,42,0.90);
        border: 1px solid rgba(255,255,255,0.12);
        color: #cbd5e1;
        line-height: 1.7;
        margin-top: 15px;
    }

    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================
st.markdown(
    '<div class="brand-icon">🛡️</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-title">PhishGuard</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-subtitle">AI-Powered Message Security</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="description">'
    'Detect suspicious messages and protect yourself from phishing and online scams.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================
st.divider()

page = st.radio(
    "Navigation",
    [
        "📩 Scanner",
        "📊 Dashboard",
        "🤖 Model Information",
        "🛡️ Safety Tips",
        "ℹ️ About Project",
    ],
    horizontal=True,
)


# ============================================================
# SUSPICIOUS WORDS
# ============================================================
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
    "account",
    "login",
    "payment",
    "transfer",
    "cashback",
    "offer",
    "limited",
    "confirm",
    "security",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def find_phishing_class(classes):
    """Return the index of the phishing class when it can be identified."""
    normalized = [str(cls).strip().lower() for cls in classes]

    phishing_names = {
        "phishing",
        "phish",
        "spam",
        "scam",
        "fraud",
        "malicious",
        "1",
        "true",
        "yes",
    }

    for index, value in enumerate(normalized):
        if value in phishing_names:
            return index

    return None


def get_model_probability(text):
    """
    Safely obtain a phishing probability from the saved model.

    Priority:
    1. predict_proba
    2. decision_function
    3. predict fallback

    This deliberately NEVER calls decision_function on an object
    unless that object actually has the method.
    """

    # --------------------------------------------------------
    # 1. predict_proba
    # --------------------------------------------------------
    if hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba([text])[0]
            classes = list(getattr(model, "classes_", range(len(probabilities))))

            phishing_index = find_phishing_class(classes)

            if phishing_index is not None:
                return float(probabilities[phishing_index])

            # If labels are not recognizable, use the second class
            # for a normal binary 0/1 classifier.
            if len(probabilities) == 2:
                return float(probabilities[1])

            return float(max(probabilities))
        except Exception:
            pass

    # --------------------------------------------------------
    # 2. decision_function
    # --------------------------------------------------------
    if hasattr(model, "decision_function"):
        try:
            raw_score = model.decision_function([text])

            if hasattr(raw_score, "__len__"):
                score = float(raw_score[0])
            else:
                score = float(raw_score)

            score = max(min(score, 10.0), -10.0)
            probability = 1.0 / (1.0 + math.exp(-score))

            classes = list(getattr(model, "classes_", []))

            if len(classes) == 2:
                phishing_index = find_phishing_class(classes)

                if phishing_index == 0:
                    return 1.0 - probability
                if phishing_index == 1:
                    return probability

            return probability
        except Exception:
            pass

    # --------------------------------------------------------
    # 3. Pipeline fallback
    # --------------------------------------------------------
    if hasattr(model, "named_steps"):
        try:
            steps = model.named_steps
            classifier = None
            vectorizer = None

            for name, step in steps.items():
                name_lower = name.lower()

                if hasattr(step, "predict_proba") or hasattr(step, "decision_function"):
                    classifier = step

                if "tfidf" in name_lower or "vector" in name_lower:
                    vectorizer = step

            if classifier is not None and vectorizer is not None:
                transformed = vectorizer.transform([text])

                if hasattr(classifier, "predict_proba"):
                    probabilities = classifier.predict_proba(transformed)[0]
                    classes = list(
                        getattr(
                            classifier,
                            "classes_",
                            range(len(probabilities)),
                        )
                    )

                    phishing_index = find_phishing_class(classes)

                    if phishing_index is not None:
                        return float(probabilities[phishing_index])

                    if len(probabilities) == 2:
                        return float(probabilities[1])

                    return float(max(probabilities))

                if hasattr(classifier, "decision_function"):
                    raw_score = classifier.decision_function(transformed)

                    if hasattr(raw_score, "__len__"):
                        score = float(raw_score[0])
                    else:
                        score = float(raw_score)

                    score = max(min(score, 10.0), -10.0)
                    probability = 1.0 / (1.0 + math.exp(-score))

                    classes = list(getattr(classifier, "classes_", []))

                    if len(classes) == 2:
                        phishing_index = find_phishing_class(classes)

                        if phishing_index == 0:
                            return 1.0 - probability
                        if phishing_index == 1:
                            return probability

                    return probability
        except Exception:
            pass

    # --------------------------------------------------------
    # 4. Prediction fallback
    # --------------------------------------------------------
    try:
        prediction = str(model.predict([text])[0]).strip().lower()

        if prediction in {
            "phishing",
            "phish",
            "spam",
            "scam",
            "fraud",
            "malicious",
            "1",
            "true",
            "yes",
        }:
            return 0.85

        return 0.15
    except Exception:
        return 0.50


def analyze_message(text):
    """Return prediction, probability, and suspicious keywords."""
    prediction = str(model.predict([text])[0]).strip().lower()
    model_probability = max(0.0, min(1.0, get_model_probability(text)))

    found_words = []

    for word in suspicious_words:
        if re.search(
            r"\b" + re.escape(word) + r"\b",
            text.lower(),
        ):
            found_words.append(word)

    # Small keyword contribution. The ML model remains the main signal.
    keyword_score = min(len(found_words) * 0.025, 0.15)

    phishing_labels = {
        "phishing",
        "phish",
        "spam",
        "scam",
        "fraud",
        "malicious",
        "1",
        "true",
        "yes",
    }

    is_phishing_prediction = prediction in phishing_labels

    if is_phishing_prediction:
        phishing_percent = max(model_probability * 100.0, 55.0)
    else:
        phishing_percent = min(model_probability * 100.0, 45.0)

    phishing_percent += keyword_score * 100.0
    phishing_percent = max(0.0, min(99.0, phishing_percent))
    phishing_percent = round(phishing_percent, 1)

    safe_percent = round(100.0 - phishing_percent, 1)

    return prediction, phishing_percent, safe_percent, found_words


# ============================================================
# PAGE 1 - SCANNER
# ============================================================
if page == "📩 Scanner":
    st.subheader("📩 Analyze a Message")

    input_method = st.radio(
        "Choose input method",
        [
            "⌨️ Type / Paste Message",
            "📸 Upload Screenshot",
        ],
        horizontal=True,
    )

    message = ""

    # --------------------------------------------------------
    # TEXT INPUT
    # --------------------------------------------------------
    if input_method == "⌨️ Type / Paste Message":
        message = st.text_area(
            "📩 Enter your message",
            height=180,
            placeholder=(
                "Paste a suspicious SMS, WhatsApp message or email here..."
            ),
        )

    # --------------------------------------------------------
    # SCREENSHOT INPUT
    # --------------------------------------------------------
    else:
        uploaded_file = st.file_uploader(
            "📸 Upload Message Screenshot",
            type=["png", "jpg", "jpeg", "webp"],
        )

        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(
                    image,
                    caption="Uploaded Screenshot",
                    use_container_width=True,
                )

                with st.spinner("🔤 Extracting text from screenshot..."):
                    try:
                        message = pytesseract.image_to_string(image).strip()
                    except Exception as e:
                        st.error("❌ Unable to extract text from image.")
                        st.code(str(e))
                        message = ""

                if message:
                    st.success("✅ Text extracted successfully!")

                    with st.expander("👀 View Extracted Message"):
                        st.write(message)
                else:
                    st.warning("⚠️ No readable text found in screenshot.")

            except Exception as e:
                st.error("❌ Unable to open the uploaded image.")
                st.code(str(e))

    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------
    if st.button(
        "🔍 ANALYZE MESSAGE",
        type="primary",
        use_container_width=True,
    ):
        if not message.strip():
            st.warning(
                "⚠️ Please enter a message or upload a screenshot first."
            )
        else:
            try:
                prediction, phishing_percent, safe_percent, found_words = (
                    analyze_message(message)
                )
            except Exception as e:
                st.error("❌ Model prediction failed.")
                st.code(str(e))
                st.stop()

            # ------------------------------------------------
            # RISK LEVEL
            # ------------------------------------------------
            if phishing_percent >= 80:
                risk_title = "🚨 HIGH RISK"
                risk_subtitle = "PHISHING DETECTED"
                risk_class = "high-risk"
                risk_description = (
                    "This message appears highly suspicious. "
                    "Do not click unknown links or share OTP, PIN, "
                    "passwords or banking information."
                )

            elif phishing_percent >= 50:
                risk_title = "⚠️ MEDIUM RISK"
                risk_subtitle = "BE CAREFUL"
                risk_class = "medium-risk"
                risk_description = (
                    "This message contains suspicious patterns. "
                    "Verify the sender and information before taking any action."
                )

            else:
                risk_title = "✅ LOW RISK"
                risk_subtitle = "LIKELY SAFE"
                risk_class = "low-risk"
                risk_description = (
                    "No strong phishing pattern was detected. "
                    "However, always verify unexpected messages before "
                    "sharing sensitive information."
                )

            # ------------------------------------------------
            # RESULT CARD
            # ------------------------------------------------
            st.markdown(
                f"""
                <div class="result-card {risk_class}">
                    <div class="result-icon">🛡️</div>
                    <div class="result-title">{risk_title}</div>
                    <div class="result-subtitle">{risk_subtitle}</div>
                    <div class="result-description">{risk_description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # DETECTION ESTIMATE
            # ------------------------------------------------
            st.subheader("📊 Detection Estimate")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "⚠️ Phishing Risk",
                    f"{phishing_percent:.1f}%",
                )

            with col2:
                st.metric(
                    "✅ Safe",
                    f"{safe_percent:.1f}%",
                )

            st.write(f"**Phishing Risk: {phishing_percent:.1f}%**")
            st.progress(phishing_percent / 100.0)

            # ------------------------------------------------
            # INDICATORS
            # ------------------------------------------------
            st.subheader("🔎 Suspicious Indicators")

            if found_words:
                indicators = " • ".join(
                    word.upper() for word in found_words
                )

                st.markdown(
                    f"""
                    <div class="indicator-box">
                        ⚠️ {indicators}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.success(
                    "✅ No common suspicious keywords detected."
                )

            # ------------------------------------------------
            # SAFETY REMINDER
            # ------------------------------------------------
            st.markdown(
                """
                <div class="safety-box">
                    🔐 <b>Safety Reminder</b>
                    <br><br>
                    Never share OTPs, PINs, passwords or banking details
                    with unknown people or websites.
                    <br><br>
                    Always verify the sender before clicking links or making payments.
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ------------------------------------------------
            # SAVE HISTORY
            # ------------------------------------------------
            history_item = {
                "message": message[:150],
                "result": prediction,
                "phishing": phishing_percent,
                "safe": safe_percent,
            }

            st.session_state.scan_history.insert(0, history_item)
            st.session_state.scan_history = (
                st.session_state.scan_history[:10]
            )


# ============================================================
# PAGE 2 - DASHBOARD
# ============================================================
elif page == "📊 Dashboard":
    st.subheader("📊 PhishGuard Dashboard")

    total_scans = len(st.session_state.scan_history)

    phishing_count = sum(
        1
        for scan in st.session_state.scan_history
        if str(scan["result"]).lower()
        in {
            "phishing",
            "phish",
            "spam",
            "scam",
            "fraud",
            "malicious",
            "1",
            "true",
            "yes",
        }
    )

    safe_count = total_scans - phishing_count

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="dashboard-number">{total_scans}</div>
                <div class="dashboard-label">Total Scans</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="dashboard-number">{phishing_count}</div>
                <div class="dashboard-label">Phishing Detected</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="dashboard-number">{safe_count}</div>
                <div class="dashboard-label">Safe Messages</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.subheader("📈 Phishing vs Safe")

    if total_scans > 0:
        chart_data = pd.DataFrame(
            {
                "Result": ["Phishing", "Safe"],
                "Count": [phishing_count, safe_count],
            }
        )

        st.bar_chart(chart_data.set_index("Result"))
    else:
        st.info(
            "📭 No scan data available yet. Analyze some messages first."
        )

    st.subheader("🕘 Recent Scan History")

    if st.session_state.scan_history:
        for index, scan in enumerate(
            st.session_state.scan_history,
            start=1,
        ):
            if str(scan["result"]).lower() in {
                "phishing",
                "phish",
                "spam",
                "scam",
                "fraud",
                "malicious",
                "1",
                "true",
                "yes",
            }:
                status = "🚨 Phishing"
            else:
                status = "✅ Safe"

            with st.expander(
                f"{index}. {status} — {scan['phishing']}% Phishing"
            ):
                st.write("**Message:**")
                st.write(scan["message"])
                st.write(f"⚠️ Phishing Risk: {scan['phishing']}%")
                st.write(f"✅ Safe: {scan['safe']}%")

        if st.button(
            "🗑️ Clear Scan History",
            use_container_width=True,
        ):
            st.session_state.scan_history = []
            st.rerun()
    else:
        st.info("No scan history available.")


# ============================================================
# PAGE 3 - MODEL INFORMATION
# ============================================================
elif page == "🤖 Model Information":
    st.subheader("🤖 Model Information")

    st.markdown(
        """
        <div class="info-card">
            <h3>🧠 Machine Learning Pipeline</h3>
            PhishGuard uses a machine learning pipeline for detecting
            potentially suspicious messages.
            <br><br>
            <b>Feature Extraction:</b> TF-IDF
            <br>
            TF-IDF converts text messages into numerical features that
            can be processed by the machine learning model.
            <br><br>
            <b>Classifier:</b> Linear Support Vector Machine
            <br>
            The classifier separates messages into phishing and safe categories.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("⚙️ Model Pipeline")

    col1, col2 = st.columns(2)

    with col1:
        st.info("1️⃣ Text Message")
        st.info("2️⃣ TF-IDF Vectorization")

    with col2:
        st.info("3️⃣ Linear SVM")
        st.success("4️⃣ Phishing / Safe Result")

    st.subheader("📚 Dataset Information")

    dataset_file = Path("messages.csv")

    if dataset_file.exists():
        try:
            data = pd.read_csv(dataset_file)

            st.metric("Dataset Messages", len(data))

            st.write("**Dataset Columns:**")
            st.write(", ".join(map(str, data.columns)))

            if "label" in data.columns:
                st.write("**Class Distribution:**")
                st.bar_chart(data["label"].value_counts())
        except Exception as e:
            st.warning("⚠️ messages.csv could not be loaded.")
            st.code(str(e))
    else:
        st.warning(
            "⚠️ messages.csv was not found in the project folder."
        )

    st.subheader("🎯 Model Accuracy")

    st.info(
        "The model accuracy is obtained from the training/testing process "
        "used to create phishguard_model.pkl."
    )

    st.code("TF-IDF + Linear SVM")


# ============================================================
# PAGE 4 - SAFETY TIPS
# ============================================================
elif page == "🛡️ Safety Tips":
    st.subheader("🛡️ Phishing Safety Tips")

    tips = [
        (
            "🔐 Never share OTP",
            "Never share OTPs with unknown people.",
        ),
        (
            "🔗 Check links carefully",
            "Avoid clicking unexpected or suspicious links.",
        ),
        (
            "📱 Verify the sender",
            "Check the sender's identity before responding.",
        ),
        (
            "💳 Protect banking information",
            "Never share PINs, passwords, CVV or banking credentials.",
        ),
        (
            "🎁 Be careful with prizes",
            "Unexpected lottery, reward and prize messages may be phishing.",
        ),
        (
            "⚠️ Don't panic",
            "Urgent messages about blocked or suspended accounts should be verified.",
        ),
        (
            "🌐 Use official websites",
            "Open websites directly instead of using suspicious links.",
        ),
        (
            "🔄 Keep accounts secure",
            "Use strong passwords and available security features.",
        ),
    ]

    for title, description in tips:
        st.markdown(
            f"""
            <div class="info-card">
                <h3>{title}</h3>
                {description}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE 5 - ABOUT PROJECT
# ============================================================
elif page == "ℹ️ About Project":
    st.subheader("ℹ️ About PhishGuard")

    st.markdown(
        """
        <div class="info-card">
            <h2>🛡️ PhishGuard</h2>
            <b>AI-Powered Message Security</b>
            <br><br>
            PhishGuard is a machine-learning based security project
            designed to analyze suspicious SMS, WhatsApp messages and emails.
            <br><br>
            The system uses natural language processing techniques to
            identify patterns that may indicate phishing or scam messages.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("✨ Project Features")

    features = [
        "📩 Text Message Analysis",
        "📸 Screenshot Text Extraction using OCR",
        "🤖 Machine Learning Classification",
        "📊 Phishing Risk Estimation",
        "🔎 Suspicious Keyword Detection",
        "📈 Scan Dashboard",
        "🕘 Recent Scan History",
        "🛡️ Phishing Safety Tips",
    ]

    for feature in features:
        st.success(feature)

    st.subheader("💻 Technology Stack")

    tech_data = pd.DataFrame(
        {
            "Technology": [
                "Python",
                "Streamlit",
                "Scikit-learn",
                "TF-IDF",
                "Linear SVM",
                "Pytesseract",
                "Pillow",
                "Pandas",
            ],
            "Purpose": [
                "Programming Language",
                "Web Application",
                "Machine Learning",
                "Text Feature Extraction",
                "Classification",
                "OCR",
                "Image Processing",
                "Dataset Handling",
            ],
        }
    )

    st.table(tech_data)

    st.subheader("🔄 Project Workflow")

    st.markdown(
        """
        <div class="info-card">
            📩 Message / Screenshot
            <br>↓<br>
            🔤 OCR if screenshot is uploaded
            <br>↓<br>
            🧹 Text Processing
            <br>↓<br>
            🧠 TF-IDF Feature Extraction
            <br>↓<br>
            🤖 Linear SVM Classification
            <br>↓<br>
            📊 Risk Estimation
            <br>↓<br>
            🛡️ Phishing / Safe Result
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "🎓 This application can be demonstrated as an academic project "
        "for machine learning, cyber security and phishing detection."
    )


# ============================================================
# FOOTER
# ============================================================
st.divider()

st.markdown(
    """
    <div class="footer-text">
        🛡️ <b>PhishGuard</b> • AI-Powered Message Security
        <br>
        Protect • Detect • Stay Safe
    </div>
    """,
    unsafe_allow_html=True,
)
