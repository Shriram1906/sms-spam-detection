# app_enhanced.py
import streamlit as st
import joblib
import re

# Load model and vectorizer
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Define suspicious keywords
suspicious_keywords = [
     # Free / Prize / Reward
    "free", "prize", "win", "won", "lottery", "jackpot", "cash", "reward",
    "bonus", "voucher", "gift", "payout", "claim", "deal", "discount",
    "redeem", "earn money", "guaranteed", "online prize", "fast cash", 
    "reward points", "limited offer", "exclusive deal", "free trial",
    
    # Urgency / Threat
    "urgent", "immediate", "important", "alert", "warning", "restricted",
    "expire", "deadline", "action required", "account suspend", "verify now",
    "confirm", "security alert", "blocked", "access denied", "update account",
    "failure", "unauthorized", "risk", "illegal", "compromise",
    
    # Click / Link / Website / Download
    "click", "link", "url", "visit", "download", "app", "login", "portal",
    "sign in", "redirect", "access", "browser", "attachment", "form", 
    "verify link", "check now", "tap here", "open now", "scan this",
    
    # Personal / Sensitive Info
    "password", "pin", "otp", "code", "secret", "confidential", "card",
    "bank", "account", "credit", "debit", "ssn", "identity", "personal",
    "scan card", "verify identity", "account number", "security code",
    
    # Promotions / Marketing / Subscriptions
    "subscription", "membership", "offer", "free trial", "exclusive", 
    "promo", "coupon", "savings", "trial", "service", "deal now",
    "limited time", "special offer", "claim bonus", "join now",
    
    # Scam / Fraud / Phishing / Hacking
    "scam", "fraud", "phishing", "fake", "spoof", "hack", "hacked",
    "compromised", "virus", "malware", "deception", "unauthorized", 
    "suspicious activity", "account hacked", "security breach", 
    "unauthorized transaction", "fake message",
    
    # Crypto / Investment / Money
    "bitcoin", "crypto", "investment", "earn crypto", "fast profit", 
    "high return", "business opportunity", "referral bonus", "work from home", 
    "make money", "easy money", "cash prize", "online earnings", 
    "investment plan", "financial gain",
    
    # Miscellaneous
    "claim your prize", "click here to win", "free bitcoin", "urgent action",
    "limited period offer", "lottery winner", "verify your account",
    "congratulations you won", "send your details", "call now", "contact us",
    "act now", "get paid", "apply now", "register now", "exclusive offer",
    "bonus reward", "cash reward", "free voucher", "limited quantity",
    "final notice", "important message", "account verification", "confirm your identity",
    "alert message", "unauthorized access", "urgent notice", "claim cash prize",
    "reward unlocked", "win big", "prize unlocked", "instant cash", "check reward"
]

# Enhanced prediction logic
def enhanced_predict(message):
    message_clean = message.lower()
    ml_pred = model.predict(vectorizer.transform([message]))[0]
    prob = model.predict_proba(vectorizer.transform([message]))[0][1]
    
    keyword_hits = [word for word in suspicious_keywords if word in message_clean]
    
    if keyword_hits and ml_pred == 0:  # ML says ham but suspicious keywords found
        return "⚠️ Suspicious (Possible Scam)", prob, keyword_hits
    elif ml_pred == 1:
        return "🚨 Spam", prob, keyword_hits
    else:
        return "✅ Safe", prob, keyword_hits

# Streamlit UI
st.set_page_config(page_title="Smart SMS Spam Detector", page_icon="📱", layout="centered")

st.title("📱SMS Spam Detection System")

message = st.text_area("✉️ Enter an SMS message to analyze:", height=150)

if st.button("Analyze"):
    if message.strip() == "":
        st.warning("Please enter a message first.")
    else:
        result, prob, keywords = enhanced_predict(message)

        # Highlight suspicious words
        highlighted = message
        for word in suspicious_keywords:
            pattern = re.compile(rf"\b{word}\b", flags=re.IGNORECASE)
            highlighted = pattern.sub(f"**:red[{word}]**", highlighted)

        st.markdown("### 🔍 Analyzed Message:")
        st.markdown(highlighted)

        st.markdown(f"### 🧠 Prediction: {result}")
        st.markdown(f"**Confidence:** {prob*100:.2f}% Spam Likelihood")

        if keywords:
            st.info(f"⚠️ Suspicious words detected: {', '.join(keywords)}")

        # Report section
        st.divider()
        st.markdown("### 📢 Think this message is spam?")
        st.markdown(
            "[Report to Government Spam Portal (TRAI)](https://www.sancharsaathi.gov.in/)",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Developed by SHRI RAM M R 💻 | Cyber Security Enthusiast")
