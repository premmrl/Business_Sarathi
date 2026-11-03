import streamlit as st
import pandas as pd
import requests
import json
import time

st.set_page_config(page_title="AI Business Sarathi", layout="wide", page_icon="🤝")

# Google Form नोंदणी लिंक
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/viewform?usp=sharing"

# भाषांची शब्दकोश रचना (Translations)
TRANSLATIONS = {
    "मराठी": {
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "सर्व व्यावसायिक आणि नेटवर्किंग समूहांमधील सदस्यांना अचूक संदर्भ (Referrals) मिळवून देणारा डिजिटल साथीदार",
        "tab1": "🔍 स्मार्ट बिझनेस सर्च",
        "tab2": "👥 सर्व सदस्य डिरेक्टरी",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 सदस्य लॉगिन व पडताळणी",
        "auth_caption": "नेटवर्किंगचा लाभ घेण्यासाठी आणि अचूक संदर्भ शोधण्यासाठी तुमची डिरेक्टरीमध्ये नोंदणी असणे आवश्यक आहे.",
        "input_label": "तुमचा नोंदणीकृत १० अंकी मोबाईल नंबर किंवा ईमेल टाका:",
        "input_placeholder": "उदा. 8087699949 किंवा name@gmail.com",
        "welcome": "स्वागत आहे, **{name}**! तुमची नोंदणी सक्रिय आहे.",
        "not_registered": "⚠️ हा मोबाईल नंबर किंवा ईमेल आमच्या डिरेक्टरीमध्ये नोंदणीकृत नाही.",
        "register_prompt": "👉 नेटवर्किंग समूहाचा लाभ घेण्यासाठी आणि इतरांचे संदर्भ मिळवण्यासाठी कृपया आधी खालील १ मिनिटाचा फॉर्म भरून नोंदणी करा:",
        "register_btn": "📝 येथे क्लिक करून १ मिनिटात नोंदणी करा (Google Form)",
        "search_title": "तुम्हाला कोणत्या व्यवसायाशी किंवा सेवेशी जोडले जायचे आहे?",
        "search_placeholder": "उदा. 'मला पुण्यात सोन्यात गुंतवणुकीसाठी कोणाशी संपर्क साधता येईल?' किंवा 'ज्वेलर्स आणि बिल्डर्सशी कनेक्टेड कोण आहे?'",
        "search_btn": "संदर्भ शोधा",
        "search_hint": "💡 संदर्भ शोधण्यासाठी कृपया वर तुमचा नोंदणीकृत मोबाईल नंबर किंवा ईमेल टाका.",
        "spinner_search": "AI डेटाबेसमधून योग्य संदर्भ तपासत आहे...",
        "dir_title": "नोंदणीकृत उद्योजक व व्यावसायिक",
        "filter_placeholder": "नाव, शहर किंवा उद्योगानुसार शोधा:",
        "no_records": "अद्याप कोणतीही नोंद आढळली नाही.",
        "pitch_title": "नेटवर्किंग मिटिंगसाठी 30 किंवा 60 सेकंदांची व्यवसाय ओळख बनवा",
        "pitch_comp": "तुमची कंपनी / ब्रँड:",
        "pitch_serv": "तुमची मुख्य उत्पादने किंवा सेवा:",
        "pitch_ask": "या आठवड्यात तुम्हाला कोणाशी कनेक्ट व्हायचे आहे (Ask)?",
        "pitch_btn": "पिच तयार करा",
        "spinner_pitch": "तुमचा प्रभावी पिच तयार होत आहे...",
        "empty_sheet": "अद्याप शीटमध्ये डेटा उपलब्ध नाही.",
        "no_key": "कृपया Gemini API Key प्रविष्ट करा.",
        "lang_name": "मराठी"
    },
    "हिंदी": {
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "सभी व्यावसायिक और नेटवर्किंग समूहों के सदस्यों को सटीक रेफ़रल दिलाने वाला डिजिटल साथी",
        "tab1": "🔍 स्मार्ट बिज़नेस सर्च",
        "tab2": "👥 सदस्य डायरेक्टरी",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 सदस्य लॉगिन व सत्यापन",
        "auth_caption": "नेटवर्किंग का लाभ उठाने और संदर्भ खोजने के लिए डायरेक्टरी में आपका पंजीकरण होना आवश्यक है।",
        "input_label": "अपना पंजीकृत 10 अंकों का मोबाइल नंबर या ईमेल दर्ज करें:",
        "input_placeholder": "उदा. 8087699949 या name@gmail.com",
        "welcome": "स्वागत है, **{name}**! आपका पंजीकरण सक्रिय है।",
        "not_registered": "⚠️ यह मोबाइल नंबर या ईमेल हमारी डायरेक्टरी में पंजीकृत नहीं है।",
        "register_prompt": "👉 नेटवर्किंग समूह का लाभ उठाने और रेफ़रल खोजने के लिए कृपया नीचे दिए गए 1 मिनट के फॉर्म से पंजीकरण करें:",
        "register_btn": "📝 यहाँ क्लिक करके 1 मिनट में पंजीकरण करें (Google Form)",
        "search_title": "आप किस व्यवसाय या सेवा से जुड़ना चाहते हैं?",
        "search_placeholder": "उदा. 'मुझे पुणे में सोने में निवेश के लिए किससे संपर्क करना चाहिए?' या 'बिल्डर्स से कौन जुड़ा है?'",
        "search_btn": "रेफ़रल खोजें",
        "search_hint": "💡 रेफ़रल खोजने के लिए कृपया ऊपर अपना पंजीकृत मोबाइल नंबर या ईमेल दर्ज करें।",
        "spinner_search": "AI डेटाबेस से उपयुक्त संपर्क खोज रहा है...",
        "dir_title": "पंजीकृत उद्यमी व पेशेवर",
        "filter_placeholder": "नाम, शहर या उद्योग के अनुसार खोजें:",
        "no_records": "अभी कोई रिकॉर्ड उपलब्ध नहीं है।",
        "pitch_title": "नेटवर्किंग मीटिंग के लिए 30 या 60 सेकंड का व्यावसायिक परिचय बनाएं",
        "pitch_comp": "आपकी कंपनी / ब्रांड:",
        "pitch_serv": "आपके मुख्य उत्पाद या सेवाएं:",
        "pitch_ask": "इस सप्ताह आप किससे जुड़ना चाहते हैं (Ask)?",
        "pitch_btn": "पिच तैयार करें",
        "spinner_pitch": "आपकी प्रभावशाली पिच तैयार हो रही है...",
        "empty_sheet": "शीट में डेटा उपलब्ध नहीं है।",
        "no_key": "कृपया Gemini API Key दर्ज करें।",
        "lang_name": "हिंदी"
    },
    "English": {
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "Your AI digital companion connecting entrepreneurs and networking members with precise referrals",
        "tab1": "🔍 Smart Business Search",
        "tab2": "👥 Member Directory",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 Member Login & Verification",
        "auth_caption": "To search referrals and leverage network benefits, your business must be registered in our directory.",
        "input_label": "Enter your registered 10-digit mobile number or email:",
        "input_placeholder": "e.g. 8087699949 or name@gmail.com",
        "welcome": "Welcome, **{name}**! Your registration is active.",
        "not_registered": "⚠️ This mobile number or email is not registered in our directory.",
        "register_prompt": "👉 To access referrals and be a part of the network, please register using the 1-minute form below:",
        "register_btn": "📝 Click here to register in 1 minute (Google Form)",
        "search_title": "Which business or service are you looking to connect with?",
        "search_placeholder": "e.g., 'Looking for gold investment advisor in Pune' or 'Who connects with builders and architects?'",
        "search_btn": "Find Referral",
        "search_hint": "💡 Please enter your registered mobile number or email above to unlock referral search.",
        "spinner_search": "AI is finding the best referral matches from directory...",
        "dir_title": "Registered Entrepreneurs & Professionals",
        "filter_placeholder": "Filter by name, city, or industry:",
        "no_records": "No records found.",
        "pitch_title": "Create a 30 to 60-Second Business Pitch for Networking Meets",
        "pitch_comp": "Your Company / Brand:",
        "pitch_serv": "Your Core Products or Services:",
        "pitch_ask": "Who do you want to connect with this week (Ask)?",
        "pitch_btn": "Generate Pitch",
        "spinner_pitch": "Generating your high-impact pitch...",
        "empty_sheet": "Directory data is not yet available in the sheet.",
        "no_key": "Please provide a valid Gemini API Key.",
        "lang_name": "English"
    }
}

# साइडबार - भाषा निवड व API Key
with st.sidebar:
    st.subheader("🌐 भाषा निवडा / Choose Language")
    selected_lang = st.selectbox(
        "Select Language:",
        options=["मराठी", "हिंदी", "English"],
        index=0
    )
    t = TRANSLATIONS[selected_lang]
    
    st.markdown("---")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    if not GEMINI_API_KEY:
        st.subheader("⚙️ API Configuration")
        GEMINI_API_KEY = st.text_input("Enter Gemini API Key:", type="password")

# Google Sheet CSV दुवा
SHEET_ID = "1WibJTWH8NeHrESLNF24im10uAoF1GR3uRgnUhFmZQFE"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=20)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df.fillna("")
    except Exception:
        return pd.DataFrame()

df = load_data()

# Gemini REST API कॉल फंक्शन
def call_gemini(prompt_text, api_key):
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }
    
    available_models = []
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(list_url, timeout=10)
        if res.status_code == 200:
            m_list = res.json().get("models", [])
            for item in m_list:
                if "generateContent" in item.get("supportedGenerationMethods", []):
                    m_name = item.get("name", "").replace("models/", "")
                    available_models.append(m_name)
    except Exception:
        pass

    if not available_models:
        available_models = ["gemini-3.8-flash", "gemini-3.8-pro", "gemini-2.5-flash", "gemini-flash-latest"]

    for m in available_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=25)
            if r.status_code == 200:
                data = r.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            elif r.status_code == 503:
                time.sleep(1)
                continue
        except Exception:
            continue

    return "Server is busy right now. Please try again in a few moments."

st.title(t["title"])
st.subheader(t["subtitle"])
st.caption(t["caption"])

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

# टॅब १: सर्च
with tab1:
    st.write(f"### {t['auth_title']}")
    st.caption(t["auth_caption"])
    
    user_contact = st.text_input(t["input_label"], placeholder=t["input_placeholder"])
    
    is_registered = False
    user_details = None
    
    if user_contact:
        contact_str = str(user_contact).strip().lower()
        mask = df.apply(lambda row: row.astype(str).str.strip().str.lower().str.contains(contact_str, regex=False), axis=1)
        matches = df[mask.any(axis=1)]
        
        if not matches.empty:
            is_registered = True
            user_details = matches.iloc[0]
            name_col = [c for c in df.columns if "नाव" in c or "Name" in c]
            user_name = user_details[name_col[0]] if name_col else "Member"
            st.success(t["welcome"].format(name=user_name))
        else:
            st.warning(t["not_registered"])
            st.info(t["register_prompt"])
            st.link_button(t["register_btn"], FORM_LINK, type="primary")

    st.markdown("---")
    
    if is_registered:
        st.write(f"### {t['search_title']}")
        query = st.text_input(t["search_title"], placeholder=t["search_placeholder"], label_visibility="collapsed")
        
        if st.button(t["search_btn"], type="primary") and query:
            if not GEMINI_API_KEY:
                st.error(t["no_key"])
            elif df.empty:
                st.warning(t["empty_sheet"])
            else:
                with st.spinner(t["spinner_search"]):
                    context_data = df.to_string(index=False)
                    prompt = f"""
                    You are 'AI Business Sarathi' - a professional networking and business referral guide.
                    Using the business directory data below, provide an exceptionally helpful and structured referral recommendation in {t['lang_name']} language.
                    
                    [Directory Data]:
                    {context_data}
                    
                    [Searching Member Profile]:
                    {user_details.to_dict() if user_details is not None else ""}
                    
                    [User Query / Requirement]:
                    {query}
                    
                    Guidelines:
                    1. Respond strictly in {t['lang_name']}.
                    2. Clearly provide the matched member's full name, company name, city, key services, and contact details.
                    3. Clearly explain how both members can collaborate and benefit each other (Synergy / Collaboration points).
                    4. Keep the output clean, highly professional, and organized with clear bullet points.
                    """
                    reply = call_gemini(prompt, GEMINI_API_KEY)
                    st.markdown(reply)
    else:
        if not user_contact:
            st.info(t["search_hint"])

# टॅब २: सदस्य डिरेक्टरी
with tab2:
    st.write(f"### {t['dir_title']}")
    if not df.empty:
        search_filter = st.text_input(t["filter_placeholder"])
        if search_filter:
            filtered = df[df.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().values, axis=1)]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.info(t["no_records"])

# टॅब ३: 30-सेकंद पिच मेकर
with tab3:
    st.write(f"### {t['pitch_title']}")
    b_name = st.text_input(t["pitch_comp"])
    b_serv = st.text_area(t["pitch_serv"])
    b_ask = st.text_input(t["pitch_ask"])
    
    if st.button(t["pitch_btn"]):
        if not GEMINI_API_KEY:
            st.error(t["no_key"])
        elif b_name and b_serv:
            with st.spinner(t["spinner_pitch"]):
                pitch_prompt = f"""
                Company: {b_name}
                Services: {b_serv}
                Current Ask / Requirement: {b_ask}
                Language: {t['lang_name']}
                
                Generate a confident, high-impact 30 to 60-second business introduction pitch for weekly networking meetings (like BNI / Rotary business meet) in {t['lang_name']}.
                Include an engaging opening, clear core business value, a specific Ask, and a strong call-to-action.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.success(pitch_reply)
