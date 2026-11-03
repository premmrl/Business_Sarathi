import streamlit as st
import pandas as pd
import requests
import json
import time

st.set_page_config(
    page_title="AI Business Sarathi | Vighnaharta Gold Foundation",
    layout="wide",
    page_icon="🤝"
)

# Google Form नोंदणी लिंक
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/viewform?usp=sharing"

# भारतातील प्रमुख १० भाषांची रचना
LANG_DATA = {
    "मराठी": {
        "initiative": "🌟 विघ्नहर्ता गोल्ड फाउंडेशनचा सामाजिक व व्यावसायिक उपक्रम",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "सर्व व्यावसायिक आणि नेटवर्किंग समूहांमधील सदस्यांना अचूक संदर्भ मिळवून देणारा डिजिटल साथीदार",
        "tab1": "🔍 स्मार्ट बिझनेस सर्च",
        "tab2": "👥 सदस्य डिरेक्टरी (संरक्षित)",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 सदस्य लॉगिन व पडताळणी",
        "auth_caption": "नेटवर्किंगचा लाभ घेण्यासाठी आणि संदर्भ शोधण्यासाठी तुमची नोंदणी असणे आवश्यक आहे.",
        "input_label": "तुमचा नोंदणीकृत १० अंकी मोबाईल नंबर किंवा ईमेल टाका:",
        "input_placeholder": "उदा. 8087699949 किंवा name@gmail.com",
        "welcome": "स्वागत आहे, **{name}**! तुमची नोंदणी सक्रिय आहे.",
        "not_registered": "⚠️ हा मोबाईल नंबर किंवा ईमेल आमच्या डिरेक्टरीमध्ये नोंदणीकृत नाही.",
        "register_prompt": "👉 नेटवर्किंग समूहाचा लाभ घेण्यासाठी आणि इतरांचे संदर्भ मिळवण्यासाठी कृपया आधी खालील १ मिनिटाचा फॉर्म भरून नोंदणी करा:",
        "register_btn": "📝 येथे क्लिक करून १ मिनिटात नोंदणी करा (Google Form)",
        "search_title": "तुम्हाला कोणत्या व्यवसायाशी किंवा सेवेशी जोडले जायचे आहे?",
        "search_placeholder": "उदा. 'मला पुण्यात सोन्यात गुंतवणुकीसाठी कोणाशी संपर्क साधता येईल?' किंवा 'बिल्डर्सशी कनेक्टेड कोण आहे?'",
        "search_btn": "संदर्भ शोधा",
        "search_hint": "💡 संदर्भ शोधण्यासाठी कृपया वर तुमचा नोंदणीकृत मोबाईल नंबर किंवा ईमेल टाका.",
        "spinner_search": "AI डेटाबेसमधून योग्य संदर्भ तपासत आहे...",
        "dir_locked": "🔒 डिरेक्टरी पाहण्यासाठी कृपया पहिल्या टॅबमध्ये जाऊन नोंदणीकृत मोबाईल नंबरने लॉगिन करा.",
        "dir_title": "नोंदणीकृत उद्योजक व व्यावसायिक डिरेक्टरी",
        "filter_placeholder": "नाव, शहर किंवा उद्योगानुसार शोधा:",
        "pitch_title": "नेटवर्किंग मिटिंगसाठी व्यवसाय ओळख (Pitch) बनवा",
        "pitch_comp": "तुमची कंपनी / ब्रँड:",
        "pitch_serv": "तुमची मुख्य उत्पादने किंवा सेवा:",
        "pitch_ask": "या आठवड्यात तुम्हाला कोणाशी कनेक्ट व्हायचे आहे (Ask)?",
        "pitch_btn": "पिच तयार करा",
        "spinner_pitch": "तुमचा प्रभावी पिच तयार होत आहे...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्योजकांच्या सशक्तीकरणासाठी व व्यवसाय नेटवर्किंगसाठी कार्यरत आहे.",
        "footer": "संकल्पना व निर्मिती: विघ्नहर्ता गोल्ड फाउंडेशन | भेट द्या:"
    },
    "हिंदी": {
        "initiative": "🌟 विघ्नहर्ता गोल्ड फाउंडेशन की व्यावसायिक पहल",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "सभी व्यावसायिक और नेटवर्किंग समूहों के सदस्यों को सटीक रेफ़रल दिलाने वाला डिजिटल साथी",
        "tab1": "🔍 स्मार्ट बिज़नेस सर्च",
        "tab2": "👥 सदस्य डायरेक्टरी (सुरक्षित)",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 सदस्य लॉगिन व सत्यापन",
        "auth_caption": "नेटवर्किंग का लाभ उठाने और संदर्भ खोजने के लिए डायरेक्टरी में पंजीकरण आवश्यक है।",
        "input_label": "अपना पंजीकृत 10 अंकों का मोबाइल नंबर या ईमेल दर्ज करें:",
        "input_placeholder": "उदा. 8087699949 या name@gmail.com",
        "welcome": "स्वागत है, **{name}**! आपका पंजीकरण सक्रिय है।",
        "not_registered": "⚠️ यह मोबाइल नंबर या ईमेल डायरेक्टरी में पंजीकृत नहीं है।",
        "register_prompt": "👉 रेफ़रल खोजने और नेटवर्किंग का हिस्सा बनने के लिए कृपया पहले 1 मिनट का फॉर्म भरें:",
        "register_btn": "📝 यहाँ क्लिक करके 1 मिनट में पंजीकरण करें (Google Form)",
        "search_title": "आप किस व्यवसाय या सेवा से जुड़ना चाहते हैं?",
        "search_placeholder": "उदा. 'मुझे पुणे में सोने में निवेश के लिए किससे संपर्क करना चाहिए?'",
        "search_btn": "रेफ़रल खोजें",
        "search_hint": "💡 रेफ़रल खोजने के लिए कृपया ऊपर पंजीकृत मोबाइल नंबर दर्ज करें।",
        "spinner_search": "AI उपयुक्त रेफ़रल खोज रहा है...",
        "dir_locked": "🔒 डायरेक्टरी देखने के लिए कृपया पहले टैब में पंजीकृत नंबर से लॉगिन करें।",
        "dir_title": "पंजीकृत उद्यमी व पेशेवर डायरेक्टरी",
        "filter_placeholder": "नाम, शहर या उद्योग अनुसार खोजें:",
        "pitch_title": "नेटवर्किंग मीटिंग के लिए व्यावसायिक परिचय (Pitch) बनाएं",
        "pitch_comp": "आपकी कंपनी / ब्रांड:",
        "pitch_serv": "मुख्य उत्पाद या सेवाएं:",
        "pitch_ask": "इस सप्ताह आपकी क्या आवश्यकता है (Ask)?",
        "pitch_btn": "पिच तैयार करें",
        "spinner_pitch": "पिच तैयार हो रही है...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्यमियों के सशक्तिकरण और नेटवर्किंग के लिए समर्पित है।",
        "footer": "संकल्पना एवं निर्माण: विघ्नहर्ता गोल्ड फाउंडेशन | वेबसाइट:"
    },
    "English": {
        "initiative": "🌟 An Initiative by Vighnaharta Gold Foundation",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "Your AI digital companion connecting entrepreneurs with high-trust referrals",
        "tab1": "🔍 Smart Business Search",
        "tab2": "👥 Member Directory (Protected)",
        "tab3": "📝 30-Sec Pitch Generator",
        "auth_title": "🔐 Member Login & Verification",
        "auth_caption": "To search referrals and access the network, your business must be registered.",
        "input_label": "Enter your registered 10-digit mobile number or email:",
        "input_placeholder": "e.g. 8087699949 or name@gmail.com",
        "welcome": "Welcome, **{name}**! Your registration is verified.",
        "not_registered": "⚠️ This mobile number or email is not registered in our directory.",
        "register_prompt": "👉 To access referrals and connect with members, please register via Google Form:",
        "register_btn": "📝 Click here to register in 1 minute (Google Form)",
        "search_title": "Which business or service are you looking to connect with?",
        "search_placeholder": "e.g. 'Looking for gold investment in Pune' or 'Who connects with architects?'",
        "search_btn": "Find Referral",
        "search_hint": "💡 Please enter your registered contact above to unlock referral search.",
        "spinner_search": "AI is matching the best referral contacts...",
        "dir_locked": "🔒 Directory is protected. Please verify your registered contact in Tab 1 to access.",
        "dir_title": "Registered Member Directory",
        "filter_placeholder": "Search by name, city, or category:",
        "pitch_title": "Create a 30 to 60-Second Business Introduction Pitch",
        "pitch_comp": "Your Company / Brand:",
        "pitch_serv": "Core Products or Services:",
        "pitch_ask": "Who do you want to connect with this week (Ask)?",
        "pitch_btn": "Generate Pitch",
        "spinner_pitch": "Generating your pitch...",
        "about": "Vighnaharta Gold Foundation empowers businesses through financial literacy and networking.",
        "footer": "Conceptualized & Developed by Vighnaharta Gold Foundation | Visit:"
    },
    "ગુજરાતી": {
        "initiative": "🌟 વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશનની એક પહેલ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "વ્યવસાયિકોને સચોટ રેફરલ્સ મેળવવામાં મદદ કરતો ડિજિટલ સાથી",
        "tab1": "🔍 સ્માર્ટ બિઝનેસ સર્ચ",
        "tab2": "👥 સભ્ય ડિરેક્ટરી (સુરક્ષિત)",
        "tab3": "📝 30-સેકન્ડ પિચ જનરેટર",
        "auth_title": "🔐 સભ્ય લૉગિન અને ચકાસણી",
        "auth_caption": "રેફરલ્સ શોધવા માટે તમારી નોંધણી હોવી જરૂરી છે.",
        "input_label": "તમારો નોંધાયેલ 10 અંકનો મોબાઇલ નંબર અથવા ઇમેઇલ દાખલ કરો:",
        "input_placeholder": "દા.ત. 8087699949",
        "welcome": "સ્વાગત છે, **{name}**! તમારી નોંધણી સક્રિય છે.",
        "not_registered": "⚠️ આ મોબાઇલ નંબર ડિરેક્ટરીમાં નોંધાયેલ નથી.",
        "register_prompt": "👉 નેટવર્કિંગનો લાભ લેવા કૃપા કરીને પહેલા 1 મિનિટનું ફોર્મ ભરો:",
        "register_btn": "📝 નોંધણી કરવા માટે અહીં ક્લિક કરો (Google Form)",
        "search_title": "તમે કયા વ્યવસાય અથવા સેવા સાથે જોડાવા માંગો છો?",
        "search_placeholder": "દા.ત. 'પુણેમાં સોનામાં રોકાણ માટે કોનો સંપર્ક કરવો?'",
        "search_btn": "રેફરલ શોધો",
        "search_hint": "💡 શોધવા માટે કૃપા કરીને ઉપર તમારો નંબર દાખલ કરો.",
        "spinner_search": "AI શ્રેષ્ઠ સંપર્કો શોધી રહ્યું છે...",
        "dir_locked": "🔒 ડિરેક્ટરી જોવા માટે કૃપા કરીને પહેલા ટેબમાં લૉગિન કરો.",
        "dir_title": "નોંધાયેલ સભ્યોની ડિરેક્ટરી",
        "filter_placeholder": "નામ, શહેર અથવા કેટેગરી દ્વારા શોધો:",
        "pitch_title": "મીટિંગ માટે 30 સેકન્ડની પિચ બનાવો",
        "pitch_comp": "કંપની / બ્રાન્ડ:",
        "pitch_serv": "મુખ્ય સેવાઓ:",
        "pitch_ask": "તમારી જરૂરિયાત (Ask):",
        "pitch_btn": "પિચ બનાવો",
        "spinner_pitch": "પિચ તૈયાર થઈ રહી છે...",
        "about": "વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન ઉદ્યોગસાહસિકોના વિકાસ માટે કાર્યરત છે.",
        "footer": "સંકલ્પના: વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન | વેબસાઇટ:"
    },
    "தமிழ்": {
        "initiative": "🌟 விக்னஹர்தா கோல்ட் அறக்கட்டளையின் முயற்சி",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "தொழில்முனைவோருக்கு துல்லியமான பரிந்துரைகளை வழங்கும் டிஜிட்டல் உதவியாளர்",
        "tab1": "🔍 ஸ்மார்ட் பிசினஸ் தேடல்",
        "tab2": "👥 உறுப்பினர் பட்டியல் (பாதுகாக்கப்பட்டது)",
        "tab3": "📝 30-வினாடி பிட்ச் உருவாக்குநர்",
        "auth_title": "🔐 உறுப்பினர் உள்நுழைவு",
        "auth_caption": "பரிந்துரைகளைத் தேட பதிவு செய்திருக்க வேண்டும்.",
        "input_label": "பதிவுசெய்த மொபைல் எண் அல்லது மின்னஞ்சலை உள்ளிடவும்:",
        "input_placeholder": "எ.கா. 8087699949",
        "welcome": "வரவேற்கிறோம், **{name}**!",
        "not_registered": "⚠️ இந்த எண் பட்டியலில் பதிவு செய்யப்படவில்லை.",
        "register_prompt": "👉 பதிவு செய்ய கீழேயுள்ள படிவத்தைப் பூர்த்தி செய்யவும்:",
        "register_btn": "📝 பதிவு செய்ய இங்கே கிளிக் செய்யவும் (Google Form)",
        "search_title": "நீங்கள் எந்த தொழிலுடன் இணைய விரும்புகிறீர்கள்?",
        "search_placeholder": "எ.கா. 'தங்க முதலீடு ஆலோசகர் தேவை'",
        "search_btn": "பரிந்துரையைத் தேடு",
        "search_hint": "💡 தேடலைத் திறக்க மேலே பதிவுசெய்த எண்ணை உள்ளிடவும்.",
        "spinner_search": "AI தேடுகிறது...",
        "dir_locked": "🔒 பட்டியலைப் பார்க்க முதல் பக்கத்தில் உள்நுழையவும்.",
        "dir_title": "பதிவுசெய்த உறுப்பினர்கள் பட்டியல்",
        "filter_placeholder": "பெயர் அல்லது நகரம் மூலம் தேடவும்:",
        "pitch_title": "வணிக அறிமுக பிட்ச் உருவாக்கவும்",
        "pitch_comp": "நிறுவனத்தின் பெயர்:",
        "pitch_serv": "சேவைகள்:",
        "pitch_ask": "தேவை (Ask):",
        "pitch_btn": "உருவாக்கு",
        "spinner_pitch": "பிட்ச் தயாராகிறது...",
        "about": "விக்னஹர்தா கோல்ட் அறக்கட்டளை தொழில்முனைவோரை மேம்படுத்துகிறது.",
        "footer": "வடிவமைப்பு: விக்னஹர்தா கோல்ட் அறக்கட்டளை | தளம்:"
    },
    "తెలుగు": {
        "initiative": "🌟 విఘ్నహర్త గోల్డ్ ఫౌండేషన్ చొరవ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "వ్యాపారవేత్తలకు ఖచ్చితమైన రిఫరల్స్ అందించే డిజిటల్ సహచరుడు",
        "tab1": "🔍 స్మార్ట్ బిజినెస్ సెర్చ్",
        "tab2": "👥 సభ్యుల డైరెక్టరీ (రక్షితం)",
        "tab3": "📝 30-సెకన్ల పిచ్ జనరేటర్",
        "auth_title": "🔐 సభ్యుల లాగిన్ & ధృవీకరణ",
        "auth_caption": "రిఫరల్స్ పొందడానికి రిజిస్ట్రేషన్ తప్పనిసరి.",
        "input_label": "నమోదిత మొబైల్ నంబర్ లేదా ఇమెయిల్ నమోదు చేయండి:",
        "input_placeholder": "ఉదా. 8087699949",
        "welcome": "స్వాగతం, **{name}**!",
        "not_registered": "⚠️ ఈ నంబర్ డైరెక్టరీలో నమోదు కాలేదు.",
        "register_prompt": "👉 నెట్‌వర్కింగ్‌లో చేరడానికి దయచేసి ఫారమ్ నింపండి:",
        "register_btn": "📝 నమోదు కొరకు ఇక్కడ క్లిక్ చేయండి (Google Form)",
        "search_title": "మీరు ఏ వ్యాపారంతో కనెక్ట్ కావాలనుకుంటున్నారు?",
        "search_placeholder": "ఉదా. 'బంగారు పెట్టుబడి సలహాదారు కావాలి'",
        "search_btn": "రిఫరల్ కనుగొనండి",
        "search_hint": "💡 సెర్చ్ చేయడానికి మీ నంబర్ నమోదు చేయండి.",
        "spinner_search": "AI రిఫరల్స్ కోసం శోధిస్తోంది...",
        "dir_locked": "🔒 డైరెక్టరీ చూడటానికి మొదటి ట్యాబ్‌లో లాగిన్ చేయండి.",
        "dir_title": "రిజిస్టర్డ్ సభ్యుల జాబితా",
        "filter_placeholder": "పేరు లేదా నగరం ద్వారా వెతకండి:",
        "pitch_title": "30 సెకన్ల బిజినెస్ పిచ్ రూపొందించండి",
        "pitch_comp": "కంపెనీ పేరు:",
        "pitch_serv": "సేవలు:",
        "pitch_ask": "అవసరం (Ask):",
        "pitch_btn": "పిచ్ సిద్ధం చేయండి",
        "spinner_pitch": "పిచ్ తయారవుతోంది...",
        "about": "విఘ్నహర్త గోల్డ్ ఫౌండేషన్ వ్యాపారవేత్తలకు సాధికారత కల్పిస్తుంది.",
        "footer": "రూపకల్పన: విఘ్నహర్త గోల్డ్ ఫౌండేషన్ | వెబ్‌సైట్:"
    },
    "ಕನ್ನಡ": {
        "initiative": "🌟 ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉಪಕ್ರಮ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ಉದ್ಯಮಿಗಳಿಗೆ ನಿಖರವಾದ ಉಲ್ಲೇಖಗಳನ್ನು ಒದಗಿಸುವ ಡಿಜಿಟಲ್ ಸಹಾಯಕ",
        "tab1": "🔍 ಸ್ಮಾರ್ಟ್ ಬಿಸಿನೆಸ್ ಹುಡುಕಾಟ",
        "tab2": "👥 ಸದಸ್ಯರ ಡೈರೆಕ್ಟರಿ (ಸುರಕ್ಷಿತ)",
        "tab3": "📝 30-ಸೆಕೆಂಡ್ ಪಿಚ್ ರಚನೆ",
        "auth_title": "🔐 ಸದಸ್ಯರ ಲಾಗಿನ್ ಮತ್ತು ಪರಿಶೀಲನೆ",
        "auth_caption": "ರೆಫರಲ್‌ಗಳನ್ನು ಹುಡುಕಲು ನೋಂದಣಿ ಅಗತ್ಯವಿದೆ.",
        "input_label": "ನೋಂದಾಯಿತ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇಮೇಲ್ ನಮೂದಿಸಿ:",
        "input_placeholder": "ಉದಾ. 8087699949",
        "welcome": "ಸ್ವಾಗತ, **{name}**!",
        "not_registered": "⚠️ ಈ ಸಂಖ್ಯೆ ಡೈರೆಕ್ಟರಿಯಲ್ಲಿ ನೋಂದಣಿಯಾಗಿಲ್ಲ.",
        "register_prompt": "👉 ನೋಂದಾಯಿಸಲು ದಯವಿಟ್ಟು ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಿ:",
        "register_btn": "📝 ನೋಂದಾಯಿಸಲು ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ (Google Form)",
        "search_title": "ನೀವು ಯಾವ ವ್ಯವಹಾರದೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಲು ಬಯಸುತ್ತೀರಿ?",
        "search_placeholder": "ಉದಾ. 'ಚಿನ್ನದ ಹೂಡಿಕೆ ಸಲಹೆಗಾರ ಬೇಕು'",
        "search_btn": "ಹುಡುಕಿ",
        "search_hint": "💡 ಹುಡುಕಲು ದಯವಿಟ್ಟು ನೋಂದಾಯಿತ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "spinner_search": "AI ಹುಡುಕುತ್ತಿದೆ...",
        "dir_locked": "🔒 ಡೈರೆಕ್ಟರಿ ನೋಡಲು ಮೊದಲ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ಲಾಗಿನ್ ಮಾಡಿ.",
        "dir_title": "ನೋಂದಾಯಿತ ಉದ್ಯಮಿಗಳ ಡೈರೆಕ್ಟರಿ",
        "filter_placeholder": "ಹೆಸರು ಅಥವಾ ನಗರದಿಂದ ಹುಡುಕಿ:",
        "pitch_title": "ವ್ಯವಹಾರ ಪರಿಚಯ ಪಿಚ್ ರಚಿಸಿ",
        "pitch_comp": "ಕಂಪನಿ ಹೆಸರು:",
        "pitch_serv": "ಸೇವೆಗಳು:",
        "pitch_ask": "ಅಗತ್ಯತೆ (Ask):",
        "pitch_btn": "ರಚಿಸಿ",
        "spinner_pitch": "ಪಿಚ್ ಸಿದ್ಧವಾಗುತ್ತಿದೆ...",
        "about": "ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉದ್ಯಮಿಗಳ ಬೆಂಬಲಕ್ಕಾಗಿ ಶ್ರಮಿಸುತ್ತದೆ.",
        "footer": "ವಿನ್ಯಾಸ: ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ | ವೆಬ್‌ಸೈಟ್:"
    },
    "മലയാളം": {
        "initiative": "🌟 വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷന്റെ സംരംഭം",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ബിസിനസ് റഫറലുകൾ കൃത്യമായി കണ്ടെത്തുന്ന ഡിജിറ്റൽ സഹായി",
        "tab1": "🔍 സ്മാർട്ട് ബിസിനസ് തിരയൽ",
        "tab2": "👥 അംഗങ്ങളുടെ ഡയറക്ടറി (സുരക്ഷിതം)",
        "tab3": "📝 30-സെക്കൻഡ് പിച്ച് ജനറേറ്റർ",
        "auth_title": "🔐 ലോഗിൻ & സ്ഥിരീകരണം",
        "auth_caption": "റഫറലുകൾ ലഭിക്കാൻ രജിസ്ട്രേഷൻ ആവശ്യമാണ്.",
        "input_label": "രജിസ്റ്റർ ചെയ്ത മൊബൈൽ നമ്പറോ ഇമെയിലോ നൽകുക:",
        "input_placeholder": "ഉദാ. 8087699949",
        "welcome": "സ്വാഗതം, **{name}**!",
        "not_registered": "⚠️ ഈ നമ്പർ ഡയറക്ടറിയിൽ ലഭ്യമല്ല.",
        "register_prompt": "👉 രജിസ്റ്റർ ചെയ്യാൻ ഫോം പൂരിപ്പിക്കുക:",
        "register_btn": "📝 രജിസ്റ്റർ ചെയ്യാൻ ഇവിടെ ക്ലിക്ക് ചെയ്യുക (Google Form)",
        "search_title": "ഏത് ബിസിനസ്സുമായാണ് ബന്ധപ്പെടേണ്ടത്?",
        "search_placeholder": "ഉദാ. 'സ്വർണ്ണ നിക്ഷേപ ഉപദേശകൻ'",
        "search_btn": "റഫറൽ കണ്ടെത്തുക",
        "search_hint": "💡 തിരയാൻ ദയവായി നിങ്ങളുടെ നമ്പർ നൽകുക.",
        "spinner_search": "AI തിരയുന്നു...",
        "dir_locked": "🔒 ഡയറക്ടറി കാണാൻ ആദ്യ ടാബിൽ ലോഗിൻ ചെയ്യുക.",
        "dir_title": "രജിസ്റ്റർ ചെയ്ത അംഗങ്ങളുടെ ഡയറക്ടറി",
        "filter_placeholder": "പേരോ നഗരമോ അനുസരിച്ച് തിരയുക:",
        "pitch_title": "ബിസിനസ് പിച്ച് തയ്യാറാക്കുക",
        "pitch_comp": "കമ്പനി:",
        "pitch_serv": "സേവനങ്ങൾ:",
        "pitch_ask": "ആവശ്യം (Ask):",
        "pitch_btn": "തയ്യാറാക്കുക",
        "spinner_pitch": "പിച്ച് തയ്യാറാകുന്നു...",
        "about": "വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ സംരംഭകരുടെ വളർച്ചയ്ക്കായി നിലകൊള്ളുന്നു.",
        "footer": "രൂപകൽപ്പന: വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ | സൈറ്റ്:"
    },
    "বাংলা": {
        "initiative": "🌟 বিঘ্নহর্তা গোল্ড ফাউন্ডেশনের একটি উদ্যোগ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ব্যবসায়ীদের সঠিক রেফারেল খুঁজে দেওয়ার ডিজিটাল সাথী",
        "tab1": "🔍 স্মার্ট বিজনেস সার্চ",
        "tab2": "👥 সদস্য ডিরেক্টরি (সুরক্ষিত)",
        "tab3": "📝 ৩০-সেকেন্ড পিচ জেনারেটর",
        "auth_title": "🔐 সদস্য লগইন ও যাচাইকরণ",
        "auth_caption": "রেফারেল খুঁজতে আপনার নিবন্ধন থাকা আবশ্যক।",
        "input_label": "আপনার নিবন্ধিত মোবাইল নম্বর বা ইমেল দিন:",
        "input_placeholder": "যেমন: 8087699949",
        "welcome": "স্বাগতম, **{name}**!",
        "not_registered": "⚠️ এই নম্বরটি ডিরেক্টরিতে নিবন্ধিত নেই।",
        "register_prompt": "👉 রেফারেল পেতে দয়া করে ফর্ম পূরণ করে নিবন্ধন করুন:",
        "register_btn": "📝 নিবন্ধন করতে এখানে ক্লিক করুন (Google Form)",
        "search_title": "আপনি কোন ব্যবসার সাথে যুক্ত হতে চান?",
        "search_placeholder": "যেমন: 'স্বর্ণে বিনিয়োগের পরামর্শদাতা চাই'",
        "search_btn": "রেফারেল খুঁজুন",
        "search_hint": "💡 অনুসন্ধানের জন্য উপরে আপনার নম্বর লিখুন।",
        "spinner_search": "AI রেফারেল খুঁজছে...",
        "dir_locked": "🔒 ডিরেক্টরি দেখতে প্রথম ট্যাবে লগইন করুন।",
        "dir_title": "নিবন্ধিত সদস্যদের ডিরেক্টরি",
        "filter_placeholder": "নাম বা শহর দিয়ে অনুসন্ধান করুন:",
        "pitch_title": "ব্যবসায়িক পরিচয়ের পিচ তৈরি করুন",
        "pitch_comp": "কোম্পানি:",
        "pitch_serv": "পরিষেবা:",
        "pitch_ask": "চাহিদা (Ask):",
        "pitch_btn": "তৈরি করুন",
        "spinner_pitch": "পিচ তৈরি হচ্ছে...",
        "about": "বিঘ্নহর্তা গোল্ড ফাউন্ডেশন ব্যবসায়ীদের ক্ষমতায়নের জন্য কাজ করে।",
        "footer": "পরিকল্পনা: বিঘ্নহর্তা গোল্ড ফাউন্ডেশন | ওয়েবসাইট:"
    },
    "ਪੰਜਾਬੀ": {
        "initiative": "🌟 ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਦਾ ਉਪਰਾਲਾ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ਕਾਰੋਬਾਰੀਆਂ ਨੂੰ ਸਹੀ ਰੈਫਰਲ ਦਿਵਾਉਣ ਵਾਲਾ ਡਿਜੀਟਲ ਸਾਥੀ",
        "tab1": "🔍 ਸਮਾਰਟ ਬਿਜ਼ਨਸ ਸਰਚ",
        "tab2": "👥 ਮੈਂਬਰ ਡਾਇਰੈਕਟਰੀ (ਸੁਰੱਖਿਅਤ)",
        "tab3": "📝 30-ਸਕਿੰਟ ਪਿੱਚ ਜਨਰੇਟਰ",
        "auth_title": "🔐 ਮੈਂਬਰ ਲੌਗਇਨ ਤੇ ਤਸਦੀਕ",
        "auth_caption": "ਰੈਫਰਲ ਲੱਭਣ ਲਈ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਹੋਣੀ ਲਾਜ਼ਮੀ ਹੈ।",
        "input_label": "ਆਪਣਾ ਰਜਿਸਟਰਡ ਮੋਬਾਈਲ ਨੰਬਰ ਜਾਂ ਈਮੇਲ ਦਰਜ ਕਰੋ:",
        "input_placeholder": "ਜਿਵੇਂ: 8087699949",
        "welcome": "ਜੀ ਆਇਆਂ ਨੂੰ, **{name}**!",
        "not_registered": "⚠️ ਇਹ ਨੰਬਰ ਡਾਇਰੈਕਟਰੀ ਵਿੱਚ ਦਰਜ ਨਹੀਂ ਹੈ।",
        "register_prompt": "👉 ਨੈੱਟਵਰਕ ਨਾਲ ਜੁੜਨ ਲਈ ਕਿਰਪਾ ਕਰਕੇ ਪਹਿਲਾਂ ਫਾਰਮ ਭਰੋ:",
        "register_btn": "📝 ਰਜਿਸਟਰ ਕਰਨ ਲਈ ਇੱਥੇ ਕਲਿੱਕ ਕਰੋ (Google Form)",
        "search_title": "ਤੁਸੀਂ ਕਿਸ ਕਾਰੋਬਾਰ ਨਾਲ ਜੁੜਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search_placeholder": "ਜਿਵੇਂ: 'ਸੋਨੇ ਦੇ ਨਿਵੇਸ਼ ਲਈ ਸੰਪਰਕ'",
        "search_btn": "ਰੈਫਰਲ ਲੱਭੋ",
        "search_hint": "💡 ਖੋਜ ਕਰਨ ਲਈ ਕਿਰਪਾ ਕਰਕੇ ਆਪਣਾ ਨੰਬਰ ਦਰਜ ਕਰੋ।",
        "spinner_search": "AI ਰੈਫਰਲ ਲੱਭ ਰਿਹਾ ਹੈ...",
        "dir_locked": "🔒 ਡਾਇਰੈਕਟਰੀ ਵੇਖਣ ਲਈ ਪਹਿਲੇ ਟੈਬ ਵਿੱਚ ਲੌਗਇਨ ਕਰੋ।",
        "dir_title": "ਰਜਿਸਟਰਡ ਕਾਰੋਬਾਰੀ ਡਾਇਰੈਕਟਰੀ",
        "filter_placeholder": "ਨਾਮ ਜਾਂ ਸ਼ਹਿਰ ਅਨੁਸਾਰ ਲੱਭੋ:",
        "pitch_title": "ਕਾਰੋਬਾਰੀ ਪਿੱਚ ਤਿਆਰ ਕਰੋ",
        "pitch_comp": "ਕੰਪਨੀ:",
        "pitch_serv": "ਸੇਵਾਵਾਂ:",
        "pitch_ask": "ਲੋੜ (Ask):",
        "pitch_btn": "ਤਿਆਰ ਕਰੋ",
        "spinner_pitch": "ਪਿੱਚ ਤਿਆਰ ਹੋ ਰਹੀ ਹੈ...",
        "about": "ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਕਾਰੋਬਾਰਾਂ ਦੇ ਵਿਕਾਸ ਲਈ ਕੰਮ ਕਰਦੀ ਹੈ।",
        "footer": "ਨਿਰਮਾਣ: ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ | ਵੈੱਬਸਾਈਟ:"
    }
}

# साइडबार - १० भाषांची निवड
with st.sidebar:
    st.markdown("### 🏛️ **विघ्नहर्ता गोल्ड फाउंडेशन**")
    st.caption("Empowering Entrepreneurs & Business Networking")
    
    st.markdown("---")
    st.subheader("🌐 भाषा निवडा / Choose Language")
    languages = list(LANG_DATA.keys())
    selected_lang = st.selectbox(
        "Select Language / भाषा चुनें:",
        options=languages,
        index=0
    )
    t = LANG_DATA[selected_lang]
    
    st.info(f"ℹ️ {t['about']}")
    st.markdown("[🌐 www.vgold.co.in](https://www.vgold.co.in)")
    
    st.markdown("---")
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
    if not GEMINI_API_KEY:
        st.subheader("⚙️ API Configuration")
        GEMINI_API_KEY = st.text_input("Enter Gemini API Key:", type="password")

# Google Sheet CSV लोड
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

# सुरक्षित Gemini कॉल
def call_gemini(prompt_text, api_key):
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    
    available_models = []
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(list_url, timeout=10)
        if res.status_code == 200:
            for item in res.json().get("models", []):
                if "generateContent" in item.get("supportedGenerationMethods", []):
                    available_models.append(item.get("name", "").replace("models/", ""))
    except Exception:
        pass

    if not available_models:
        available_models = ["gemini-3.8-flash", "gemini-3.8-pro", "gemini-2.5-flash", "gemini-flash-latest"]

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

    return "Server is busy. Please try again."

# हेडर
st.markdown(f"**{t['initiative']}**")
st.title(t["title"])
st.subheader(t["subtitle"])
st.caption(t["caption"])

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

# लॉगिन स्टेट तपासणे
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# टॅब १: सर्च व लॉगिन
with tab1:
    st.write(f"### {t['auth_title']}")
    st.caption(t["auth_caption"])
    
    user_contact = st.text_input(t["input_label"], placeholder=t["input_placeholder"])
    
    if user_contact:
        contact_str = str(user_contact).strip().lower()
        mask = df.apply(lambda row: row.astype(str).str.strip().str.lower().str.contains(contact_str, regex=False), axis=1)
        matches = df[mask.any(axis=1)]
        
        if not matches.empty:
            st.session_state.logged_in_user = matches.iloc[0]
            name_col = [c for c in df.columns if "नाव" in c or "Name" in c]
            user_name = st.session_state.logged_in_user[name_col[0]] if name_col else "Member"
            st.success(t["welcome"].format(name=user_name))
        else:
            st.session_state.logged_in_user = None
            st.warning(t["not_registered"])
            st.info(t["register_prompt"])
            st.link_button(t["register_btn"], FORM_LINK, type="primary")

    st.markdown("---")
    
    if st.session_state.logged_in_user is not None:
        st.write(f"### {t['search_title']}")
        query = st.text_input(t["search_title"], placeholder=t["search_placeholder"], label_visibility="collapsed")
        
        if st.button(t["search_btn"], type="primary") and query:
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
                    4. Professional formatting with bullet points.
                    """
                    reply = call_gemini(prompt, GEMINI_API_KEY)
                    st.markdown(reply)
    else:
        if not user_contact:
            st.info(t["search_hint"])

# टॅब २: सुरक्षित डिरेक्टरी (Protected)
with tab2:
    st.write(f"### {t['dir_title']}")
    
    if st.session_state.logged_in_user is None:
        st.warning(t["dir_locked"])
        st.info("💡 डेटा सुरक्षिततेसाठी डिरेक्टरी फक्त अधिकृत सदस्यांनाच पाहता येते.")
    else:
        if not df.empty:
            search_filter = st.text_input(t["filter_placeholder"])
            
            # संवेदनशील माहिती (जसे Timestamp) वगळून डिरेक्टरी दाखवणे
            display_cols = [c for c in df.columns if "Timestamp" not in c and "टाइम" not in c]
            safe_df = df[display_cols] if display_cols else df
            
            if search_filter:
                filtered = safe_df[safe_df.apply(lambda row: search_filter.lower() in row.astype(str).str.lower().values, axis=1)]
                st.dataframe(filtered, use_container_width=True)
            else:
                st.dataframe(safe_df, use_container_width=True)
        else:
            st.info("No records.")

# टॅब ३: पिच जनरेटर
with tab3:
    st.write(f"### {t['pitch_title']}")
    b_name = st.text_input(t["pitch_comp"])
    b_serv = st.text_area(t["pitch_serv"])
    b_ask = st.text_input(t["pitch_ask"])
    
    if st.button(t["pitch_btn"]):
        if not GEMINI_API_KEY:
            st.error("API Key missing.")
        elif b_name and b_serv:
            with st.spinner(t["spinner_pitch"]):
                pitch_prompt = f"""
                Company: {b_name}
                Services: {b_serv}
                Ask: {b_ask}
                Language: {selected_lang}
                
                Generate a confident 30-sec pitch for business networking meet in {selected_lang}.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.success(pitch_reply)

# तळटीप ब्रँडिंग
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 15px;'>
        {t['footer']} 
        <a href='https://www.vgold.co.in' target='_blank' style='color: #d4af37; font-weight: bold; text-decoration: none;'>
            www.vgold.co.in
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
