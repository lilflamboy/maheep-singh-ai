import os
import re
import time
import urllib.parse
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Maheep Singh AI | WhatsApp Roast & Comebacks",
    page_icon="🕶️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, modern, mobile-friendly WhatsApp-themed styling
st.markdown(
    """
    <style>
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 820px;
    }

    /* WhatsApp header simulation */
    .wa-header {
        background: linear-gradient(135deg, #075E54 0%, #128C7E 100%);
        color: white;
        padding: 18px 22px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px rgba(7, 94, 84, 0.2);
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .wa-avatar {
        font-size: 38px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 50%;
        width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .wa-title-box h1 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2;
    }
    .wa-subtitle {
        color: #E0F2F1;
        font-size: 0.85rem;
        margin-top: 4px;
        opacity: 0.95;
    }

    /* WhatsApp Bubble Card */
    .joke-card {
        background: #F0F4F2;
        border-left: 5px solid #25D366;
        border-radius: 12px;
        padding: 16px 18px 12px 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.15s ease-in-out;
    }
    .joke-card:hover {
        transform: translateY(-2px);
    }
    .joke-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        color: #075E54;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .joke-number {
        background: #128C7E;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
    }
    .joke-text {
        font-size: 1.05rem;
        line-height: 1.45;
        color: #1F2937;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .joke-footer {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        font-size: 0.75rem;
        color: #6B7280;
        gap: 6px;
    }
    .ticks {
        color: #34B7F1;
        font-weight: bold;
    }

    /* WhatsApp direct share link button */
    .wa-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #25D366;
        color: white !important;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 6px 12px;
        border-radius: 8px;
        text-decoration: none !important;
        transition: background-color 0.2s;
    }
    .wa-btn:hover {
        background-color: #1EBE5D;
        color: white !important;
    }

    /* Quick chip buttons container */
    .sample-tag {
        font-size: 0.8rem;
        color: #4B5563;
        margin-bottom: 6px;
        font-weight: 600;
    }

    /* Streamlit UI tweaks */
    div[data-testid="stCodeBlock"] {
        margin-top: 4px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# System Instruction as strictly required
SYSTEM_INSTRUCTION = """You are a quick-witted, sarcastic Indian cousin in a lively family WhatsApp group, channeling the legendary deadpan, dry wit of comic Maheep Singh. Your job is to write short, punchy, realistic roasts and comebacks. 
Rules:
- Never sound polite, formal, or robotic.
- Avoid cheesy dad jokes, corny puns, or long paragraphs.
- Write like a real 20-something texting in a group chat: use natural phrasing, dry sarcasm, and relatable family dynamics (ghosting, living abroad, duty-free chocolates, not visiting, acting busy).
- Keep each joke under 2 sentences so it hits hard in a WhatsApp chat.
- Output ONLY the 5 numbered jokes without any intro or outro text."""

# ----------------- HELPER: API KEY VALIDATION -----------------
def sanitize_api_key(key: str) -> str:
    """Sanitize API key by stripping quotes, whitespace, and copy-paste prefixes."""
    if not key:
        return ""
    cleaned = key.strip()
    if cleaned.startswith("GEMINI_API_KEY="):
        cleaned = cleaned.replace("GEMINI_API_KEY=", "", 1).strip()
    cleaned = cleaned.strip("\"' \t\r\n")
    return cleaned

def validate_api_key(key: str) -> tuple[bool, str]:
    """Validate API key format and ensure it doesn't contain non-ASCII characters or copied error text."""
    cleaned = sanitize_api_key(key)
    if not cleaned:
        return False, "API Key is empty. Please enter your Gemini API key in the sidebar."
    
    # Check for non-ASCII characters (which cause 'ascii' codec can't encode errors in HTTP headers)
    try:
        cleaned.encode("ascii")
    except UnicodeEncodeError:
        return False, "The API Key contains invalid characters (e.g. emojis or accidental error text). Please copy and paste ONLY your actual Gemini API key starting with AIzaSy."
    
    if len(cleaned) < 20:
        return False, "The API Key appears incomplete or too short. A standard Gemini key starts with 'AIzaSy' and is ~39 characters."
    
    return True, ""

@st.cache_data(show_spinner=False, ttl=300)
def get_supported_models(api_key: str) -> list[str]:
    """Fetch live list of supported generation models for this API key, excluding retired models."""
    default_models = ["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-2.0-flash", "gemini-1.5-flash"]
    if not api_key:
        return default_models
    try:
        client = genai.Client(api_key=api_key)
        discovered = []
        for m in client.models.list():
            model_id = (m.name or "").replace("models/", "").strip()
            # Skip non-text or deprecated models
            if not model_id or "gemini" not in model_id:
                continue
            if any(skip in model_id for skip in ["embed", "imagen", "veo", "aqa", "bison", "2.5-flash", "2.5-pro"]):
                continue
            discovered.append(model_id)
        if discovered:
            preferred_order = ["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-2.0-flash", "gemini-1.5-flash"]
            sorted_models = [p for p in preferred_order if p in discovered]
            for d in discovered:
                if d not in sorted_models:
                    sorted_models.append(d)
            if sorted_models:
                return sorted_models
    except Exception:
        pass
    return default_models

# ----------------- SIDEBAR: API KEY CONFIG -----------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check Streamlit Cloud Secrets first, then local .env
    cloud_secret = ""
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            cloud_secret = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    env_api_key = sanitize_api_key(cloud_secret or os.getenv("GEMINI_API_KEY", ""))
    
    if env_api_key:
        source_label = "Cloud Secrets" if cloud_secret else "`.env`"
        st.success(f"🔑 API Key loaded from {source_label}")
        user_api_key = st.text_input(
            "Override Gemini API Key (Optional)",
            value="",
            type="password",
            placeholder="Paste another key to override...",
            help="Leave blank to use the pre-configured key."
        )
        active_api_key = sanitize_api_key(user_api_key if user_api_key.strip() else env_api_key)
    else:
        st.warning("⚠️ No API key found in `.env` or Secrets")
        raw_input_key = st.text_input(
            "Paste Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Get your free key from Google AI Studio (aistudio.google.com)"
        )
        active_api_key = sanitize_api_key(raw_input_key)
    
    # Real-time visual feedback if an invalid key or error text was pasted
    if active_api_key:
        is_valid_key, val_err = validate_api_key(active_api_key)
        if not is_valid_key:
            st.error(f"⚠️ {val_err}")
        else:
            st.caption("✅ Key format looks good!")
    
    st.markdown("---")
    st.markdown("### 🤖 Model Info")
    available_models = get_supported_models(active_api_key)
    selected_model = st.selectbox(
        "Gemini Model",
        options=available_models,
        index=0,
        help="Active models recommended by Google. If a model experiences high demand (503), the app automatically switches to another available model."
    )
    st.info(f"**Model:** `{selected_model}`\n\n**SDK:** `google-genai` official")
    
    with st.expander("💡 Need a Gemini API Key?"):
        st.markdown(
            """
            1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
            2. Click **Create API Key**.
            3. Paste it here or save it inside the `.env` file as:
               `GEMINI_API_KEY=your_key_here`
            """
        )
    
    st.markdown("---")
    st.caption("🕶️ **Maheep Singh AI** — Pure deadpan sarcasm & savage WhatsApp comebacks.")

# ----------------- HEADER -----------------
st.markdown(
    """
    <div class="wa-header">
        <div class="wa-avatar">🕶️</div>
        <div class="wa-title-box">
            <h1>Maheep Singh AI</h1>
            <div class="wa-subtitle">WhatsApp Banter & Comeback Generator • "Tension kyu le rahe ho... Mummy se baat karau?"</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "Channel the legendary deadpan sarcasm of **Maheep Singh** in your family WhatsApp group. Generate savage roasts, clever comebacks, or dramatic Indian family guilt trips ready to copy-paste."
)

# ----------------- QUICK SAMPLE CHIPS -----------------
SAMPLE_CONTEXTS = {
    "🇨🇦 Canada Ghosting": "Cousin living in Canada hasn't replied in 3 months but posts Instagram stories every day.",
    "🤖 Called Joke ChatGPT": "Another cousin called my funny meme or joke generated by ChatGPT.",
    "💍 Rishta/Marriage Pressure": "Aunties asking when I am getting married at a family function.",
    "🍫 No Duty-Free Chocolates": "Cousin returned from an abroad trip with zero duty-free chocolates for anyone.",
    "💼 Corporate 14-hr Hustle": "Cousin bragging in the group about working 14 hours a day at their corporate job."
}

st.markdown('<div class="sample-tag">💡 Quick Inspiration (Click to load):</div>', unsafe_allow_html=True)
chip_cols = st.columns(len(SAMPLE_CONTEXTS))
for col, (label, sample_text) in zip(chip_cols, SAMPLE_CONTEXTS.items()):
    if col.button(label, use_container_width=True):
        st.session_state["target_context"] = sample_text

default_text = st.session_state.get(
    "target_context",
    "Cousin living in Canada hasn't replied in the group for 3 months but watches every Instagram story."
)

# ----------------- MAIN INPUTS -----------------
target_context = st.text_area(
    "🎯 Target / Context (What happened?):",
    value=default_text,
    height=100,
    placeholder="e.g., Cousin living in Canada hasn't replied in 3 months, or Sharma Ji's son got an award..."
)

col1, col2 = st.columns(2)

with col1:
    roast_style = st.selectbox(
        "🎭 Roast Style:",
        options=[
            "Savage Roast (No mercy, brutal family banter)",
            "Witty Comeback (Quick, clever clapbacks)",
            "Light Teasing (Playful, safe for parents in the group)",
            "Emotional Blackmail (Dramatic Indian family style)"
        ],
        index=0
    )

with col2:
    vibe_choice = st.radio(
        "🗣️ Language / Vibe:",
        options=[
            "English",
            "Hinglish (Natural Indian mix)",
            "Short One-Liners"
        ],
        horizontal=True,
        index=1  # Default to Hinglish for natural Indian family WhatsApp flavor
    )

st.markdown("<br>", unsafe_allow_html=True)

# Generate Button
generate_btn = st.button("🔥 Generate Roasts", type="primary", use_container_width=True)

# ----------------- GENERATION LOGIC -----------------
def generate_roasts(api_key: str, context: str, style: str, vibe: str, model_name: str = "gemini-3.8-flash", status_box=None):
    """Call Gemini via google-genai SDK to generate 5 roasts with retry and modern model cascade."""
    client = genai.Client(api_key=api_key)
    
    user_prompt = f"""Target / Context:
{context}

Desired Roast Style:
{style}

Desired Language / Vibe:
{vibe}

Please generate exactly 5 numbered roasts/comebacks (1. to 5.).
Remember:
- Keep each joke under 2 sentences.
- Match the selected style ({style}) and vibe ({vibe}).
- If Hinglish: use natural, authentic colloquial Indian group-chat Hinglish.
- If Short One-Liners: keep them exceptionally crisp and sharp.
- Return ONLY the 5 numbered jokes without any introduction, headers, or concluding remarks."""

    # Modern, non-deprecated fallback models
    fallback_pool = ["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-2.0-flash", "gemini-1.5-flash"]
    candidate_models = [model_name]
    for m in fallback_pool:
        if m not in candidate_models:
            candidate_models.append(m)

    quota_hit = False
    last_error = None
    for model in candidate_models:
        if status_box:
            status_box.write(f"⚡ Trying model: `{model}`...")
        # Up to 2 attempts per model for temporary 503 spikes
        for attempt in range(2):
            try:
                # Fast generation config (disabling reasoning delay via thinking_budget=0)
                try:
                    fast_config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.9,
                        max_output_tokens=600,
                        thinking_config=types.ThinkingConfig(thinking_budget=0)
                    )
                    response = client.models.generate_content(
                        model=model,
                        contents=user_prompt,
                        config=fast_config
                    )
                except Exception as config_err:
                    standard_config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.9,
                        max_output_tokens=600
                    )
                    response = client.models.generate_content(
                        model=model,
                        contents=user_prompt,
                        config=standard_config
                    )
                
                # Check for safety blocks
                if response and not response.text:
                    if hasattr(response, "candidates") and response.candidates:
                        finish_reason = getattr(response.candidates[0], "finish_reason", "")
                        if "SAFETY" in str(finish_reason):
                            raise RuntimeError("Google AI safety guidelines declined this prompt. Jokes targeting recent deaths, grief, or personal bereavement are restricted. Please choose relatable family banter topics (ghosting, weddings, borrowed money) instead.")
                
                if response and response.text:
                    return response.text, model
            except Exception as e:
                err_str = str(e)
                last_error = e
                # Check for 503 (UNAVAILABLE / High Demand)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    if attempt == 0:
                        if status_box:
                            status_box.write(f"⏳ `{model}` busy (high traffic), pausing 2s...")
                        time.sleep(2.0)
                        continue
                    else:
                        break  # Move to next candidate model
                # Check for 429 (RESOURCE_EXHAUSTED / Quota limit reached)
                elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    quota_hit = True
                    if status_box:
                        status_box.write(f"⚠️ Daily quota reached on `{model}`. Switching to backup model...")
                    break  # Move to next candidate model immediately
                # Check for 404 (NOT_FOUND / Model unavailable)
                elif "404" in err_str or "NOT_FOUND" in err_str:
                    break  # Move to next candidate model immediately
                else:
                    raise e

    if quota_hit:
        raise RuntimeError(
            "Daily free quota (20 requests/day) reached for this Google Cloud project. "
            "To keep testing for free right now, visit https://aistudio.google.com/app/apikey, click 'Create API key in NEW project', and paste the new key into the sidebar!"
        )
    if last_error:
        raise last_error
    raise RuntimeError("Unable to generate roasts right now due to server capacity. Please wait a few moments and try again.")

def parse_jokes(raw_text: str):
    """Parse 5 numbered jokes from model response."""
    lines = raw_text.strip().split("\n")
    jokes = []
    current_joke = ""
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        # Check if line starts with a number like "1.", "1)", "1 -", etc.
        match = re.match(r"^(\d+)[\.\)\-:\s]+(.*)", cleaned_line)
        if match:
            if current_joke:
                jokes.append(current_joke.strip())
            current_joke = match.group(2).strip()
        else:
            if current_joke:
                current_joke += " " + cleaned_line
            else:
                current_joke = cleaned_line
                
    if current_joke:
        jokes.append(current_joke.strip())
        
    # If regex parsing didn't find clear numbered items, fallback to non-empty lines
    if len(jokes) < 2:
        fallback = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
        if len(fallback) >= 2:
            jokes = fallback
            
    return jokes[:5]

# ----------------- OUTPUT SECTION -----------------
if generate_btn:
    is_valid_key, val_err = validate_api_key(active_api_key)
    if not is_valid_key:
        st.error(f"🔑 **Gemini API Key Issue:** {val_err}")
    elif not target_context.strip():
        st.warning("⚠️ Please provide some context so Maheep Singh AI can roast them properly!")
    else:
        with st.status("💭 Channeling peak Maheep Singh deadpan sarcasm...", expanded=True) as status_box:
            try:
                raw_output, model_used = generate_roasts(
                    api_key=active_api_key,
                    context=target_context,
                    style=roast_style,
                    vibe=vibe_choice,
                    model_name=selected_model,
                    status_box=status_box
                )
                jokes = parse_jokes(raw_output)
                
                # Save into session state
                st.session_state["generated_jokes"] = jokes
                st.session_state["raw_output"] = raw_output
                st.session_state["last_style"] = roast_style
                st.session_state["last_vibe"] = vibe_choice
                st.session_state["last_model"] = model_used

                status_box.update(label="🔥 Roasts generated successfully!", state="complete", expanded=False)

                if model_used != selected_model:
                    st.toast(f"⚡ High traffic on `{selected_model}`, successfully generated using `{model_used}`!")
            except Exception as e:
                status_box.update(label="❌ Generation failed", state="error", expanded=True)
                st.error(f"Error communicating with Gemini API: {str(e)}")

# Display generated jokes if available
if "generated_jokes" in st.session_state and st.session_state["generated_jokes"]:
    jokes = st.session_state["generated_jokes"]
    style_label = st.session_state.get("last_style", roast_style).split("(")[0].strip()
    vibe_label = st.session_state.get("last_vibe", vibe_choice)
    
    st.markdown("---")
    st.subheader(f"💬 Fresh Roasts ({style_label} • {vibe_label})")
    st.caption("Click the copy icon in any box to copy to clipboard, or tap 'Send to WhatsApp' to open directly.")
    
    for idx, joke in enumerate(jokes, 1):
        # WhatsApp web link for instant sharing
        encoded_joke = urllib.parse.quote(joke)
        wa_url = f"https://api.whatsapp.com/send?text={encoded_joke}"
        
        st.markdown(
            f"""
            <div class="joke-card">
                <div class="joke-header">
                    <span class="joke-number">Option #{idx}</span>
                    <span>Family Chat • Sent</span>
                </div>
                <div class="joke-text">{joke}</div>
                <div class="joke-footer">
                    <span>Just now</span>
                    <span class="ticks">✓✓</span>
                    &nbsp;|&nbsp;
                    <a href="{wa_url}" target="_blank" class="wa-btn">📲 Send via WhatsApp</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Native Streamlit code block with built-in 1-click copy button
        st.code(joke, language=None)
    
    # Bonus: Copy all at once
    all_jokes_text = "\n\n".join([f"{i+1}. {j}" for i, j in enumerate(jokes)])
    with st.expander("📋 Copy All 5 Jokes at Once"):
        st.code(all_jokes_text, language=None)
