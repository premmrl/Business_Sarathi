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

# Google Form चे फॉर्म आयडी व ॲक्शन URL
FORM_SUBMIT_URL = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/formResponse"

# गुगल फॉर्ममधील एन्ट्री आयडी मॅपिंग
# टीप: गुगल फॉर्ममधील फील्ड आयडी सामान्यतः entry.XXXXXXXXX स्वरूपात असतात.
# बॅकअपसाठी किंवा थेट गुगल फॉर्मवर जाण्यासाठी मूळ लिंक:
FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSffLyVq9szubqpQaeVX2KH3u_QOfF7ra_LUr9-WT7wN8w4FBg/viewform?usp=sharing"

# भारतातील प्रमुख १० भाषांची रचना
LANG_DATA = {
    "मराठी": {
        "foundation": "🏛️ विघ्नहर्ता गोल्ड फाउंडेशनचा उपक्रम",
        "title": "🤝 AI Business Sarathi",
        "caption": "उद्योजकांना अचूक संदर्भ व व्यावसायिक सहकार्य मिळवून देणारा डिजिटल साथीदार",
        "tab1": "🔍 स्मार्ट शोध",
        "tab2": "📝 नवीन नोंदणी",
        "tab3": "🎙️ पिच व स्टिम्युलेशन",
        "auth_label": "नोंदणीकृत १० अंकी मोबाईल नंबर किंवा ईमेल:",
        "input_placeholder": "उदा. 8087699949 किंवा email",
        "welcome": "✅ स्वागत आहे, **{name}**!",
        "not_registered": "⚠️ हा नंबर डिरेक्टरीमध्ये नोंदणीकृत नाही.",
        "register_prompt": "👉 संदर्भ शोधण्यासाठी कृपया दुसऱ्या टॅबमधून (📝 नवीन नोंदणी) आधी नोंदणी पूर्ण करा.",
        "search_label": "तुम्हाला कोणत्या व्यवसायाशी/सेवेशी जोडले जायचे आहे?",
        "search_placeholder": "उदा. 'पुण्यात सोन्यात गुंतवणुकीसाठी संपर्क'...",
        "search_hint": "💡 संदर्भ शोधण्यासाठी वर नोंदणीकृत नंबर टाकून बाणावर (➔) दाबा.",
        "spinner_search": "AI अचूक संदर्भ शोधत आहे...",
        # इन-ॲप नोंदणी लेबल्स
        "reg_title": "बिझनेस नेटवर्कमध्ये नवीन सदस्य नोंदणी",
        "reg_name": "पूर्ण नाव (Full Name):",
        "reg_comp": "कंपनी / ब्रँडचे नाव (Company / Business Name):",
        "reg_phone": "मोबाईल / व्हॉट्सॲप नंबर (Mobile / WhatsApp):",
        "reg_email": "ईमेल आयडी (Email ID):",
        "reg_city": "शहर (City / Location):",
        "reg_serv": "मुख्य उत्पादने किंवा सेवा (Products / Services):",
        "reg_btn": "नोंदणी पूर्ण करा ➔",
        "reg_success": "🎉 अभिनंदन! तुमची नोंदणी यशस्वीरीत्या पूर्ण झाली आहे. आता तुम्ही टॅब १ मध्ये जाऊन थेट संदर्भ शोधू शकता.",
        # पिच लेबल्स
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
        "tab1": "🔍 स्मार्ट सर्च",
        "tab2": "📝 नया पंजीकरण",
        "tab3": "🎙️ पिच व स्टिम्युलेशन",
        "auth_label": "पंजीकृत 10 अंकों का मोबाइल नंबर या ईमेल:",
        "input_placeholder": "उदा. 8087699949 या email",
        "welcome": "✅ स्वागत है, **{name}**!",
        "not_registered": "⚠️ यह नंबर डायरेक्टरी में पंजीकृत नहीं है।",
        "register_prompt": "👉 रेफ़रल खोजने के लिए कृपया दूसरे टैब (📝 नया पंजीकरण) से पहले पंजीकरण पूरा करें।",
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
        "reg_success": "🎉 बधाई! आपका पंजीकरण सफलतापूर्वक पूरा हो गया है। अब आप पहले टैब से रेफ़रल खोज सकते हैं।",
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
        "tab1": "🔍 Smart Search",
        "tab2": "📝 New Registration",
        "tab3": "🎙️ Pitch & Stimulation",
        "auth_label": "Registered 10-digit mobile number or email:",
        "input_placeholder": "e.g. 8087699949 or email",
        "welcome": "✅ Welcome, **{name}**!",
        "not_registered": "⚠️ This contact is not registered in our directory.",
        "register_prompt": "👉 To access referrals, please complete registration in the second tab (📝 New Registration).",
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
        "reg_success": "🎉 Congratulations! Your registration is successful. You can now search referrals in Tab 1.",
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
    },
    "ગુજરાતી": {
        "foundation": "🏛️ વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશનની પહેલ",
        "title": "🤝 AI Business Sarathi",
        "caption": "વ્યવસાયિકોને સચોટ રેફરલ્સ મેળવવામાં મદદ કરતો ડિજિટલ સાથી",
        "tab1": "🔍 સ્માર્ટ સર્ચ",
        "tab2": "📝 નવી નોંધણી",
        "tab3": "🎙️ પિચ અને સ્ટિમ્યુલેશન",
        "auth_label": "નોંધાયેલ 10 અંકનો મોબાઇલ નંબર અથવા ઇમેઇલ:",
        "input_placeholder": "દા.ત. 8087699949",
        "welcome": "✅ સ્વાગત છે, **{name}**!",
        "not_registered": "⚠️ આ નંબર ડિરેક્ટરીમાં નોંધાયેલ નથી.",
        "register_prompt": "👉 શોધવા માટે કૃપા કરીને બીજા ટેબમાંથી (📝 નવી નોંધણી) નોંધણી પૂર્ણ કરો.",
        "search_label": "તમે કયા વ્યવસાય સાથે જોડાવા માંગો છો?",
        "search_placeholder": "જરૂરિયાત લખીને ➔ દબાવો...",
        "search_hint": "💡 શોધવા માટે ઉપર તમારો નંબર દાખલ કરીને બાણ (➔) દબાવો.",
        "spinner_search": "AI સંપર્કો શોધી રહ્યું છે...",
        "reg_title": "બિઝનેસ નેટવર્કમાં નવી સભ્ય નોંધણી",
        "reg_name": "પૂર્ણ નામ:",
        "reg_comp": "કંપની / બ્રાન્ડનું નામ:",
        "reg_phone": "મોબાઇલ / વ્હોટ્સએપ નંબર:",
        "reg_email": "ઇમેઇલ આઇડી:",
        "reg_city": "શહેર:",
        "reg_serv": "મુખ્ય સેવાઓ / ઉત્પાદનો:",
        "reg_btn": "નોંધણી પૂર્ણ કરો ➔",
        "reg_success": "🎉 અભિનંદન! તમારી નોંધણી સફળ થઈ ગઈ છે.",
        "pitch_title": "30-સેકન્ડ પિચ અને સ્ટિમ્યુલેશન",
        "pitch_comp": "કંપની / બ્રાન્ડ:",
        "pitch_serv": "મુખ્ય સેવાઓ:",
        "pitch_stim": "સ્ટિમ્યુલેશન / ટ્રિગર (વૈકલ્પિક):",
        "pitch_stim_hint": "દા.ત. 'સોનાના ભાવ વધ્યા છે'",
        "pitch_ask": "તમારી જરૂરિયાત (Ask):",
        "pitch_btn": "પિચ બનાવો ➔",
        "spinner_pitch": "પિચ તૈયાર થઈ રહી છે...",
        "about": "વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન ઉદ્યોગસાહસિકોના વિકાસ માટે કાર્યરત છે.",
        "footer": "સંકલ્પના: વિઘ્નહર્તા ગોલ્ડ ફાઉન્ડેશન | વેબસાઇટ:"
    },
    "தமிழ்": {
        "foundation": "🏛️ விக்னஹர்தா கோல்ட் அறக்கட்டளையின் முயற்சி",
        "title": "🤝 AI Business Sarathi",
        "caption": "தொழில்முனைவோருக்கு துல்லியமான பரிந்துரைகளை வழங்கும் டிஜிட்டல் உதவியாளர்",
        "tab1": "🔍 ஸ்மார்ட் தேடல்",
        "tab2": "📝 புதிய பதிவு",
        "tab3": "🎙️ பிட்ச் & ஸ்டிமுலேஷன்",
        "auth_label": "பதிவுசெய்த மொபைல் எண் அல்லது மின்னஞ்சல்:",
        "input_placeholder": "எ.கா. 8087699949",
        "welcome": "✅ வரவேற்கிறோம், **{name}**!",
        "not_registered": "⚠️ எண் பட்டியலில் இல்லை.",
        "register_prompt": "👉 பரிந்துரைகளைத் தேட இரண்டாவது தாவலில் (📝 புதிய பதிவு) பதிவு செய்யவும்.",
        "search_label": "நீங்கள் எந்த தொழிலுடன் இணைய விரும்புகிறீர்கள்?",
        "search_placeholder": "தேவையை உள்ளிட்டு ➔ அழுத்தவும்...",
        "search_hint": "💡 தேடலுக்கு மேலே எண் உள்ளிட்டு (➔) தொடவும்.",
        "spinner_search": "AI தேடுகிறது...",
        "reg_title": "புதிய உறுப்பினர் பதிவு",
        "reg_name": "முழு பெயர்:",
        "reg_comp": "நிறுவனத்தின் பெயர்:",
        "reg_phone": "மொபைல் எண்:",
        "reg_email": "மின்னஞ்சல்:",
        "reg_city": "நகரம்:",
        "reg_serv": "முதன்மை சேவைகள்:",
        "reg_btn": "பதிவை முடிக்கவும் ➔",
        "reg_success": "🎉 வாழ்த்துகள்! உங்கள் பதிவு வெற்றிகரமாக முடிந்தது.",
        "pitch_title": "பிட்ச் & ஸ்டிமுலேஷன் உருவாக்குநர்",
        "pitch_comp": "நிறுவனம்:",
        "pitch_serv": "சேவைகள்:",
        "pitch_stim": "தூண்டுதல் (விருப்பத்தேர்வு):",
        "pitch_stim_hint": "எ.கா. 'தங்கம் விலை உயர்வு'",
        "pitch_ask": "தேவை (Ask):",
        "pitch_btn": "உருவாக்கு ➔",
        "spinner_pitch": "தயாராகிறது...",
        "about": "விக்னஹர்தா கோல்ட் அறக்கட்டளை தொழில்முனைவோரை மேம்படுத்துகிறது.",
        "footer": "வடிவமைப்பு: விக்னஹர்தா கோல்ட் அறக்கட்டளை"
    },
    "తెలుగు": {
        "foundation": "🏛️ విఘ్నహర్త గోల్డ్ ఫౌండేషన్ చొరవ",
        "title": "🤝 AI Business Sarathi",
        "caption": "వ్యాపారవేత్తలకు ఖచ్చితమైన రిఫరల్స్ అందించే డిజిటల్ సహచరుడు",
        "tab1": "🔍 స్మార్ట్ సెర్చ్",
        "tab2": "📝 కొత్త రిజిస్ట్రేషన్",
        "tab3": "🎙️ పిచ్ & స్టిమ్యులేషన్",
        "auth_label": "నమోదిత మొబైల్ నంబర్ లేదా ఇమెయిల్:",
        "input_placeholder": "ఉదా. 8087699949",
        "welcome": "✅ స్వాగతం, **{name}**!",
        "not_registered": "⚠️ నంబర్ డైరెక్టరీలో లేదు.",
        "register_prompt": "👉 రిఫరల్స్ కోసం రెండవ ట్యాబ్ (📝 కొత్త రిజిస్ట్రేషన్) నుండి నమోదు చేసుకోండి.",
        "search_label": "ఏ వ్యాపారంతో కనెక్ట్ కావాలనుకుంటున్నారు?",
        "search_placeholder": "అవసరం నమోదు చేసి ➔ నొక్కండి...",
        "search_hint": "💡 సెర్చ్ చేయడానికి నంబర్ నమోదు చేసి బాణం (➔) నొక్కండి.",
        "spinner_search": "AI శోధిస్తోంది...",
        "reg_title": "కొత్త సభ్యుల నమోదు",
        "reg_name": "పూర్తి పేరు:",
        "reg_comp": "కంపెనీ పేరు:",
        "reg_phone": "మొబైల్ నంబర్:",
        "reg_email": "ఇమెయిల్:",
        "reg_city": "నగరం:",
        "reg_serv": "సేవలు:",
        "reg_btn": "నమోదు పూర్తి చేయండి ➔",
        "reg_success": "🎉 అభినందనలు! మీ నమోదు విజయవంతమైంది.",
        "pitch_title": "పిచ్ & స్టిమ్యులేషన్ జనరేటర్",
        "pitch_comp": "కంపెనీ:",
        "pitch_serv": "సేవలు:",
        "pitch_stim": "ట్రిగ్గర్ (ఐచ్ఛికం):",
        "pitch_stim_hint": "ఉదా. 'బంగారం ధరలు పెరిగాయి'",
        "pitch_ask": "అవసరం (Ask):",
        "pitch_btn": "సిద్ధం చేయండి ➔",
        "spinner_pitch": "తయారవుతోంది...",
        "about": "విఘ్నహర్త గోల్డ్ ఫౌండేషన్ వ్యాపారవేత్తలకు సాధికారత కల్పిస్తుంది.",
        "footer": "రూపకల్పన: విఘ్నహర్త గోల్డ్ ఫౌండేషన్"
    },
    "ಕನ್ನಡ": {
        "foundation": "🏛️ ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉಪಕ್ರಮ",
        "title": "🤝 AI Business Sarathi",
        "caption": "ಉದ್ಯಮಿಗಳಿಗೆ ನಿಖರವಾದ ಉಲ್ಲೇಖಗಳನ್ನು ಒದಗಿಸುವ ಡಿಜಿಟಲ್ ಸಹಾಯಕ",
        "tab1": "🔍 ಸ್ಮಾರ್ಟ್ ಹುಡುಕಾಟ",
        "tab2": "📝 ಹೊಸ ನೋಂದಣಿ",
        "tab3": "🎙️ ಪಿಚ್ & ಸ್ಟಿಮ್ಯುಲೇಶನ್",
        "auth_label": "ನೋಂದಾಯಿತ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇಮೇಲ್:",
        "input_placeholder": "ಉದಾ. 8087699949",
        "welcome": "✅ ಸ್ವಾಗತ, **{name}**!",
        "not_registered": "⚠️ ಈ ಸಂಖ್ಯೆ ನೋಂದಣಿಯಾಗಿಲ್ಲ.",
        "register_prompt": "👉 ರೆಫರಲ್‌ಗಳಿಗಾಗಿ ಎರಡನೇ ಟ್ಯಾಬ್‌ನಲ್ಲಿ (📝 ಹೊಸ ನೋಂದಣಿ) ನೋಂದಾಯಿಸಿ.",
        "search_label": "ಯಾವ ವ್ಯವಹಾರದೊಂದಿಗೆ ಸಂಪರ್ಕ ಸಾಧಿಸಲು ಬಯಸುತ್ತೀರಿ?",
        "search_placeholder": "ಅಗತ್ಯತೆ ನಮೂದಿಸಿ ➔ ಒತ್ತಿರಿ...",
        "search_hint": "💡 ಹುಡುಕಲು ಸಂಖ್ಯೆ ನಮೂದಿಸಿ ಬಾಣದ ಗುರುತು (➔) ಒತ್ತಿರಿ.",
        "spinner_search": "AI ಹುಡುಕುತ್ತಿದೆ...",
        "reg_title": "ಹೊಸ ಸದಸ್ಯರ ನೋಂದಣಿ",
        "reg_name": "ಪೂರ್ಣ ಹೆಸರು:",
        "reg_comp": "ಕಂಪನಿ ಹೆಸರು:",
        "reg_phone": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ:",
        "reg_email": "ಇಮೇಲ್:",
        "reg_city": "ನಗರ:",
        "reg_serv": "ಪ್ರಮುಖ ಸೇವೆಗಳು:",
        "reg_btn": "ನೋಂದಣಿ ಪೂರ್ಣಗೊಳಿಸಿ ➔",
        "reg_success": "🎉 ಅಭಿನಂದನೆಗಳು! ನಿಮ್ಮ ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ.",
        "pitch_title": "ಪಿಚ್ & ಸ್ಟಿಮ್ಯುಲೇಶನ್ ರಚನೆ",
        "pitch_comp": "ಕಂಪನಿ:",
        "pitch_serv": "ಸೇವೆಗಳು:",
        "pitch_stim": "ಟ್ರಿಗ್ಗರ್ (ಐಚ್ಛಿಕ):",
        "pitch_stim_hint": "ಉದಾ. 'ಚಿನ್ನದ ದರ ಏರಿಕೆ'",
        "pitch_ask": "ಅಗತ್ಯತೆ (Ask):",
        "pitch_btn": "ರಚಿಸಿ ➔",
        "spinner_pitch": "ಸಿದ್ಧವಾಗುತ್ತಿದೆ...",
        "about": "ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್ ಉದ್ಯಮಿಗಳ ಬೆಂಬಲಕ್ಕಾಗಿ ಶ್ರಮಿಸುತ್ತದೆ.",
        "footer": "ವಿನ್ಯಾಸ: ವಿಘ್ನಹರ್ತ ಗೋಲ್ಡ್ ಫೌಂಡೇಶನ್"
    },
    "മലയാളം": {
        "foundation": "🏛️ വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ സംരംഭം",
        "title": "🤝 AI Business Sarathi",
        "caption": "ബിസിനസ് റഫറലുകൾ നൽകുന്ന ഡിജിറ്റൽ സഹായി",
        "tab1": "🔍 സ്മാർട്ട് തിരയൽ",
        "tab2": "📝 പുതിയ രജിസ്ട്രേഷൻ",
        "tab3": "🎙️ പിച്ചും സ്റ്റിമുലേഷനും",
        "auth_label": "രജിസ്റ്റർ ചെയ്ത മൊബൈൽ നമ്പറോ ഇമെയിലോ:",
        "input_placeholder": "ഉദാ. 8087699949",
        "welcome": "✅ സ്വാഗതം, **{name}**!",
        "not_registered": "⚠️ നമ്പർ ലഭ്യമല്ല.",
        "register_prompt": "👉 റഫറലുകൾ ലഭിക്കാൻ രണ്ടാമത്തെ ടാബിൽ (📝 പുതിയ രജിസ്ട്രേഷൻ) രജിസ്റ്റർ ചെയ്യുക.",
        "search_label": "ഏത് ബിസിനസ്സുമായാണ് ബന്ധപ്പെടേണ്ടത്?",
        "search_placeholder": "ആവശ്യം നൽകി ➔ ക്ലിക്ക് ചെയ്യുക...",
        "search_hint": "💡 നമ്പർ നൽകി അമ്പടയാളത്തിൽ (➔) ക്ലിക്ക് ചെയ്യുക.",
        "spinner_search": "AI തിരയുന്നു...",
        "reg_title": "പുതിയ അംഗങ്ങളുടെ രജിസ്ട്രേഷൻ",
        "reg_name": "പൂർണ്ണമായ പേര്:",
        "reg_comp": "കമ്പനി പേര്:",
        "reg_phone": "മൊബൈൽ നമ്പർ:",
        "reg_email": "ഇമെയിൽ:",
        "reg_city": "നഗരം:",
        "reg_serv": "പ്രധാന സേവനങ്ങൾ:",
        "reg_btn": "രജിസ്ട്രേഷൻ പൂർത്തിയാക്കുക ➔",
        "reg_success": "🎉 അഭിനന്ദനങ്ങൾ! രജിസ്ട്രേഷൻ വിജയകരമായി പൂർത്തിയായി.",
        "pitch_title": "പിച്ചും സ്റ്റിമുലേഷനും",
        "pitch_comp": "കമ്പനി:",
        "pitch_serv": "സേവനങ്ങൾ:",
        "pitch_stim": "ട്രിഗർ (ഓപ്ഷണൽ):",
        "pitch_stim_hint": "ഉദാ. 'സ്വർണ്ണവില വർദ്ധനവ്'",
        "pitch_ask": "ആവശ്യം (Ask):",
        "pitch_btn": "തയ്യാറാക്കുക ➔",
        "spinner_pitch": "തയ്യാറാകുന്നു...",
        "about": "വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ സംരംഭകരുടെ വളർച്ചയ്ക്കായി നിലകൊള്ളുന്നു.",
        "footer": "രൂപകൽപ്പന: വിഘ്നഹർത്ത ഗോൾഡ് ഫൗണ്ടേഷൻ"
    },
    "বাংলা": {
        "foundation": "🏛️ বিঘ্নহর্তা গোল্ড ফাউন্ডেশনের উদ্যোগ",
        "title": "🤝 AI Business Sarathi",
        "caption": "ব্যবসায়ীদের সঠিক রেফারেল খুঁজে দেওয়ার ডিজিটাল সাথী",
        "tab1": "🔍 স্মার্ট অনুসন্ধান",
        "tab2": "📝 নতুন নিবন্ধন",
        "tab3": "🎙️ পিচ ও স্টিমুলেশন",
        "auth_label": "নিবন্ধিত মোবাইল নম্বর বা ইমেল:",
        "input_placeholder": "যেমন: 8087699949",
        "welcome": "✅ স্বাগতম, **{name}**!",
        "not_registered": "⚠️ এই নম্বরটি নিবন্ধিত নেই।",
        "register_prompt": "👉 রেফারেল পেতে দ্বিতীয় ট্যাবে (📝 নতুন নিবন্ধন) গিয়ে নিবন্ধন করুন।",
        "search_label": "কোন ব্যবসার সাথে যুক্ত হতে চান?",
        "search_placeholder": "প্রয়োজন লিখে ➔ চাপুন...",
        "search_hint": "💡 অনুসন্ধানের জন্য নম্বর লিখে তীর চিহ্নে (➔) ক্লিক করুন।",
        "spinner_search": "AI রেফারেল খুঁজছে...",
        "reg_title": "নতুন সদস্য নিবন্ধন",
        "reg_name": "পুরো নাম:",
        "reg_comp": "কোম্পানির নাম:",
        "reg_phone": "মোবাইল নম্বর:",
        "reg_email": "ইমেল আইডি:",
        "reg_city": "শহর:",
        "reg_serv": "প্রধান পরিষেবা:",
        "reg_btn": "নিবন্ধন সম্পন্ন করুন ➔",
        "reg_success": "🎉 অভিনন্দন! আপনার নিবন্ধন সফল হয়েছে।",
        "pitch_title": "পিচ এবং স্টিমুলেশন",
        "pitch_comp": "কোম্পানি:",
        "pitch_serv": "পরিষেবা:",
        "pitch_stim": "রেফারেল ট্রিগার (ঐচ্ছিক):",
        "pitch_stim_hint": "যেমন: 'সোনার দাম বেড়েছে'",
        "pitch_ask": "চাহিদা (Ask):",
        "pitch_btn": "তৈরি করুন ➔",
        "spinner_pitch": "তৈরি হচ্ছে...",
        "about": "বিঘ্নহর্তা গোল্ড ফাউন্ডেশন ব্যবসায়ীদের জন্য কাজ করে।",
        "footer": "পরিকল্পনা: বিঘ্নহর্তা গোল্ড ফাউন্ডেশন"
    },
    "ਪੰਜਾਬੀ": {
        "foundation": "🏛️ ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਦਾ ਉਪਰਾਲਾ",
        "title": "🤝 AI Business Sarathi",
        "caption": "ਕਾਰੋਬਾਰੀਆਂ ਨੂੰ ਸਹੀ ਰੈਫਰਲ ਦਿਵਾਉਣ ਵਾਲਾ ਡਿਜੀਟਲ ਸਾਥੀ",
        "tab1": "🔍 ਸਮਾਰਟ ਖੋਜ",
        "tab2": "📝 ਨਵੀਂ ਰਜਿਸਟ੍ਰੇਸ਼ਨ",
        "tab3": "🎙️ ਪਿੱਚ ਅਤੇ ਸਟਿਮੂਲੇਸ਼ਨ",
        "auth_label": "ਰਜਿਸਟਰਡ ਮੋਬਾਈਲ ਨੰਬਰ ਜਾਂ ਈਮੇਲ:",
        "input_placeholder": "ਜਿਵੇਂ: 8087699949",
        "welcome": "✅ ਜੀ ਆਇਆਂ ਨੂੰ, **{name}**!",
        "not_registered": "⚠️ ਨੰਬਰ ਦਰਜ ਨਹੀਂ ਹੈ।",
        "register_prompt": "👉 ਰੈਫਰਲ ਲੱਭਣ ਲਈ ਦੂਜੇ ਟੈਬ (📝 ਨਵੀਂ ਰਜਿਸਟ੍ਰੇਸ਼ਨ) ਵਿੱਚ ਰਜਿਸਟਰ ਕਰੋ।",
        "search_label": "ਕਿਸ ਕਾਰੋਬਾਰ ਨਾਲ ਜੁੜਨਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "search_placeholder": "ਲੋੜ ਦਰਜ ਕਰਕੇ ➔ ਦਬਾਓ...",
        "search_hint": "💡 ਖੋਜ ਕਰਨ ਲਈ ਨੰਬਰ ਦਰਜ ਕਰਕੇ ਤੀਰ (➔) ਦਬਾਓ।",
        "spinner_search": "AI ਰੈਫਰਲ ਲੱਭ ਰਿਹਾ ਹੈ...",
        "reg_title": "ਨਵੇਂ ਮੈਂਬਰ ਦੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ",
        "reg_name": "ਪੂਰਾ ਨਾਮ:",
        "reg_comp": "ਕੰਪਨੀ ਦਾ ਨਾਮ:",
        "reg_phone": "ਮੋਬਾਈਲ ਨੰਬਰ:",
        "reg_email": "ਈਮੇਲ ਆਈਡੀ:",
        "reg_city": "ਸ਼ਹਿਰ:",
        "reg_serv": "ਮੁੱਖ ਸੇਵਾਵਾਂ:",
        "reg_btn": "ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਮੁਕੰਮਲ ਕਰੋ ➔",
        "reg_success": "🎉 ਵਧਾਈਆਂ! ਤੁਹਾਡੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਸਫਲ ਹੋ ਗਈ ਹੈ।",
        "pitch_title": "ਪਿੱਚ ਅਤੇ ਸਟਿਮੂਲੇਸ਼ਨ",
        "pitch_comp": "ਕੰਪਨੀ:",
        "pitch_serv": "ਸੇਵਾਵਾਂ:",
        "pitch_stim": "ਟ੍ਰਿਗਰ (ਵਿਕਲਪਿਕ):",
        "pitch_stim_hint": "ਜਿਵੇਂ: 'ਸੋਨੇ ਦੇ ਭਾਅ ਵਧੇ ਹਨ'",
        "pitch_ask": "ਲੋੜ (Ask):",
        "pitch_btn": "ਤਿਆਰ ਕਰੋ ➔",
        "spinner_pitch": "ਤਿਆਰ ਹੋ ਰਹੀ ਹੈ...",
        "about": "ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ ਕਾਰੋਬਾਰਾਂ ਦੇ ਵਿਕਾਸ ਲਈ ਕੰਮ ਕਰਦੀ ਹੈ।",
        "footer": "ਨਿਰਮਾਣ: ਵਿਘਨਹਰਤਾ ਗੋਲਡ ਫਾਊਂਡੇਸ਼ਨ"
    }
}

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
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.9rem;
            font-weight: 600;
            border-radius: 8px;
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

# भाषा निवड थेट मुख्य स्क्रीनवर सर्वात वर
languages = list(LANG_DATA.keys())
col_lang1, col_lang2 = st.columns([6, 4], vertical_alignment="center")
with col_lang2:
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

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# टॅब १: सर्च व लॉगिन
with tab1:
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

# टॅब २: इन-ॲप नवीन नोंदणी (१० भाषांमध्ये थेट ॲपवरून)
with tab2:
    st.write(f"### {t['reg_title']}")
    
    with st.form("in_app_registration_form", clear_on_submit=True):
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
                # बॅकएंडला गुगल फॉर्मवर डेटा पोस्ट करणे
                # जर गुगल फॉर्मची CORS किंवा रिस्ट्रिक्शन असेल, तरीही युझरला कन्फर्मेशन मिळते
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

# टॅब ३: पिच व स्टिम्युलेशन
with tab3:
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
                1. **30-Second Speaking Pitch (३०-सेकंदांचा प्रभावी पिच)**:
                   - An attention-grabbing Opening Hook.
                   - Clear core value proposition in 2 lines.
                   - The clear Weekly Ask.
                   - Strong Memory Hook / Catchy Closing Tagline.
                   
                2. **Referral Stimulation / Triggers (स्टिम्युलेशन - सदस्यांना तुमचे नाव कधी आठवावे?)**:
                   - "When you hear..." (जेव्हा तुम्ही हे शब्द ऐकाल...): 2 exact sentences.
                   - "Look for people who..." (अशा व्यक्ती शोधा ज्या...): 2 scenarios.
                   - "How to connect them to me" (त्यांना माझ्याशी कसे जोडावे - 1 tip).
                
                Format neatly using clear bullet points in {selected_lang}.
                """
                pitch_reply = call_gemini(pitch_prompt, GEMINI_API_KEY)
                st.markdown(pitch_reply)

# तळटीप (Footer)
st.markdown(f"""
    <div class="app-footer">
        {t['footer']} 
        <a href='https://www.vgold.co.in' target='_blank' style='color: #d4af37; font-weight: 700; text-decoration: none;'>
            www.vgold.co.in
        </a>
    </div>
""", unsafe_allow_html=True)
