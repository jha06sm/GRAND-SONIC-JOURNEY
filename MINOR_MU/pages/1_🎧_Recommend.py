import streamlit as st
from recs.text_recs import get_text_recommendations   # Minor MU FAISS-based
from recs.gsj_recs import gsj_recommend              # GSJ YouTube-based

st.title("🎧 Music Recommender")

# Create two tabs
tab1, tab2 = st.tabs(["AI Generated", "Mood Based"])

# --- Tab 1: Minor MU Recommendations ---
with tab1:
    st.subheader("AI Generated Recommendation")
    user_input = st.text_area("Enter some lyrics, theme, or text 🎶")

    if st.button("Get Mood Based Recommendations", key="minor_mu_btn"):
        if user_input.strip():
            recs = get_text_recommendations(user_input)
            if recs:
                st.write("### Suggested Tracks:")
                for r in recs:
                    st.write(f"🎵 {r}")
            else:
                st.warning("No recommendations found.")
        else:
            st.warning("Please enter some text.")

# --- Tab 2: GSJ Recommendations ---
with tab2:
    st.subheader(" Mood-based Recommendations")
    mood = st.text_input("Enter your mood (e.g., happy, sad, calm, energetic)")

    if st.button("Get GSJ Recommendations", key="gsj_btn"):
        if mood.strip():
            results = gsj_recommend(mood)
            if results:
                st.write("### Suggested YouTube Songs:")
                for r in results:
                    st.markdown(f"🎵 [{r['title']}]({r['url']})")
            else:
                st.warning("No GSJ recommendations found.")
        else:
            st.warning("Please enter your mood.")
