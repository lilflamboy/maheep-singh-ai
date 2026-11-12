# 🕶️ Maheep Singh AI

A witty, deadpan WhatsApp group comeback and roast generator inspired by the legendary comic **Maheep Singh** (*"Tension kyu le rahe ho... Mummy se baat karau?"*). Built with **Python**, **Streamlit**, and the official **`google-genai`** SDK powered by **`gemini-3.8-flash`**.

---

## 🚀 Features

- **WhatsApp Chat Aesthetic**: Clean, responsive, mobile-friendly design resembling real WhatsApp messages (delivery ticks, message bubbles, green accents).
- **Target / Context Input**: Enter what your cousin or family member did (e.g. ghosting from Canada, calling your joke ChatGPT, boasting about work, or rishta aunties).
- **Quick Inspiration Buttons**: 1-click preset scenarios for instant banter.
- **4 Roast Styles**:
  1. *Savage Roast* (No mercy, brutal family banter)
  2. *Witty Comeback* (Quick, clever clapbacks)
  3. *Light Teasing* (Playful, safe for parents in the group)
  4. *Emotional Blackmail* (Dramatic Indian family style)
- **3 Language / Vibe Modes**:
  1. *English*
  2. *Hinglish (Natural Indian mix)*
  3. *Short One-Liners*
- **1-Click Copy & Direct WhatsApp Sharing**:
  - Built-in copy icon on every joke box.
  - Direct `📲 Send via WhatsApp` link to open WhatsApp with the roast pre-filled.
  - Expandable `Copy All 5 Jokes at Once` block.
- **Flexible API Key Management**: Loads automatically from `.env` or can be pasted/overridden in the sidebar.

---

## 🛠️ Project Structure

```
jokeapi/
├── .env                  # API Key configuration
├── requirements.txt      # Python dependencies
├── app.py                # Main Streamlit application
└── README.md             # Documentation
```

---

## 📦 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Add your Gemini API Key in the `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Alternatively, enter it directly into the app sidebar at runtime.)*

### 3. Launch the Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.
