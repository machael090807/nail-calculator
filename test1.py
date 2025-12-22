import streamlit as st
import datetime

# --- 設定網頁標題與介面 ---
st.set_page_config(page_title="Fairy.L 報價系統", page_icon="💅")

# ==========================================
# 👇 CSS 樣式設定區塊 👇
# ==========================================
custom_css = """
<style>
/* 1. 設定背景為奶茶色 */
.stApp {
    background-color: #F3E5D8; /* 淺奶茶色 */
}

/* 2. 設定全站主要文字顏色為深咖啡色 */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stRadio label {
    color: #4E342E !important; /* 深咖啡色 */
}

/* 讓上方標題列變透明 */
header[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

/* (選項) 調整輸入框與按鈕的邊框顏色 */
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input {
    border-color: #DCC7A1 !important;
}

/* 優化 Radio Button 的間距，讓手指比較好點 */
div[role="radiogroup"] > label {
    padding-top: 5px;
    padding-bottom: 5px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# ==========================================
# 👆 CSS 設定結束 👆
# ==========================================


st.title("💅 Fairy.L 報價計算機")
st.write("---")

# --- 輸入區塊 ---

# 1. 基礎服務 (改成 Radio 單選清單，解決下拉選單難收合的問題)
service_options = {
    "單色": 1000,
    "貓眼": 1100,
    "鏡面": 1300,
    "法式": 1500,
    "漸層": 1300
}
# 這裡把 st.selectbox 改成 st.radio
service_name = st.radio("基礎服務", list(service_options.keys())) 
service_price = service_options[service_name]

st.write("") # 空行間距

# 2. 位置
position = st.radio("位置", ["手部", "足部"], horizontal=True)
pos_price = 200 if position == "足部" else 0

st.write("") # 空行間距

# 3. 卸甲服務 (也改成 Radio，操作更順手)
remove_options = {
    "無": 0,
    "本店卸甲": 200,
    "他店卸甲": 300,
    "純卸甲": 500
}
# 這裡把 st.selectbox 改成 st.radio
remove_name = st.radio("卸甲服務", list(remove_options.keys()))
remove_price = remove_options[remove_name]

# 4. 加購項目
col1, col2 = st.columns(2)
with col1:
    st.write("")
    art_count = st.number_input("跳色數量 (指)", min_value=0, step=1)
    art_price = art_count * 100
with col2:
    addon_price = st.number_input("延甲/飾品金額 ($)", min_value=0, step=50)

# 5. 優惠
st.write("") 
is_birthday = st.toggle("🎂 壽星優惠 (9折)")

# --- 計算邏輯 ---
subtotal = service_price + pos_price + remove_price + art_price + addon_price
final_total = subtotal * 0.9 if is_birthday else subtotal

# --- 產生報價單文字 ---
date_str = datetime.date.today().strftime("%Y/%m/%d")
discount_text = " (已折抵壽星優惠)" if is_birthday else ""
remove_text = "無" if remove_name == "無" else remove_name

quote_text = f"""【Fairy. L NAIL ART 報價明細】
📅 日期：{date_str}
---------------------------
■ 項目：{service_name} ({position})
■ 卸甲：{remove_text}
■ 額外加購：${int(art_price + addon_price)}
---------------------------
💰 預估總額：${int(final_total)}{discount_text}
＊提醒：本店作品享有一週保固"""

# --- 顯示結果區 ---
st.write("---")
st.markdown(f"### 💰 總金額：`${int(final_total)}`")

st.text_area("報價單預覽", value=quote_text, height=200)

st.code(quote_text, language="text")
st.caption("👆 點擊右上角的複製圖示即可複製")
