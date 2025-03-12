import re
import secrets
import string
import streamlit as st
import time

if "password_history" not in st.session_state:
    st.session_state.password_history = []

def evaluate_password(password):
    score = 0
    feedback = []
    common_passwords = {"password123", "12345678", "qwerty", "letmein"}
    if password in common_passwords:
        return 1, "❌ Weak Password - High Risk"

    weights = {
        "length": 3,
        "uppercase_lowercase": 1.5,
        "digit": 1,
        "special_char": 2,
        "repeating_chars": -2
    }

    if len(password) >= 12:
        score += weights["length"]
    else:
        feedback.append("Increase password length to at least 12 characters.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += weights["uppercase_lowercase"]
    else:
        feedback.append("Use a mix of uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += weights["digit"]
    else:
        feedback.append("Include at least one number.")

    if re.search(rf"[{re.escape(string.punctuation)}]", password):
        score += weights["special_char"]
    else:
        feedback.append("Add at least one special character.")

    if re.search(r"(.)\1{2,}", password):
        score += weights["repeating_chars"]
        feedback.append("Avoid repeating the same character three or more times.")

    # Return password strength level and message
    if score >= 7:
        return 3, "🛡 Strong Password - Secure & Reliable"
    elif score >= 4:
        return 2, "⚠️ Moderate Password - Needs Improvement"
    else:
        return 1, "❌ Weak Password - High Risk"

# Strong Password Generator
def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password

#  Calculation
def rate_password_entropy(password):
    if len(password) == 0:
        return "🔢 Entropy Score: 0/10 (Invalid Input)"
    unique_chars = len(set(password))
    entropy_score = round(unique_chars / len(password) * 10, 2)
    return f"🔢 Entropy Score: {entropy_score}/10 (Higher is better.)"

# Streamlit App Configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")
st.title("🔐 Advanced Password Strength Checker")
st.markdown("Secure your online accounts with a strong password!")

# Password Generator Section
st.subheader("🔑 Generate a Strong Password")
password_length = st.slider("Select Password Length", 8, 32, 16)

if st.button("Generate Password"):
    generated_password = generate_strong_password(password_length)
    st.session_state.password_history.append(generated_password)  
    st.success("🛡 Strong Password Generated!")
    st.code(generated_password)

# Password History 
if st.session_state.password_history:
    st.subheader("📜 Password History")
    for idx, pwd in enumerate(st.session_state.password_history): 
        st.write(f"{idx + 1}. `{pwd}`")

    if st.button("Clear Password History"):
        st.session_state.password_history.clear()
        st.rerun()  

st.markdown("---")

# Password Strength Checker 
st.subheader("🔍 Check Your Password Strength")
password = st.text_input("Enter Your Password", type="password")

if st.button("Check Strength"):
    if not password.strip():
        st.warning("⚠️ Please enter a password before checking strength.")
    else:
        with st.spinner("Analyzing your password..."):
            time.sleep(1)

        strength, result = evaluate_password(password)
        entropy = rate_password_entropy(password)

        st.markdown(
            f'<div style="padding: 10px; font-weight: bold; text-align: center; background-color: {"#4CAF50" if strength == 3 else "#FFA500" if strength == 2 else "#FF4B4B"}; color: white; border-radius: 8px;">{result}</div>',
            unsafe_allow_html=True
        )
        st.progress(strength / 3)
        st.write(entropy)

        if strength == 1:
            suggested_password = generate_strong_password()
            st.write("🔹 Suggested Strong Password:", f"`{suggested_password}`")

st.markdown("---")

# Password Security Tips 
st.subheader("🔑 Tips for Creating a Strong Password")
st.markdown("""
- Use **at least 12 characters**
- Avoid **more than 3 consecutive repeating characters**
- Include a mix of **uppercase, lowercase, numbers, and special characters**
- Avoid common passwords like `password123` or `qwerty`
- Use a **password manager** to keep track of your secure passwords
""")
