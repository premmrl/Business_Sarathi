import streamlit as st
import pandas as pd
import requests
import json
import time

st.set_page_config(
    page_title="AI Business Sarathi | Vighnaharta Gold Foundation",
    layout="wide",
    page_icon="🤝",
    initial_sidebar_state="collapsed"
)

# गुगल फॉर्म सबमिशन लिंक
FORM_SUBMIT_URL = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/formResponse"
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/viewform?usp=sharing"

# भारतातील प्रमुख १० भाषांची रचना
LANG_DATA = {
    "मराठी": {
        "foundation": "🏛️ विघ्नहर्ता गोल्ड फाउंडेशनचा उपक्रम",
        "title": "🤝 AI Business Sarathi",
        "caption": "उद्योजकांना अचूक संदर्भ व व्यावसायिक सहकार्य मिळवून देणारा डिजिटल साथीदार",
        "menu_opt": ["🔍 स्मार्ट शोध", "📝 नवीन नोंदणी", "🎙️ पिच व स्टिम्युलेशन"],
        "auth_label": "नोंदणीकृत १० अंकी मोबाईल नंबर किंवा ईमेल:",
        "input_placeholder": "उदा. 8087699949 किंवा email",
        "welcome": "✅ स्वागत आहे, **{name}**!",
        "not_registered": "⚠️ हा नंबर डिरेक्टरीमध्ये नोंदणीकृत नाही.",
        "register_prompt": "👉 संदर्भ शोधण्यासाठी आधी तुमची नोंदणी पूर्ण करा:",
        "register_btn_text": "📝 येथे क्लिक करून १ मिनिटात नोंदणी करा",
        "search_label": "तुम्हाला कोणत्या व्यवसायाशी/सेवेशी जोडले जायचे आहे?",
        "search_placeholder": "उदा. 'पुण्यात सोन्यात गुंतवणुकीसाठी संपर्क'...",
        "search_hint": "💡 संदर्भ शोधण्यासाठी वर नोंदणीकृत नंबर टाकून बाणावर (➔) दाबा.",
        "spinner_search": "AI अचूक संदर्भ शोधत आहे...",
        "reg_title": "बिझनेस नेटवर्कमध्ये नवीन सदस्य नोंदणी",
        "reg_name": "पूर्ण नाव (Full Name):",
        "reg_comp": "कंपनी / ब्रँडचे नाव (Company Name):",
        "reg_phone": "मोबाईल / व्हॉट्सॲप नंबर (Mobile / WhatsApp):",
        "reg_email": "ईमेल आयडी (Email ID):",
        "reg_city": "शहर (City / Location):",
        "reg_serv": "मुख्य उत्पादने किंवा सेवा (Products / Services):",
        "reg_btn": "नोंदणी पूर्ण करा ➔",
        "reg_success": "🎉 अभिनंदन! तुमची नोंदणी यशस्वी झाली आहे. आता '🔍 स्मार्ट शोध' मेनू निवडून संदर्भ शोधा.",
        "pitch_title": "३०-सेकंद पिच व स्टिम्युलेशन जनरेटर",
        "pitch_comp": "तुमची कंपनी / ब्रँड:",
        "pitch_serv": "मुख्य उत्पादने किंवा सेवा:",
        "pitch_stim": "स्टिम्युलेशन / ट्रिगर थीम (ऐच्छिक):",
        "pitch_stim_hint": "उदा. 'सोने महाग झाले आहे', 'मुलीच्या लग्नासाठी सोन्याचे नियोजन'",
        "pitch_ask": "या आठवड्यात कोणाशी कनेक्ट व्हायचे आहे (Ask)?",
        "pitch_btn": "प्रभावी पिच व स्टिम्युलेशन बनवा ➔",
        "spinner_pitch": "पिच तयार होत आहे...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्योजकांच्या सशक्तीकरणासाठी व नेटवर्किंगसाठी कार्यरत आहे.",
        "footer": "संकल्पना व निर्मिती: विघ्नहर्ता गोल्ड फाउंडेशन | अधिक माहितीसाठी:"
    },
    "हिंदी": {
        "foundation": "🏛️ विघ्नहर्ता गोल्ड फाउंडेशन की पहल",
        "title": "🤝 AI Business Sarathi",
        "caption": "उद्यमियों को सटीक रेफ़रल व व्यावसायिक सहयोग दिलाने वाला डिजिटल साथी",
        "menu_opt": ["🔍 स्मार्ट सर्च", "📝 नया पंजीकरण", "🎙️ पिच व स्टिम्युलेशन"],
        "auth_label": "पंजीकृत 10 अंकों का मोबाइल नंबर या ईमेल:",
        "input_placeholder": "उदा. 8087699949 या email",
        "welcome": "✅ स्वागत है, **{name}**!",
        "not_registered": "⚠️ यह नंबर डायरेक्टरी में पंजीकृत नहीं है।",
        "register_prompt": "👉 रेफ़रल खोजने के लिए पहले अपना पंजीकरण पूरा करें:",
        "register_btn_text": "📝 यहाँ क्लिक करके 1 मिनट में पंजीकरण करें",
        "search_label": "आप किस व्यवसाय या सेवा से जुड़ना चाहते हैं?",
        "search_placeholder": "उदा. 'मुझे पुणे में सोने में निवेश के लिए संपर्क'...",
        "search_hint": "💡 रेफ़रल खोजने के लिए ऊपर अपना पंजीकृत नंबर डालकर ➔ दबाएं।",
        "spinner_search": "AI उपयुक्त रेफ़रल खोज रहा है...",
        "reg_title": "बिजनेस नेटवर्क में नया सदस्य पंजीकरण",
        "reg_name": "पूरा नाम (Full Name):",
        "reg_comp": "कंपनी / ब्रांड का नाम (Company Name):",
        "reg_phone": "मोबाइल / व्हाट्सएप नंबर (Mobile / WhatsApp):",
        "reg_email": "ईमेल आईडी (Email ID):",
        "reg_city": "शहर (City / Location):",
        "reg_serv": "मुख्य उत्पाद या सेवाएं (Products / Services):",
        "reg_btn": "पंजीकरण पूरा करें ➔",
        "reg_success": "🎉 बधाई! आपका पंजीकरण सफल हो गया है। अब '🔍 स्मार्ट सर्च' में जाकर खोजें।",
        "pitch_title": "30-सेकंड पिच और स्टिम्युलेशन जनरेटर",
        "pitch_comp": "कंपनी / ब्रांड:",
        "pitch_serv": "मुख्य उत्पाद या सेवाएं:",
        "pitch_stim": "स्टिम्युलेशन / ट्रिगर थीम (वैकल्पिक):",
        "pitch_stim_hint": "उदा. 'सोना महंगा हो गया है'",
        "pitch_ask": "इस सप्ताह आपकी क्या आवश्यकता है (Ask)?",
        "pitch_btn": "पिच और स्टिम्युलेशन तैयार करें ➔",
        "spinner_pitch": "पिच तैयार हो रही है...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्यमियों के सशक्तिकरण और नेटवर्किंग के लिए समर्पित है।",
        "footer": "संकल्पना एवं निर्माण: विघ्नहर्ता गोल्ड फाउंडेशन | वेबसाइट:"
    },
    "English": {
        "foundation": "🏛️ An Initiative by Vighnaharta Gold Foundation",
        "title": "🤝 AI Business Sarathi",
        "caption": "Connecting entrepreneurs with precise referrals and business collaborations",
        "menu_opt": ["🔍 Smart Search", "📝 New Registration", "🎙️ Pitch & Stimulation"],
        "auth_label": "Registered 10-digit mobile number or email:",
        "input_placeholder": "e.g. 8087699949 or email",
        "welcome": "✅ Welcome, **{name}**!",
        "not_registered": "⚠️ This contact is not registered in our directory.",
        "register_prompt": "👉 To access referrals, please complete your registration first:",
        "register_btn_text": "📝 Click here to register in 1 minute",
        "search_label": "Which business or service are you looking to connect with?",
        "search_placeholder": "e.g. 'Looking for gold investment advisor'...",
        "search_hint": "💡 Please enter your registered contact above and tap ➔ arrow.",
        "spinner_search": "AI is finding the best matches...",
        "reg_title": "Register Business in Directory",
        "reg_name": "Full Name:",
        "reg_comp": "Company / Brand Name:",
        "reg_phone": "Mobile / WhatsApp Number:",
        "reg_email": "Email ID:",
        "reg_city": "City / Location:",
        "reg_serv": "Core Products or Services:",
        "reg_btn": "Submit Registration ➔",
        "reg_success": "🎉 Congratulations! Registration complete. You can now use '🔍 Smart Search'.",
        "pitch_title": "30-Sec Pitch & Stimulation Generator",
        "pitch_comp": "Company / Brand:",
        "pitch_serv": "Core Products or Services:",
        "pitch_stim": "Stimulation / Trigger Theme (Optional):",
        "pitch_stim_hint": "e.g. 'Gold price rise', 'Retirement savings'",
        "pitch_ask": "Who do you want to connect with this week (Ask)?",
        "pitch_btn": "Generate Pitch & Stimulation ➔",
        "spinner_pitch": "Crafting pitch...",
        "about": "Vighnaharta Gold Foundation empowers businesses through financial literacy and networking.",
        "footer": "Conceptualized & Developed by Vighnaharta Gold Foundation | Visit:"
    }
}

# मराठी, हिंदी, इंग्रजीव्यतिरिक्त उर्वरित भाषांसाठी डिफॉल्ट इंग्लिश मॅपिंग
for l_key in ["ગુજરાતી", "தமிழ்", "తెలుగు", "ಕನ್ನಡ", "മലയാളം", "বাংলা", "ਪੰਜਾਬੀ"]:
    if l_key not in LANG_DATA:
        LANG_DATA[l_key] = LANG_DATA["English"]

# CSS स्टायलिंग
st.markdown("""
    <style>
        .block-container {
            padding-top: 2.2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
            max-width: 750px;
        }
        .app-header {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #d4af37;
            padding: 14px;
            border-radius: 14px;
            margin-bottom: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        .app-foundation {
            font-size: 0.92rem;
            color: #d4af37;
            font-weight: 700;
            margin-bottom: 3px;
        }
        .app-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            margin: 2px 0;
        }
        .app-caption {
            font-size: 0.78rem;
            color: #94a3b8;
        }
        /* नेव्हिगेशन मेनू अधिक स्पष्ट व मोबाईलवर सोपा करणे */
        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            justify-content: space-around !important;
            background: #1e293b !important;
            padding: 8px !important;
            border-radius: 10px !important;
            border: 1px solid #334155 !important;
            margin-bottom: 15px !important;
        }
        div[role="radiogroup"] label {
            background: transparent !important;
            padding: 6px 10px !important;
            border-radius: 6px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
        }
        .app-footer {
            text-align: center;
            color: #64748b;
            font-size: 0.78rem;
            margin-top: 25px;
            padding-top: 12px;
            border-top: 1px solid #334155;
        }
    </style>
""", unsafe_allow_html=True)

# भाषा निवड
languages = list(LANG_DATA.keys())
c_l1, c_l2 = st.columns([6, 4], vertical_alignment="center")
with c_l2:
    selected_lang = st.selectbox("🌐 भाषा / Language:", options=languages, index=0)

t = LANG_DATA[selected_lang]
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Google Sheet लोड
SHEET_ID = "1WibJTWH8NeHrESLNF24im10uAoF1GR3uRgnUhFmZQFE"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=15)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df.fillna("")
    except Exception:
        return pd.DataFrame()

df = load_data()

# Gemini API कॉल
def call_gemini(prompt_text, api_key):
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    available_models = ["gemini-2.5-flash", "gemini-flash-latest"]
    for m in available_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=25)
            if r.status_code == 200:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            elif r.status_code == 503:
                time.sleep(1)
                continue
        except Exception:
            continue
    return "सर्व्हर सध्या व्यस्त आहे. कृपया पुन्हा प्रयत्न करा."

# हेडर कार्ड
st.markdown(f"""
    <div class="app-header">
        <div class="app-foundation">{t['foundation']}</div>
        <div class="app-title">{t['title']}</div>
        <div class="app-caption">{t['caption']}</div>
    </div>
""", unsafe_allow_html=True)

# स्टेट मॅनेजमेंट
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "active_nav" not in st.session_state:
    st.session_state.active_nav = t["menu_opt"][0]

# नेव्हिगेशन मेनू (टॅब अडकण्याची समस्या कायमस्वरूपी बंद)
active_page = st.radio(
    "Navigation",
    options=t["menu_opt"],
    index=t["menu_opt"].index(st.session_state.active_nav) if st.session_state.active_nav in t["menu_opt"] else 0,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.active_nav = active_page

st.markdown("---")

# १. स्मार्ट शोध
if active_page == t["menu_opt"][0]:
    st.markdown(f"**{t['auth_label']}**")
    
    col_in, col_btn = st.columns([8, 2], vertical_alignment="bottom")
    with col_in:
        user_contact = st.text_input(
            label=t["auth_label"],
            placeholder=t["input_placeholder"],
            label_visibility="collapsed",
            key="user_contact_input"
        )
    with col_btn:
        submit_login = st.button("➔", key="btn_login_arrow", type="primary", use_container_width=True)

    if (submit_login or user_contact) and user_contact:
        contact_str = str(user_contact).strip().lower()
        mask = df.apply(lambda row: row.astype(str).str.strip().str.lower().str.contains(contact_str, regex=False), axis=1)
        matches = df[mask.any(axis=1)]
        
        if not matches.empty:
            st.session_state.logged_in_user = matches.iloc[0]
        else:
            st.session_state.logged_in_user = None
            st.warning(t["not_registered"])
            st.info(t["register_prompt"])
            if st.button(t["register_btn_text"], type="secondary", use_container_width=True):
                st.session_state.active_nav = t["menu_opt"][1]
                st.rerun()

    if st.session_state.logged_in_user is not None:
        name_col = [c for c in df.columns if "नाव" in c or "Name" in c]
        user_name = st.session_state.logged_in_user[name_col[0]] if name_col else "Member"
        st.success(t["welcome"].format(name=user_name))
        
        st.markdown(f"**{t['search_label']}**")
        sc1, sc2 = st.columns([8, 2], vertical_alignment="bottom")
        with sc1:
            query = st.text_input(
                label=t["search_label"],
                placeholder=t["search_placeholder"],
                label_visibility="collapsed",
                key="search_query_input"
            )
        with sc2:
            submit_search = st.button("➔", key="btn_search_arrow", type="primary", use_container_width=True)
            
        if (submit_search or query) and query:
            if not GEMINI_API_KEY:
                st.error("API Key missing.")
            elif df.empty:
                st.warning("Data empty.")
            else:
                with st.spinner(t["spinner_search"]):
                    context_data = df.to_string(index=False)
                    prompt = f"""
                    You are 'AI Business Sarathi', an initiative of Vighnaharta Gold Foundation.
                    Provide a referral match strictly in {selected_lang} language.
                    
                    [Directory Data]:
                    {context_data}
                    
                    [Searching Member Profile]:
                    {st.session_state.logged_in_user.to_dict()}
                    
                    [Requirement]:
                    {query}
                    
                    Rules:
                    1. Respond strictly in {selected_lang}.
                    2. Give matched member's full name, company, city, services, and phone number.
                    3. Clearly explain synergy/how they can benefit each other.
                    4. Professional formatting with clear bullet points.
                    """
                    reply = call_gemini(prompt, GEMINI_API_KEY)
                    st.markdown(reply)
    else:
        if not user_contact:
            st.info(t["search_hint"])

# २. नवीन नोंदणी फॉर्म
elif active_page == t["menu_opt"][1]:
    st.write(f"### {t['reg_title']}")
    
    with st.form("in_app_reg_form", clear_on_submit=False):
        r_name = st.text_input(t["reg_name"])
        r_comp = st.text_input(t["reg_comp"])
        r_phone = st.text_input(t["reg_phone"])
        r_email = st.text_input(t["reg_email"])
        r_city = st.text_input(t["reg_city"])
        r_serv = st.text_area(t["reg_serv"], height=80)
        
        reg_submit = st.form_submit_button(t["reg_btn"], type="primary", use_container_width=True)
        
    if reg_submit:
        if not r_name or not r_phone:
            st.error("⚠️ कृपया नाव आणि मोबाईल नंबर अवश्य प्रविष्ट करा.")
        else:
            with st.spinner("नोंदणी सबमिट होत आहे..."):
                try:
                    payload = {
                        "entry.123456789": r_name,
                        "entry.987654321": r_comp,
                        "entry.555555555": r_phone,
                        "entry.444444444": r_email,
                        "entry.333333333": r_city,
                        "entry.222222222": r_serv
                    }
                    requests.post(FORM_SUBMIT_URL, data=payload, timeout=5)
                except Exception:
                    pass
                
                st.success(t["reg_success"])
                st.balloons()
                st.cache_data.clear()

# ३. पिच व स्टिम्युलेशन
elif active_page == t["menu_opt"][2]:
    st.markdown(f"##### {t['pitch_title']}")
    with st.form("pitch_form", clear_on_submit=False):
        b_name = st.text_input(t["pitch_comp"])
        b_serv = st.text_area(t["pitch_serv"], height=70)
        b_stim = st.text_input(t["pitch_stim"], placeholder=t["pitch_stim_hint"])
        b_ask = st.text_input(t["pitch_ask"])
        submit_pitch = st.form_submit_button(t["pitch_btn"], type="primary")
    
    if submit_pitch:
        if not GEMINI_API_KEY:
            st.error("API Key missing.")
        elif b_name and b_serv:
            with st.spinner(t["spinner_pitch"]):
                pitch_prompt = f"""
                You are an expert executive networking coach for BNI and professional business chapters, under Vighnaharta Gold Foundation.
                Language to respond: {selected_lang}
                
                Input Details:
                - Company / Brand: {b_name}
                - Core Products / Services: {b_serv}
                - Stimulation Theme / Specific Trigger: {b_stim if b_stim else "General customer pain point"}
                - Specific Ask: {b_ask}
                
                Please generate:
                1. **30-Second Speaking Pitch**:
                   - Opening Hook, Core Value, Weekly Ask, Memory Hook Tagline.
                2. **Referral Stimulation / Triggers**:
                   - "When you hear...", "Look for people who...", "How to connect them to me".
                
                Format neatly using clear bullet points in {selected_lang}.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.markdown(pitch_reply)

# तळटीप
st.markdown(f"""
    <div class="app-footer">
        {t['footer']} 
        <a href='https://www.vgold.co.in' target='_blank' style='color: #d4af37; font-weight: 700; text-decoration: none;'>
            www.vgold.co.in
        </a>
    </div>
""", unsafe_allow_html=True)
