import streamlit as st
from predict import predict

st.set_page_config(page_title="AI Moderation Agent", page_icon="🛡️")

st.title(" AI Social Media Moderation System")
st.markdown("### Harmful content is filtered before you see it")

# Toggle to show/hide blocked content
show_blocked = st.checkbox("Show blocked content")

# Simulated social media feed
comments = [
    "You are amazing ❤️",
    "I hate you",
    "This is the worst thing ever",
    "Great job, keep going!",
    "You are stupid",
    "Have a nice day 😊"
]

st.markdown("## Social Media Feed")

for comment in comments:
    result, confidence = predict(comment)

    # Moderation logic
    if "Toxic" in result and confidence > 80:
        if show_blocked:
            st.error(f" BLOCKED: {comment} ({confidence}%)")
        else:
            st.error(" This content is blocked")

    elif "Toxic" in result and confidence > 60:
        with st.expander(" This content may be offensive (click to view)"):
            st.warning(f"{comment} ({confidence}%)")

    else:
        st.success(comment)