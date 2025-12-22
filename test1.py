import streamlit as st
import datetime

# ==========================================
# 1. 設定 App 圖示
# ==========================================
icon_url = "https://raw.githubusercontent.com/machael090807/nail-calculator/07e29efbbce9832dec754699d7a2afdc9660c024/2025-12-22%2019.08.45.jpg"

st.set_page_config(page_title="Fairy.L 報價系統", page_icon=icon_url)

st.markdown(
    f"""
    <head>
        <link rel="apple-touch-icon" href="{icon_url}">
    </head>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 2. CSS 美化設定 (奶茶色 + 隱藏所有選單按鈕)
# ==========================================
custom_css = """
<style>
/* 設定背景為奶茶色 */
.stApp {
    background-color: #F3E5D8;
}

/* 設定全站主要文字顏色為深咖啡色 */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stRadio label, .stCheckbox label, .stToggle label {
    color: #4E342E !important;
}

/* 標題響應式設定 */
h1 {
    text-align: center !important;
    font-size: clamp(1.5rem, 6vw, 2.5rem) !important; 
    padding-bottom: 10px;
    white-space: nowrap;
}

/* 👇👇👇 新增：隱藏上方工具列 (Fork按鈕) 與下方 Footer (Logo) 👇👇👇 */

/* 1. 隱藏最上方的 Header (包含 Fork 按鈕、Deploy 按鈕、三條線選單) */
header[data-testid="stHeader"] {
    display: none !important;
}

/* 2. 隱藏最下方的 Footer (Made with Streamlit) */
footer {
    display: none !important;
}

/* 3. 隱藏主選單 (雙重保險) */
#MainMenu {
    visibility: hidden;
}

/* 4. 隱藏右下角的 viewer badge (如果有的話) */
.viewerBadge_container__1QSob {
    display: none !important;
}

/* 👆👆👆 隱藏設定結束 👆👆👆 */


/* 調整輸入框與按鈕的邊框顏色 */
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-color: #DCC7A1 !important;
}

/* 優化選單間距 */
div[role="radiogroup"] > label, div[data-testid="stCheckbox"] label {
    padding-top: 5px;
    padding-bottom: 5px;
}

/* 隱藏數字輸入框的 +/- 按鈕 */
[data-testid="stNumberInput"] button {
    display: none !important;
}
[data-testid="stNumberInput"] input {
    text-align: center;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# 3. 介面與輸入區塊
# ==========================================
st.title("💅 Fairy.L 報價計算機") 
st.write("---")

# --- 基礎服務 ---
service_options = {
    "單色": 1000,
    "貓眼": 1100,
    "鏡面": 1300,
    "法式": 1500,
    "漸層": 1300
}
service_name = st.radio("基礎服務", list(service_options.keys())) 
service_unit_price = service_options[service_name]

st.write("") 

# --- 位置 ---
st.write("位置 (可複選)")
col_p1, col_p2 = st.columns(2)
with col_p1:
    pos_hand = st.checkbox("手部", value=True)
with col_p2:
    pos_foot = st.checkbox("足部 (+200)")

# 位置邏輯
selected_pos = []
if pos_hand: selected_pos.append("手部")
if pos_foot: selected_pos.append("足部")
pos_count = len(selected_pos)
pos_surcharge = 200 if pos_foot else 0 

st.write("") 

# --- 卸甲服務 ---
remove_options = {
    "無": 0,
    "本店卸甲": 200,
    "他店卸甲": 300,
    "純卸甲": 500
}
remove_name = st.radio("卸甲服務", list(remove_options.keys()))
remove_price = remove_options[remove_name]

# --- 加購項目 ---
col1, col2 = st.columns(2)
with col1:
    st.write("")
    art_count = st.number_input("跳色數量 (指)", min_value=0, step=1)
    art_price = art_count * 100
with col2:
    addon_price = st.number_input("延甲/飾品金額 ($)", min_value=0, step=50)

st.write("") 

# --- 優惠 ---
with st.container(border=True):
    st.markdown("#### 🎉 優惠活動")
    is_birthday = st.toggle("🎂 壽星優惠 (9折)", value=False)


# ==========================================
# 4. 金額計算
# ==========================================
base_service_total = service_unit_price * pos_count
subtotal = base_service_total + pos_surcharge + remove_price + art_price + addon_price
final_total = subtotal * 0.9 if is_birthday else subtotal

if pos_count == 0:
    final_total = 0


# ==========================================
# 5. 輸出報價單
# ==========================================
date_str = datetime.date.today().strftime("%Y/%m/%d")
discount_text = " (已折抵壽星優惠)" if is_birthday else ""
remove_text = "無" if remove_name == "無" else remove_name
pos_text = "+".join(selected_pos) if selected_pos else "未選擇"

quote_text = f"""【Fairy. L NAIL ART 報價明細】
📅 日期：{date_str}
---------------------------
■ 項目：{service_name} ({pos_text})
■ 卸甲：{remove_text}
■ 額外加購：${int(art_price + addon_price)}
---------------------------
💰 預估總額：${int(final_total)}{discount_text}
＊提醒：本店作品享有一週保固"""

st.write("---")
st.markdown(f"### 💰 總金額：`${int(final_total)}`")

st.caption("👇 可在此直接編輯報價單內容")
edited_quote = st.text_area("報價單預覽", value=quote_text, height=200, label_visibility="collapsed")

st.code(edited_quote, language="text")
st.caption("👆 點擊右上角的複製圖示即可複製")
