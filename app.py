import streamlit as st
import pandas as pd
import requests
import json
import time

st.set_page_config(page_title="AI Business Sarathi", layout="wide", page_icon="🤝")

# Google Form ची लिंक (येथे तुमची फॉर्म लिंक पेस्ट करा)
FORM_LINK = "https://docs.google.com/forms/d/1hnpUYKjmHuG2kqhWgPldUggED5OZQ8sdmbaDPb_04Kc/viewform"

# Gemini API Key मिळवणे
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    with st.sidebar:
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
    except Exception as e:
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

    return "सर्व्हर सध्या व्यस्त आहे. कृपया पुन्हा प्रयत्न करा."

st.title("🤝 AI Business Sarathi")
st.subheader("Universal Networking & Referral Matcher")
st.caption("सर्व व्यावसायिक आणि नेटवर्किंग समूहांमधील सदस्यांना अचूक संदर्भ (Referrals) मिळवून देणारा डिजिटल साथीदार")

tab1, tab2, tab3 = st.tabs(["🔍 स्मार्ट बिझनेस सर्च", "👥 सर्व सदस्य डिरेक्टरी", "📝 30-Sec Pitch Generator"])

# टॅब १: AI सर्च (Gated Access सह)
with tab1:
    st.write("### 🔐 सदस्य लॉगिन व पडताळणी")
    st.caption("नेटवर्किंगचा लाभ घेण्यासाठी आणि संदर्भ शोधण्यासाठी तुमची नोंदणी असणे आवश्यक आहे.")
    
    user_contact = st.text_input("तुमचा नोंदणीकृत १० अंकी मोबाईल नंबर किंवा ईमेल टाका:", placeholder="उदा. 98XXXXXXXX किंवा name@gmail.com")
    
    is_registered = False
    user_details = None
    
    if user_contact:
        # शीटमधील मोबाईल नंबर किंवा ईमेल कॉलममध्ये तपासणे
        contact_str = str(user_contact).strip().lower()
        
        # शीटमधील सर्व सेल तपासून शोधणे
        mask = df.apply(lambda row: row.astype(str).str.strip().str.lower().str.contains(contact_str, regex=False), axis=1)
        matches = df[mask.any(axis=1)]
        
        if not matches.empty:
            is_registered = True
            user_details = matches.iloc[0]
            # नाव शोधणे
            name_col = [c for c in df.columns if "नाव" in c or "Name" in c]
            user_name = user_details[name_col[0]] if name_col else "उद्योजक मित्र"
            st.success(f"✅ स्वागत आहे, **{user_name}**! तुमची नोंदणी सक्रिय आहे.")
        else:
            st.warning("⚠️ हा मोबाईल नंबर किंवा ईमेल आमच्या डिरेक्टरीमध्ये नोंदणीकृत नाही.")
            st.info(f"👉 नेटवर्किंग समूहाचा लाभ घेण्यासाठी आणि शोध घेण्यासाठी कृपया खालील लिंकवरून आधी नोंदणी करा:")
            st.link_button("📝 येथे क्लिक करून १ मिनिटात नोंदणी करा (Google Form)", FORM_LINK, type="primary")

    st.markdown("---")
    
    # नोंदणीकृत असल्यासच सर्च बॉक्स दिसेल
    if is_registered:
        st.write("### तुम्हाला कोणत्या व्यवसायाशी किंवा सेवेशी जोडले जायचे आहे?")
        query = st.text_input("उदा. 'मला पुण्यात सोन्यात गुंतवणुकीसाठी कोणाशी संपर्क साधता येईल?' किंवा 'ज्वेलर्स आणि बिल्डर्सशी कनेक्टेड कोण आहे?'")
        
        if st.button("संदर्भ शोधा", type="primary") and query:
            if not GEMINI_API_KEY:
                st.error("कृपया Gemini API Key प्रविष्ट करा.")
            elif df.empty:
                st.warning("अद्याप शीटमध्ये डेटा उपलब्ध नाही.")
            else:
                with st.spinner("AI डेटाबेसमधून योग्य संदर्भ तपासत आहे..."):
                    context_data = df.to_string(index=False)
                    prompt = f"""
                    तू 'AI Business Sarathi' आहेस - उद्योजकांसाठीचा नेटवर्किंग आणि संदर्भ मार्गदर्शक.
                    खालील व्यावसायिक डिरेक्टरीचा डेटा वापरून वापरकर्त्याच्या प्रश्नाचे अत्यंत उपयुक्त आणि सकारात्मक उत्तर दे:
                    
                    [डिरेक्टरी डेटा]:
                    {context_data}
                    
                    [शोध घेणारा सदस्य]:
                    {user_details.to_dict() if user_details is not None else ""}
                    
                    [वापरकर्त्याची गरज / शोध]:
                    {query}
                    
                    मार्गदर्शक सूचना:
                    1. संबंधित सदस्याचे नाव, कंपनीचे नाव, शहर, मुख्य सेवा आणि मोबाईल नंबर ठळकपणे दे.
                    2. दोघे एकत्र येऊन एकमेकांना कसा व्यवसाय/फायदा मिळवून देऊ शकतात (Synergy/Collaboration) हे सुचव.
                    3. माहिती अत्यंत व्यावसायिक, मराठीत आणि सुटसुटीत बुलेट पॉईंट्समध्ये दे.
                    """
                    reply = call_gemini(prompt, GEMINI_API_KEY)
                    st.markdown(reply)
    else:
        if not user_contact:
            st.info("💡 संदर्भ शोधण्यासाठी कृपया वर तुमचा नोंदणीकृत मोबाईल नंबर किंवा ईमेल टाका.")

# टॅब २: सदस्य डिरेक्टरी
with tab2:
    st.write("### नोंदणीकृत उद्योजक व व्यावसायिक")
    if not df.empty:
        search_filter = st.text_input("नाव, शहर किंवा उद्योगानुसार शोधा:")
        if search_filter:
            filtered = df[df.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().values, axis=1)]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.info("अद्याप कोणतीही नोंद आढळली नाही.")

# टॅब ३: 30-सेकंद पिच मेकर
with tab3:
    st.write("### नेटवर्किंग मिटिंगसाठी 30 किंवा 60 सेकंदांची व्यवसाय ओळख बनवा")
    b_name = st.text_input("तुमची कंपनी / ब्रँड:")
    b_serv = st.text_area("तुमची मुख्य उत्पादने किंवा सेवा:")
    b_ask = st.text_input("या आठवड्यात तुम्हाला कोणाशी कनेक्ट व्हायचे आहे (Ask)?")
    
    if st.button("पिच तयार करा"):
        if not GEMINI_API_KEY:
            st.error("कृपया Gemini API Key टाका.")
        elif b_name and b_serv:
            with st.spinner("तुमचा प्रभावी पिच तयार होत आहे..."):
                pitch_prompt = f"""
                कंपनी: {b_name}
                सेवा: {b_serv}
                सध्याची आवश्यकता (Ask): {b_ask}
                
                या माहितीच्या आधारे नेटवर्किंग मिटींगसाठी (उदा. BNI / Rotary बिझनेस मीट) ३० सेकंदांचा प्रभावी, आत्मविश्वासू आणि व्यावसायिक मराठी पिच तयार कर.
                शेवटी एक स्पष्ट Call-to-action असावा.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.success(pitch_reply)
