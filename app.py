import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="AI Business Sarathi", layout="wide", page_icon="🤝")

# Gemini API Key मिळवणे (Secrets किंवा थेट इनपुट)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    with st.sidebar:
        st.subheader("⚙️ API Configuration")
        GEMINI_API_KEY = st.text_input("Enter Gemini API Key:", type="password")

# Google Sheet CSV दुवा
SHEET_ID = "1WibJTWH8NeHrESLNF24im10uAoF1GR3uRgnUhFmZQFE"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=30)
def load_data():
    try:
        df = pd.read_csv(CSV_URL)
        return df.fillna("")
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# Gemini REST API कॉल (Fallback पर्यायांसह)
def call_gemini(prompt_text, api_key):
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-latest", "gemini-1.5-flash"]
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }
    
    last_error = ""
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_error = response.text
        except Exception as e:
            last_error = str(e)
            
    return f"API त्रुटी: {last_error}"

st.title("🤝 AI Business Sarathi")
st.subheader("Universal Networking & Referral Matcher")
st.caption("सर्व व्यावसायिक आणि नेटवर्किंग समूहांमधील सदस्यांना अचूक संदर्भ (Referrals) मिळवून देणारा डिजिटल साथीदार")

tab1, tab2, tab3 = st.tabs(["🔍 स्मार्ट बिझनेस सर्च", "👥 सर्व सदस्य डिरेक्टरी", "📝 30-Sec Pitch Generator"])

# टॅब १: AI सर्च
with tab1:
    st.write("### तुम्हाला कोणत्या व्यवसायाशी किंवा सेवेशी जोडले जायचे आहे?")
    query = st.text_input("उदा. 'मला पुण्यात सोन्यात गुंतवणुकीसाठी कोणाशी संपर्क साधता येईल?' किंवा 'ज्वेलर्स आणि बिल्डर्सशी कनेक्टेड कोण आहे?'")
    
    if st.button("संदर्भ शोधा", type="primary") and query:
        if not GEMINI_API_KEY:
            st.error("कृपया डाव्या बाजूला किंवा Secrets मध्ये Gemini API Key प्रविष्ट करा.")
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
                
                [वापरकर्त्याची गरज / शोध]:
                {query}
                
                मार्गदर्शक सूचना:
                1. संबंधित सदस्याचे नाव, कंपनीचे नाव, शहर, मुख्य सेवा आणि मोबाईल नंबर ठळकपणे दे.
                2. दोघे एकत्र येऊन एकमेकांना कसा व्यवसाय/फायदा मिळवून देऊ शकतात (Synergy/Collaboration) हे सुचव.
                3. माहिती अत्यंत व्यावसायिक, मराठीत आणि सुटसुटीत बुलेट पॉईंट्समध्ये दे.
                """
                reply = call_gemini(prompt, GEMINI_API_KEY)
                st.markdown(reply)

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
            st.error("कृपया Gemini API Key प्रविष्ट करा.")
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
