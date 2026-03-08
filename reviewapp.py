import streamlit as st
import joblib

model = joblib.load("authentica_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("Authentica AI")

review = st.text_area("Enter a product review")

if st.button("Analyze"):

    vec = vectorizer.transform([review])

    pred = model.predict(vec)[0]

    prob = model.predict_proba(vec)[0]

    label = "Fake Review" if pred == 1 else "Real Review"

    confidence = max(prob)

    st.write("Authenticity:", label)
    st.write("Confidence:", round(confidence*100,2),"%")


