# 🌾 Annadaata.AI

**AI-Powered Personal Farming Assistant for Kerala Farmers**

Smart India Hackathon 2026 · Internal Hackathon, Fergusson College (Autonomous)
**Team ByteCraft** · PS ID: SIH25074 · Theme: Agriculture, FoodTech & Rural Development · Category: Software

**Live demo:** [`(https://annadaataai-bqtxylbix773ucjwkdyfva.streamlit.app/)`]

---

## About the project

Annadaata.AI is a WhatsApp-based AI assistant that gives farmers real-time crop recommendations, instant crop disease diagnosis and voice support in their own language. This project currently focuses on farmers in **Kerala**, with an assistant that replies in **Malayalam**.

Today, farmers often have to visit the Krishi Bhavan in person to get a disease diagnosed, officers are overburdened, and complex apps and portals are hard to use for low-literacy farmers. Annadaata.AI brings that help to the tool farmers already use: WhatsApp.

## Objectives

1. **Bridge the digital literacy gap** with a simple, voice-enabled Malayalam AI assistant.
2. **Reduce crop losses through early detection** by scanning a plant photo with computer vision to identify diseases and suggest treatments.
3. **Provide microclimate-specific crop recommendations** using machine learning models.
4. **Equip rural farmers** with timely, actionable insights to raise productivity and reduce agricultural financial distress.

## Features

| Feature | How it works |
|---|---|
| 💬 Malayalam Q&A (text) | Gemini 2.5 Flash answers farming questions in simple Malayalam |
| 🎤 Voice notes | WhatsApp voice notes are sent to Gemini, which listens and answers |
| 🍃 Leaf disease scan | A CNN (MobileNetV2, trained on PlantVillage) identifies the disease, and Gemini explains treatment and prevention in Malayalam |
| ✅ Confidence check | If the CNN is less than 70% confident, the farmer is referred to the nearest Krishi Bhavan instead of getting unreliable advice |
| 🌱 Crop recommendation | A Random Forest model suggests suitable crops from soil and weather values, and Gemini explains the best option in Malayalam |
| 💚 WhatsApp bot | A Flask webhook connects all of the above to WhatsApp (Twilio sandbox for the prototype) |

## How it works

```
Farmer
 ├── Voice / text query ──► Gemini 2.5 Flash (Malayalam understanding) ─┐
 └── Leaf photo ──► CNN (MobileNetV2) ──► Disease identification ───────┤
                                                                         ▼
                                              Farming AI engine (region, climate, crop context)
                                                                         ▼
                                                              Personalised response
                                                                         ▼
                                                            WhatsApp bot / web app
```

## Tech stack

- **Language:** Python
- **LLM / voice / language:** Google Gemini 2.5 Flash
- **Computer vision:** TensorFlow / Keras, MobileNetV2 transfer learning, PlantVillage dataset
- **Machine learning:** scikit-learn (Random Forest)
- **Web demo:** Streamlit
- **WhatsApp:** Flask webhook with Twilio WhatsApp Sandbox (prototype). The planned production path is the Meta WhatsApp Business API.

## Repository structure

```
├── app.py                    # Streamlit web demo (Ask, Leaf scan, Crop advice)
├── gemini_helper.py          # Gemini text, voice, vision and explanation helpers
├── disease.py                # Loads the CNN and predicts disease with a confidence check
├── train_disease.py          # Trains the CNN locally (data/plantvillage/<class>/*.jpg)
├── colab_train.py            # One-cell script to train the CNN on Google Colab
├── crop.py                   # Trains and runs the crop recommendation model
├── whatsapp_bot.py           # Flask + Twilio WhatsApp webhook
├── disease_model.keras       # Trained CNN
├── class_names.txt           # Disease class names used by the CNN
├── requirements.txt          # Packages for the web app
└── whatsapp_requirements.txt # Extra packages for the WhatsApp bot
```

## Getting started

### 1. Requirements

Python 3.9–3.12 (3.11 recommended, since TensorFlow may not install on newer versions) and a free Gemini API key from Google AI Studio.

### 2. Install

```bash
# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### 3. Add your API key

Create a file named `.env` in the project folder:

```
GEMINI_API_KEY=your_key_here
```

Never commit `.env` to GitHub. On Streamlit Community Cloud, add the key under **Secrets** instead:

```toml
GEMINI_API_KEY = "your_key_here"
```

### 4. Run the web app

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501`. If `disease_model.keras` is missing, the Leaf scan tab falls back to Gemini vision.

## Training the models

### Disease model (CNN)

The model is trained on a subset of PlantVillage (Tomato, Potato, Pepper, Corn, Orange). The easiest way is Google Colab:

1. Open Google Colab and choose **Runtime → Change runtime type → T4 GPU**.
2. Paste the contents of `colab_train.py` into one cell and run it.
3. Download `disease_model.keras` and `class_names.txt` and put them next to `app.py`.

To train locally instead, place the images in `data/plantvillage/<class_name>/` and run `python train_disease.py`.

**Validation accuracy:** `<add your result here>`

### Crop recommendation model

1. Download the Kaggle "Crop Recommendation Dataset" and save it as `data/crop_data.csv` (columns: N, P, K, temperature, humidity, ph, rainfall, label).
2. Run `python crop.py`. This creates `crop_model.joblib`.

## WhatsApp integration (prototype)

1. Create a free Twilio account and join the **WhatsApp Sandbox** from your phone.
2. Add these to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   ```
3. Install and start the bot:
   ```bash
   pip install -r whatsapp_requirements.txt
   python whatsapp_bot.py
   ```
4. Expose it with [ngrok](https://ngrok.com): `ngrok http 5000`.
5. In the Twilio sandbox settings, set **"When a message comes in"** to `https://<your-ngrok-link>/whatsapp` (method POST).
6. Send a Malayalam message, a voice note or a leaf photo to the sandbox number.

Note: the Twilio sandbox only works for phones that have joined it. For real farmers, the plan is to move to the Meta WhatsApp Business API.

## Feasibility and limitations

| Challenge | Mitigation |
|---|---|
| Low digital literacy | WhatsApp-first access: familiar text, voice and image interaction, with no new app to install |
| Regional language and dialects | Malayalam-first prompts tuned for farming terms |
| Real-world data gaps | Modular design with independently testable services (crop advice, disease detection, chat) |
| Prediction reliability | Confidence-based assistance: low confidence leads to an expert referral instead of guidance |

Known limitations of this prototype:

- PlantVillage has no rice, coconut, banana, black pepper or rubber, so the CNN covers only the crops it was trained on. Kerala-specific crop datasets are the next step.
- PlantVillage images are lab-style photos, so accuracy on real field photos will be lower than the validation accuracy.
- The Kaggle crop dataset is not Kerala-specific. Kerala district soil and weather data should replace it.
- Treatment and crop advice come from an AI model. They are guidance, not a replacement for the Krishi Bhavan.

## Impact

| Aspect | Today | With Annadaata.AI |
|---|---|---|
| Disease diagnosis | Farmers visit Krishi Bhavan, delaying treatment | Instant leaf scan with real-time remedies |
| Expert reach | Overburdened officers cannot cover every farm | 24/7 virtual assistant that triages routine queries |
| Digital access | Complex portals and apps | Zero-learning-curve WhatsApp voice interface in Malayalam |
| Yield and planning | Crop choice relies on guesswork | Data-driven crop recommendations for local terrain |

## Roadmap

- [ ] Add Kerala crop datasets (rice, banana, coconut and others) to the CNN
- [ ] Replace the generic crop dataset with Kerala district soil and weather data
- [ ] Move from the Twilio sandbox to the Meta WhatsApp Business API
- [ ] Add live weather data for microclimate-aware advice
- [ ] Field-test with farmers and Krishi Bhavan officers

## Team ByteCraft

- Ritu Sawant
- Gaurav Jagdhane
- Masira Shaikh
- Mahi Joshi
- Gauri Sadafule
- Raj Handique

## References

- Department of Agriculture Development and Farmers' Welfare, Government of Kerala.
- Sherin, P. S., & Haseena, V. A. (2023). *Agriculture Distress and Farmers' Suicide in Kerala in the Globalization Era.* IJAE.
- Meta WhatsApp Business API, Google Gemini 2.5 Flash, PlantVillage dataset.
