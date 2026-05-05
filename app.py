import streamlit as st
import matplotlib.pyplot as plt

# إعداد الصفحة لتكون واسعة واحترافية
st.set_page_config(page_title="HUE - Student Success Prediction", page_icon="🎓", layout="centered")

# إضافة التصميم (Styling) الخاص بالموقع بألوان هادئة
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A;
        color: #FFFFFF;
    }
    h1, h2, h3, h4, label, p, .stMarkdown, .stWarning, .stSuccess, .stError {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #FFFFFF !important;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# القاموس الخاص باللغات
translations = {
    "ar": {
        "university": "جامعة حورس - HUE | كلية الذكاء الاصطناعي",
        "title": "نظام التنبؤ بنجاح الطلاب",
        "login_title": "تسجيل الدخول",
        "name_label": "اسم الطالب:",
        "id_label": "الرقم الجامعي:",
        "login_btn": "دخول",
        "logout_btn": "تسجيل الخروج",
        "input_header": "أدخل بيانات الطالب للتنبؤ",
        "hours_label": "عدد ساعات الدراسة (أسبوعياً):",
        "attendance_label": "نسبة الحضور (%):",
        "grade_label": "الدرجة السابقة (%):",
        "predict_btn": "توقع النتيجة 🚀",
        "result_pass": "النتيجة المتوقعة: ناجح 🎓",
        "result_fail": "النتيجة المتوقعة: راسب ⚠️",
        "chart_success": "Success",
        "chart_fail": "Failure",
        "team_text": "الفريق: كريم وليد (الليدر) 8251536 | عمر حسن 8241388 | عبد الرحمن محمد 8251537 | أحمد وليد 8251755 | أنس رضا 8251689"
    },
    "en": {
        "university": "Horus University Egypt - HUE",
        "title": "Student Success Prediction System",
        "login_title": "Login",
        "name_label": "Student Name:",
        "id_label": "University ID:",
        "login_btn": "Login",
        "logout_btn": "Logout",
        "input_header": "Enter Student Information",
        "hours_label": "Study Hours (Weekly):",
        "attendance_label": "Attendance (%):",
        "grade_label": "Previous Grade (%):",
        "predict_btn": "Predict Result 🚀",
        "result_pass": "Predicted Result: Pass 🎓",
        "result_fail": "Predicted Result: Fail ⚠️",
        "chart_success": "Success",
        "chart_fail": "Failure",
        "team_text": "Team: Kareem Waleed (Leader) 8251536 | Omar Hassan 8241388 | Abdulrahman Mohamed 8251537 | Ahmed Waleed 8251755 | Anas Reda 8251689"
    }
}

# إدارة الحالات (Session State) للحفاظ على البيانات والتسجيل
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

# 1. شريط اختيار اللغة في الأعلى
st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
lang_selection = st.radio("🌐 Language / اللغة", ["العربية", "English"], horizontal=True, index=0 if st.session_state.lang == "ar" else 1)
st.session_state.lang = "ar" if lang_selection == "العربية" else "en"
st.markdown("</div>", unsafe_allow_html=True)

t = translations[st.session_state.lang]

# العنوان الرئيسي للجامعة
st.markdown(f"<h3 style='text-align: center; color: #38BDF8;'>{t['university']}</h3>", unsafe_allow_html=True)

# 2. صفحة تسجيل الدخول
if not st.session_state.logged_in:
    st.markdown(f"<h2 style='text-align: center; margin-top: 30px;'>{t['login_title']}</h2>", unsafe_allow_html=True)
    
    name = st.text_input(t['name_label'])
    id_num = st.text_input(t['id_label'])
    
    if st.button(t['login_btn']):
        if name and id_num:
            st.session_state.logged_in = True
            st.session_state.name = name
            st.session_state.id = id_num
            st.rerun()
        else:
            if st.session_state.lang == "ar":
                st.warning("⚠️ يرجى إدخال اسم الطالب والرقم الجامعي.")
            else:
                st.warning("⚠️ Please enter both Name and University ID.")

# 3. الصفحة الرئيسية للموقع (بعد تسجيل الدخول)
else:
    st.markdown(f"<h1 style='text-align: center; margin-top: 20px;'>{t['title']}</h1>", unsafe_allow_html=True)
    st.write(f"**Welcome/مرحباً:** {st.session_state.name} | ID: {st.session_state.id}")
    st.markdown("---")
    
    st.subheader(t['input_header'])
    
    hours = st.number_input(t['hours_label'], min_value=0.0, max_value=24.0, value=5.0, step=0.5)
    attendance = st.number_input(t['attendance_label'], min_value=0.0, max_value=100.0, value=85.0, step=1.0)
    grade = st.number_input(t['grade_label'], min_value=0.0, max_value=100.0, value=70.0, step=1.0)
    
    if st.button(t['predict_btn']):
        # خوارزمية التنبؤ بنجاح الطالب
        prob_score = (min(hours, 10) / 10 * 0.4) + (attendance / 100 * 0.4) + (grade / 100 * 0.2)
        success_prob = prob_score * 100
        fail_prob = 100 - success_prob
        
        if success_prob >= 60:
            st.success(f"{t['result_pass']} - {success_prob:.1f}%")
        else:
            st.error(f"{t['result_fail']} - {success_prob:.1f}%")
            
        # رسم المخطط البياني (Pie Chart) 
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.patch.set_facecolor('#0F172A')
        ax.set_facecolor('#0F172A')
        
        labels = [t['chart_success'], t['chart_fail']]
        sizes = [success_prob, fail_prob]
        colors = ['#10B981', '#EF4444']
        
        ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            colors=colors, 
            startangle=140, 
            textprops={'fontsize': 10, 'color': 'white'}
        )
        ax.axis('equal')
        st.pyplot(fig)
        
    st.markdown("---")
    
    # أسماء الفريق
    st.caption(f"{t['team_text']}")
    
    if st.button(t['logout_btn']):
        st.session_state.logged_in = False
        st.rerun()
