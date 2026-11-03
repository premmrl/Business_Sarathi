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
        "tab2": "📝 30-Sec Pitch & Stimulation Generator",
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
        "pitch_title": "नेटवर्किंग मिटिंगसाठी 30-सेकंद पिच व स्टिम्युलेशन (Stimulation)",
        "pitch_comp": "तुमची कंपनी / ब्रँड:",
        "pitch_serv": "तुमची मुख्य उत्पादने किंवा सेवा:",
        "pitch_stim": "स्टिम्युलेशन / ट्रिगर थीम (उदा. ग्राहकांचे बोलणे, समस्या, प्रसंग किंवा ऑफर - ऐच्छिक):",
        "pitch_stim_hint": "उदा. 'सोने महाग झाले आहे', 'मुलीच्या लग्नासाठी सोन्याचे नियोजन', 'MDRT एजंट्सचे इन्कम मॉडेल'",
        "pitch_ask": "या आठवड्यात तुम्हाला कोणाशी कनेक्ट व्हायचे आहे (Ask)?",
        "pitch_btn": "प्रभावी पिच आणि स्टिम्युलेशन बनवा",
        "spinner_pitch": "तुमचा प्रभावी पिच आणि स्टिम्युलेशन ट्रिगर्स तयार होत आहेत...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्योजकांच्या सशक्तीकरणासाठी व व्यवसाय नेटवर्किंगसाठी कार्यरत आहे.",
        "footer": "संकल्पना व निर्मिती: विघ्नहर्ता गोल्ड फाउंडेशन | अधिक माहितीसाठी:"
    },
    "हिंदी": {
        "initiative": "🌟 विघ्नहर्ता गोल्ड फाउंडेशन की व्यावसायिक पहल",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "सभी व्यावसायिक और नेटवर्किंग समूहों के सदस्यों को सटीक रेफ़रल दिलाने वाला डिजिटल साथी",
        "tab1": "🔍 स्मार्ट बिज़नेस सर्च",
        "tab2": "📝 30-Sec Pitch & Stimulation Generator",
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
        "pitch_title": "नेटवर्किंग मीटिंग के लिए 30-सेकंड पिच और स्टिम्युलेशन (Stimulation)",
        "pitch_comp": "आपकी कंपनी / ब्रांड:",
        "pitch_serv": "मुख्य उत्पाद या सेवाएं:",
        "pitch_stim": "स्टिम्युलेशन / ट्रिगर थीम (वैकल्पिक):",
        "pitch_stim_hint": "उदा. 'सोना महंगा हो गया है', 'भविष्य के लिए सोने की बचत'",
        "pitch_ask": "इस सप्ताह आपकी क्या आवश्यकता है (Ask)?",
        "pitch_btn": "पिच और स्टिम्युलेशन तैयार करें",
        "spinner_pitch": "पिच और स्टिम्युलेशन ट्रिगर्स तैयार हो रहे हैं...",
        "about": "विघ्नहर्ता गोल्ड फाउंडेशन उद्यमियों के सशक्तिकरण और नेटवर्किंग के लिए समर्पित है।",
        "footer": "संकल्पना एवं निर्माण: विघ्नहर्ता गोल्ड फाउंडेशन | वेबसाइट:"
    },
    "English": {
        "initiative": "🌟 An Initiative by Vighnaharta Gold Foundation",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "Your AI digital companion connecting entrepreneurs with high-trust referrals",
        "tab1": "🔍 Smart Business Search",
        "tab2": "📝 30-Sec Pitch & Stimulation Generator",
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
        "pitch_title": "Create a 30-Sec Business Pitch with Stimulation & Triggers",
        "pitch_comp": "Your Company / Brand:",
        "pitch_serv": "Core Products or Services:",
        "pitch_stim": "Stimulation / Trigger Point (Optional):",
        "pitch_stim_hint": "e.g., 'When someone says gold is too expensive', 'Child marriage planning'",
        "pitch_ask": "Who do you want to connect with this week (Ask)?",
        "pitch_btn": "Generate Pitch & Stimulation",
        "spinner_pitch": "Crafting high-impact pitch and referral triggers...",
        "about": "Vighnaharta Gold Foundation empowers businesses through financial literacy and networking.",
        "footer": "Conceptualized & Developed by Vighnaharta Gold Foundation | Visit:"
    },
    "ગુજરાતી": {
        "initiative": "🌟 વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશનની એક પહેલ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "વ્યવસાયિકોને સચોટ રેફરલ્સ મેળવવામાં મદદ કરતો ડિજિટલ સાથી",
        "tab1": "🔍 સ્માર્ટ બિઝનેસ સર્ચ",
        "tab2": "📝 30-સેકન્ડ પિચ અને સ્ટિમ્યુલેશન જનરેટર",
        "auth_title": "🔐 સભ્ય લૉગિન અને ચકાસણી",
        "auth_caption": "રેફરલ્સ શોધવા માટે તમારી નોંધણી હોવી જરૂરી છે.",
        "input_label": "તમારો નોંધાયેલ 10 અંકનો મોબાઇલ નંબર અથવા ઇમેઇલ દાખલ કરો:",
        "input_placeholder": "દા.ત. 8087699949",
        "welcome": "સ્વાગત છે, **{name}**!",
        "not_registered": "⚠️ આ મોબાઇલ નંબર ડિરેક્ટરીમાં નોંધાયેલ નથી.",
        "register_prompt": "👉 નેટવર્કિંગનો લાભ લેવા કૃપા કરીને પહેલા ફોર્મ ભરો:",
        "register_btn": "📝 નોંધણી કરવા માટે અહીં ક્લિક કરો (Google Form)",
        "search_title": "તમે કયા વ્યવસાય અથવા સેવા સાથે જોડાવા માંગો છો?",
        "search_placeholder": "દા.ત. 'પુણેમાં સોનામાં રોકાણ માટે કોનો સંપર્ક કરવો?'",
        "search_btn": "રેફરલ શોધો",
        "search_hint": "💡 શોધવા માટે કૃપા કરીને ઉપર તમારો નંબર દાખલ કરો.",
        "spinner_search": "AI શ્રેષ્ઠ સંપર્કો શોધી રહ્યું છે...",
        "pitch_title": "મીટિંગ માટે 30-સેકન્ડ પિચ અને સ્ટિમ્યુલેશન બનાવો",
        "pitch_comp": "કંપની / બ્રાન્ડ:",
        "pitch_serv": "મુખ્ય સેવાઓ:",
        "pitch_stim": "સ્ટિમ્યુલેશન / ટ્રિગર (વૈકલ્પિક):",
        "pitch_stim_hint": "દા.ત. 'સોનાના ભાવ વધ્યા છે'",
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
        "tab2": "📝 30-வினாடி பிட்ச் & ஸ்டிமுலேஷன்",
        "auth_title": "🔐 உறுப்பினர் உள்நுழைவு",
        "auth_caption": "பரிந்துரைகளைத் தேட பதிவு அவசியம்.",
        "input_label": "பதிவுசெய்த மொபைல் எண் உள்ளிடவும்:",
        "input_placeholder": "எ.கா. 8087699949",
        "welcome": "வரவேற்கிறோம், **{name}**!",
        "not_registered": "⚠️ எண் பட்டியலில் இல்லை.",
        "register_prompt": "👉 பதிவு செய்ய படிவத்தைப் பூர்த்தி செய்யவும்:",
        "register_btn": "📝 பதிவு செய்ய கிளிக் செய்யவும் (Google Form)",
        "search_title": "நீங்கள் எந்த தொழிலுடன் இணைய விரும்புகிறீர்கள்?",
        "search_placeholder": "எ.கா. 'தங்க முதலீடு ஆலோசகர் தேவை'",
        "search_btn": "பரிந்துரையைத் தேடு",
        "search_hint": "💡 தேடலுக்கு மேலே எண் உள்ளிடவும்.",
        "spinner_search": "AI தேடுகிறது...",
        "pitch_title": "வணிக அறிமுக பிட்ச் & ஸ்டிமுலேஷன்",
        "pitch_comp": "நிறுவனம்:",
        "pitch_serv": "சேவைகள்:",
        "pitch_stim": "ஸ்டிமுலேஷன் / தூண்டுதல்:",
        "pitch_stim_hint": "எ.கா. 'தங்கம் விலை உயர்வு'",
        "pitch_ask": "தேவை (Ask):",
        "pitch_btn": "உருவாக்கு",
        "spinner_pitch": "தயாராகிறது...",
        "about": "விக்னஹர்தா கோல்ட் அறக்கட்டளை தொழில்முனைவோரை மேம்படுத்துகிறது.",
        "footer": "வடிவமைப்பு: விக்னஹர்தா கோல்ட் அறக்கட்டளை"
    },
    "తెలుగు": {
        "initiative": "🌟 విఘ్నహర్త గోల్డ్ ఫౌండేషన్ చొరవ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "వ్యాపారవేత్తలకు ఖచ్చితమైన రిఫరల్స్ అందించే డిజిటల్ సహచరుడు",
        "tab1": "🔍 స్మార్ట్ బిజినెస్ సెర్చ్",
        "tab2": "📝 30-సెకన్ల పిచ్ & స్టిమ్యులేషన్",
        "auth_title": "🔐 సభ్యుల లాగిన్",
        "auth_caption": "రిఫరల్స్ కోసం రిజిస్ట్రేషన్ తప్పనిసరి.",
        "input_label": "మొబైల్ నంబర్ నమోదు చేయండి:",
        "input_placeholder": "ఉదా. 8087699949",
        "welcome": "స్వాగతం, **{name}**!",
        "not_registered": "⚠️ నంబర్ డైరెక్టరీలో లేదు.",
        "register_prompt": "👉 నమోదు కొరకు ఫారమ్ నింపండి:",
        "register_btn": "📝 నమోదు చేయండి (Google Form)",
        "search_title": "ఏ వ్యాపారంతో కనెక్ట్ కావాలనుకుంటున్నారు?",
        "search_placeholder": "ఉదా. 'బంగారు పెట్టుబడి సలహాదారు'",
        "search_btn": "కనుగొనండి",
        "search_hint": "💡 సెర్చ్ చేయడానికి నంబర్ నమోదు చేయండి.",
        "spinner_search": "AI శోధిస్తోంది...",
        "pitch_title": "30 సెకన్ల పిచ్ మరియు స్టిమ్యులేషన్",
        "pitch_comp": "కంపెనీ:",
        "pitch_serv": "సేవలు:",
        "pitch_stim": "స్టిమ్యులేషన్ / ట్రిగ్గర్:",
        "pitch_stim_hint": "ఉదా. 'బంగారం ధరలు పెరిగాయి'",
        "pitch_ask": "అవసరం (Ask):",
        "pitch_btn": "సిద్ధం చేయండి",
        "spinner_pitch": "తయారవుతోంది...",
        "about": "విఘ్నహర్త గోల్డ్ ఫౌండేషన్ వ్యాపారవేత్తలకు సాధికారత కల్పిస్తుంది.",
        "footer": "రూపకల్పన: విఘ్నహర్త గోల్డ్ ఫౌండేషన్"
    },
    "ಕನ್ನಡ": {
        "initiative": "🌟 ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉಪಕ್ರಮ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ಉದ್ಯಮಿಗಳಿಗೆ ನಿಖರವಾದ ಉಲ್ಲೇಖಗಳನ್ನು ಒದಗಿಸುವ ಡಿಜಿಟಲ್ ಸಹಾಯಕ",
        "tab1": "🔍 ಸ್ಮಾರ್ಟ್ ಬಿಸಿನೆಸ್ ಹುಡುಕಾಟ",
        "tab2": "📝 30-ಸೆಕೆಂಡ್ ಪಿಚ್ ಮತ್ತು ಸ್ಟಿಮ್ಯುಲೇಶನ್",
        "auth_title": "🔐 ಸದಸ್ಯರ ಲಾಗಿನ್",
        "auth_caption": "ರೆಫರಲ್‌ಗಳಿಗಾಗಿ ನೋಂದಣಿ ಅಗತ್ಯವಿದೆ.",
        "input_label": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ:",
        "input_placeholder": "ಉದಾ. 8087699949",
        "welcome": "ಸ್ವಾಗತ, **{name}**!",
        "not_registered": "⚠️ ಈ ಸಂಖ್ಯೆ ನೋಂದಣಿಯಾಗಿಲ್ಲ.",
        "register_prompt": "👉 ನೋಂದಾಯಿಸಲು ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಿ:",
        "register_btn": "📝 ನೋಂದಾಯಿಸಿ (Google Form)",
        "search_title": "ಯಾವ ವ್ಯವಹಾರದೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಲು ಬಯಸುತ್ತೀರಿ?",
        "search_placeholder": "ಉದಾ. 'ಚಿನ್ನದ ಹೂಡಿಕೆ'",
        "search_btn": "ಹುಡುಕಿ",
        "search_hint": "💡 ಹುಡುಕಲು ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.",
        "spinner_search": "AI ಹುಡುಕುತ್ತಿದೆ...",
        "pitch_title": "ವ್ಯವಹಾರ ಪಿಚ್ ಮತ್ತು ಸ್ಟಿಮ್ಯುಲೇಶನ್ ರಚಿಸಿ",
        "pitch_comp": "ಕಂಪನಿ:",
        "pitch_serv": "ಸೇವೆಗಳು:",
        "pitch_stim": "ಸ್ಟಿಮ್ಯುಲೇಶನ್ / ಟ್ರಿಗ್ಗರ್:",
        "pitch_stim_hint": "ಉದಾ. 'ಚಿನ್ನದ ದರ ಏರಿಕೆ'",
        "pitch_ask": "ಅಗತ್ಯತೆ (Ask):",
        "pitch_btn": "ರಚಿಸಿ",
        "spinner_pitch": "ಸಿದ್ಧವಾಗುತ್ತಿದೆ...",
        "about": "ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉದ್ಯಮಿಗಳ ಬೆಂಬಲಕ್ಕಾಗಿ ಶ್ರಮಿಸುತ್ತದೆ.",
        "footer": "ವಿನ್ಯಾಸ: ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್"
    },
    "മലയാളം": {
        "initiative": "🌟 വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ സംരംഭം",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ബിസിനസ് റഫറലുകൾ നൽകുന്ന ഡിജിറ്റൽ സഹായി",
        "tab1": "🔍 സ്മാർട്ട് ബിസിനസ് തിരയൽ",
        "tab2": "📝 30-സെക്കൻഡ് പിച്ചും സ്റ്റിമുലേഷനും",
        "auth_title": "🔐 ലോഗിൻ & സ്ഥിരീകരണം",
        "auth_caption": "റഫറലുകൾ ലഭിക്കാൻ രജിസ്ട്രേഷൻ ആവശ്യമാണ്.",
        "input_label": "മൊബൈൽ നമ്പർ നൽകുക:",
        "input_placeholder": "ഉദാ. 8087699949",
        "welcome": "സ്വാഗതം, **{name}**!",
        "not_registered": "⚠️ നമ്പർ ലഭ്യമല്ല.",
        "register_prompt": "👉 രജിസ്റ്റർ ചെയ്യാൻ ഫോം പൂരിപ്പിക്കുക:",
        "register_btn": "📝 രജിസ്റ്റർ ചെയ്യുക (Google Form)",
        "search_title": "ഏത് ബിസിനസ്സുമായാണ് ബന്ധപ്പെടേണ്ടത്?",
        "search_placeholder": "ഉദാ. 'സ്വർണ്ണ നിക്ഷേപം'",
        "search_btn": "കണ്ടെത്തുക",
        "search_hint": "💡 നമ്പർ നൽകുക.",
        "spinner_search": "AI തിരയുന്നു...",
        "pitch_title": "ബിസിനസ് പിച്ചും സ്റ്റിമുലേഷനും",
        "pitch_comp": "കമ്പനി:",
        "pitch_serv": "സേവനങ്ങൾ:",
        "pitch_stim": "സ്റ്റിമുലേഷൻ / ട്രിഗർ:",
        "pitch_stim_hint": "ഉദാ. 'സ്വർണ്ണവില വർദ്ധനവ്'",
        "pitch_ask": "ആവശ്യം (Ask):",
        "pitch_btn": "തയ്യാറാക്കുക",
        "spinner_pitch": "തയ്യാറാകുന്നു...",
        "about": "വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ സംരംഭകരുടെ വളർച്ചയ്ക്കായി നിലകൊള്ളുന്നു.",
        "footer": "രൂപകൽപ്പന: വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ"
    },
    "বাংলা": {
        "initiative": "🌟 বিঘ্নহর্তা গোল্ড ফাউন্ডেশনের একটি উদ্যোগ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ব্যবসায়ীদের সঠিক রেফারেল খুঁজে দেওয়ার ডিজিটাল সাথী",
        "tab1": "🔍 স্মার্ট বিজনেস সার্চ",
        "tab2": "📝 ৩০-সেকেন্ড পিচ ও স্টিমুলেশন",
        "auth_title": "🔐 সদস্য লগইন",
        "auth_caption": "রেফারেল খুঁজতে নিবন্ধন আবশ্যক।",
        "input_label": "মোবাইল নম্বর দিন:",
        "input_placeholder": "যেমন: 8087699949",
        "welcome": "স্বাগতম, **{name}**!",
        "not_registered": "⚠️ এই নম্বরটি নিবন্ধিত নেই।",
        "register_prompt": "👉 নিবন্ধন করতে ফর্ম পূরণ করুন:",
        "register_btn": "📝 নিবন্ধন করুন (Google Form)",
        "search_title": "আপনি কোন ব্যবসার সাথে যুক্ত হতে চান?",
        "search_placeholder": "যেমন: 'স্বর্ণে বিনিয়োগ'",
        "search_btn": "খুঁজুন",
        "search_hint": "💡 অনুসন্ধানের জন্য নম্বর লিখুন।",
        "spinner_search": "AI রেফারেল খুঁজছে...",
        "pitch_title": "ব্যবসায়িক পিচ এবং স্টিমুলেশন তৈরি করুন",
        "pitch_comp": "কোম্পানি:",
        "pitch_serv": "পরিষেবা:",
        "pitch_stim": "স্টিমুলেশন / রেফারেল ট্রিগার:",
        "pitch_stim_hint": "যেমন: 'সোনার দাম বেড়েছে'",
        "pitch_ask": "চাহিদা (Ask):",
        "pitch_btn": "তৈরি করুন",
        "spinner_pitch": "তৈরি হচ্ছে...",
        "about": "বিঘ্নহর্তা গোল্ড ফাউন্ডেশন ব্যবসায়ীদের জন্য কাজ করে।",
        "footer": "পরিকল্পনা: বিঘ্নহর্তা গোল্ড ফাউন্ডেশন"
    },
    "ਪੰਜਾਬੀ": {
        "initiative": "🌟 ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਦਾ ਉਪਰਾਲਾ",
        "title": "🤝 AI Business Sarathi",
        "subtitle": "Universal Networking & Referral Matcher",
        "caption": "ਕਾਰੋਬਾਰੀਆਂ ਨੂੰ ਸਹੀ ਰੈਫਰਲ ਦਿਵਾਉਣ ਵਾਲਾ ਡਿਜੀਟਲ ਸਾਥੀ",
        "tab1": "🔍 ਸਮਾਰਟ ਬਿਜ਼ਨਸ ਸਰਚ",
        "tab2": "📝 30-ਸਕਿੰਟ ਪਿੱਚ ਅਤੇ ਸਟਿਮੂਲੇਸ਼ਨ",
        "auth_title": "🔐 ਮੈਂਬਰ ਲੌਗਇਨ",
        "auth_caption": "ਰੈਫਰਲ ਲੱਭਣ ਲਈ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਾਜ਼ਮੀ ਹੈ।",
        "input_label": "ਮੋਬਾਈਲ ਨੰਬਰ ਦਰਜ ਕਰੋ:",
        "input_placeholder": "ਜਿਵੇਂ: 8087699949",
        "welcome": "ਜੀ ਆਇਆਂ ਨੂੰ, **{name}**!",
        "not_registered": "⚠️ ਨੰਬਰ ਦਰਜ ਨਹੀਂ ਹੈ।",
        "register_prompt": "👉 ਕਿਰਪਾ ਕਰਕੇ ਪਹਿਲਾਂ ਫਾਰਮ ਭਰੋ:",
        "register_btn": "📝 ਰਜਿਸਟਰ ਕਰੋ (Google Form)",
        "search_title": "ਤੁਸੀਂ ਕਿਸ ਕਾਰੋਬਾਰ ਨਾਲ ਜੁੜਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search_placeholder": "ਜਿਵੇਂ: 'ਸੋਨੇ ਦਾ ਨਿਵੇਸ਼'",
        "search_btn": "ਲੱਭੋ",
        "search_hint": "💡 ਖੋਜ ਕਰਨ ਲਈ ਨੰਬਰ ਦਰਜ ਕਰੋ।",
        "spinner_search": "AI ਰੈਫਰਲ ਲੱਭ ਰਿਹਾ ਹੈ...",
        "pitch_title": "ਕਾਰੋਬਾਰੀ ਪਿੱਚ ਅਤੇ ਸਟਿਮੂਲੇਸ਼ਨ",
        "pitch_comp": "ਕੰਪਨੀ:",
        "pitch_serv": "ਸੇਵਾਵਾਂ:",
        "pitch_stim": "ਸਟਿਮੂਲੇਸ਼ਨ / ਟ੍ਰਿਗਰ:",
        "pitch_stim_hint": "ਜਿਵੇਂ: 'ਸੋਨੇ ਦੇ ਭਾਅ ਵਧੇ ਹਨ'",
        "pitch_ask": "ਲੋੜ (Ask):",
        "pitch_btn": "ਤਿਆਰ ਕਰੋ",
        "spinner_pitch": "ਤਿਆਰ ਹੋ ਰਹੀ ਹੈ...",
        "about": "ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਕਾਰੋਬਾਰਾਂ ਦੇ ਵਿਕਾਸ ਲਈ ਕੰਮ ਕਰਦੀ ਹੈ।",
        "footer": "ਨਿਰਮਾਣ: ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ"
    }
}

# साइडबार
with st.sidebar:
    st.markdown("### 🏛️ **विघ्नहर्ता गोल्ड फाउंडेशन**")
    st.caption("Empowering Entrepreneurs & Business Growth")
    
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

# Gemini REST API फंक्शन
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

    return "Server is busy right now. Please try again."

# मुख्य हेडर
st.markdown(f"**{t['initiative']}**")
st.title(t["title"])
st.subheader(t["subtitle"])
st.caption(t["caption"])

tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

# लॉगिन स्टेट
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

# टॅब २: 30-सेकंद पिच व स्टिम्युलेशन (Stimulation) जनरेटर
with tab2:
    st.write(f"### {t['pitch_title']}")
    b_name = st.text_input(t["pitch_comp"])
    b_serv = st.text_area(t["pitch_serv"])
    b_stim = st.text_input(t["pitch_stim"], placeholder=t["pitch_stim_hint"])
    b_ask = st.text_input(t["pitch_ask"])
    
    if st.button(t["pitch_btn"]):
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
                - Stimulation Theme / Specific Trigger: {b_stim if b_stim else "General customer pain point / conversation trigger"}
                - Specific Ask: {b_ask}
                
                Please generate a high-impact, professional networking presentation containing:
                1. **30-Second Speaking Pitch (३०-सेकंदांचा प्रभावी पिच)**:
                   - An attention-grabbing Opening Hook.
                   - Clear core value proposition in 2 lines.
                   - The clear Weekly Ask.
                   - Strong Memory Hook / Catchy Closing Tagline.
                   - Estimated timing: approx. 60-70 words.
                   
                2. **Referral Stimulation / Triggers (स्टिम्युलेशन - सदस्यांना तुमचे नाव कधी आठवावे?)**:
                   - "When you hear..." (जेव्हा तुम्ही मित्रांच्या/ग्राहकांच्या तोंडून हे शब्द ऐकाल...): Give 2-3 exact sentences people say in daily life.
                   - "Look for people who..." (अशा व्यक्ती शोधा ज्या...): 2 exact scenarios.
                   - "How to connect them to me" (त्यांना माझ्याशी कसे जोडावे - 1 simple intro tip).
                
                Format neatly using clear bullet points and bold headers in {selected_lang}.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.markdown(pitch_reply)

# अधिकृत तळटीप (Footer)
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
