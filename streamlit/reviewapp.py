import streamlit as st
import joblib

# Page config
st.set_page_config(page_title="Authentica AI", layout="centered")

# Load model and vectorizer
import os

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "authentica_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))

# Title
st.title("Authentica")
st.caption("AI system for detecting fake reviews and emotional manipulation tactics")

st.markdown("---")

#manipulation text
urgency_words = [
"buy now","limited time","hurry","act now","only today",
"while stocks last","dont miss out","last chance"
]

exaggeration_words = [
"best ever","life changing","amazing","unbelievable",
"perfect","incredible","fantastic","mind blowing"
]

fear_words = [
"dangerous","warning","avoid","risk","unsafe",
"harmful","toxic"
]

social_pressure = [
"everyone is buying","everyone loves this",
"people love this","most popular","everyone recommends"
]

authority_words = [
"doctors recommend","experts say",
"scientifically proven","research shows"
]

emotional_words = [
"changed my life","i cried","i'm obsessed",
"i love this so much"
]

price_pressure = [
"best deal","cheap","huge discount",
"save money","limited offer"
]


# Manipulation scoring

def manipulation_score(text):

    score = 0
    text = text.lower()

    for w in urgency_words:
        if w in text:
            score += 25

    for w in exaggeration_words:
        if w in text:
            score += 20

    score += text.count("!") * 5

    return min(score,100)


# Detect tactics

def detect_tactics(text):

    tactics = []
    text = text.lower()

    if any(w in text for w in urgency_words):
        tactics.append("Urgency")

    if any(w in text for w in exaggeration_words):
        tactics.append("Exaggeration")

    if any(w in text for w in fear_words):
        tactics.append("Fear Manipulation")

    if any(w in text for w in social_pressure):
        tactics.append("Social Pressure")

    if any(w in text for w in authority_words):
        tactics.append("Authority Manipulation")

    if any(w in text for w in emotional_words):
        tactics.append("Emotional Appeal")

    if any(w in text for w in price_pressure):
        tactics.append("Financial Pressure")

    if "!" in text:
        tactics.append("Emotional Emphasis")

    return tactics


# User input
review = st.text_area("Enter a product review")


# Prediction
if st.button("Analyze"):

    vec = vectorizer.transform([review])

    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]

    confidence = max(prob)

    # Prediction result
    if pred == 1:
        st.error("Fake Review Detected")
    else:
        st.success("Genuine Review")

    st.write("Confidence:", round(confidence*100,2), "%")
    st.progress(int(confidence * 100))

    st.markdown("---")

    # Manipulation analysis
    score = manipulation_score(review)
    tactics = detect_tactics(review)

    st.subheader("Manipulation Analysis")

    st.write("Manipulation Score:", score)
    st.progress(score)

    if tactics:
        st.write("Detected tactics:")
        for t in tactics:
            st.write("•", t)
    else:
        st.write("No manipulation tactics detected.")



