# Annadaata.AI prototype UI.  Run:  streamlit run app.py
import streamlit as st
from PIL import Image
import gemini_helper as gh
import disease
import crop

st.set_page_config(page_title="Annadaata.AI", page_icon="🌾")
st.title("🌾 Annadaata.AI")
st.caption("Kerala farming assistant (prototype)")

district = st.sidebar.selectbox(
    "Your district", ["Thiruvananthapuram", "Kollam", "Alappuzha", "Kottayam", "Idukki",
                      "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode",
                      "Wayanad", "Kannur", "Kasaragod", "Pathanamthitta"])
context = f"Farmer is in {district}, Kerala."

tab1, tab2, tab3 = st.tabs(["💬 Ask (Malayalam)", "🍃 Leaf scan", "🌱 Crop advice"])

with tab1:
    q = st.text_area("Ask your question (Malayalam / Manglish / English)")
    if st.button("Ask") and q:
        with st.spinner("Thinking..."):
            st.write(gh.ask_text(q, context))
    voice = st.file_uploader("Or upload a voice note", type=["ogg", "mp3", "wav", "m4a"])
    if voice and st.button("Answer my voice note"):
        mime = voice.type or "audio/ogg"
        with st.spinner("Listening..."):
            st.write(gh.ask_audio(voice.read(), mime, context))

with tab2:
    photo = st.file_uploader("Upload a leaf photo", type=["jpg", "jpeg", "png"])
    if photo:
        img = Image.open(photo)
        st.image(img, width=300)
        if st.button("Diagnose"):
            with st.spinner("Scanning..."):
                if disease.model_ready():
                    name, conf = disease.predict(img)
                    st.write(f"**Result:** {name}  ({conf:.0%} confident)")
                    if conf < disease.CONFIDENCE_LIMIT:
                        st.warning("Not sure. Please contact your nearest Krishi Bhavan.")
                    else:
                        st.write(gh.explain_disease(name, conf, context))
                else:
                    st.info("CNN not trained yet, using Gemini vision as backup.")
                    st.write(gh.diagnose_with_gemini_vision(img))

with tab3:
    st.write("Enter soil and weather details")
    c1, c2 = st.columns(2)
    n = c1.number_input("Nitrogen (N)", 0, 150, 50)
    p = c1.number_input("Phosphorus (P)", 0, 150, 50)
    k = c1.number_input("Potassium (K)", 0, 210, 50)
    ph = c1.number_input("Soil pH", 3.0, 10.0, 6.0)
    temp = c2.number_input("Temperature (°C)", 5.0, 45.0, 28.0)
    hum = c2.number_input("Humidity (%)", 10.0, 100.0, 80.0)
    rain = c2.number_input("Rainfall (mm)", 20.0, 300.0, 200.0)
    if st.button("Recommend crop"):
        if not crop.model_ready():
            st.error("Run `python crop.py` first to train the model.")
        else:
            results = crop.recommend(n, p, k, temp, hum, ph, rain)
            for name, score in results:
                st.write(f"**{name}**  ({score:.0%})")
            st.write(gh.ask_text(
                f"Top crop options are {[r[0] for r in results]}. Explain in Malayalam which is best and why.", context))
