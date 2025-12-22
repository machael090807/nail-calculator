import streamlit as st
import datetime

# ==========================================
# 1. 設定 App 圖示與 iOS 強制參數
# ==========================================
icon_url = "https://raw.githubusercontent.com/machael090807/nail-calculator/07e29efbbce9832dec754699d7a2afdc9660c024/2025-12-22%2019.08.45.jpg"

st.set_page_config(page_title="Fairy.L 報價系統", page_icon=icon_url)

# 嘗試強制注入 iOS icon (注意：iOS Safari 對動態網頁的支援度有限，若仍失敗是正常的)
st.markdown(
    f"""
    <head>
        <link rel="apple-touch-icon" sizes="180x180" href="{icon_url}">
        <link rel="icon" type="image/png" href="{icon_url}">
    </head>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 2. CSS 美化 + 核彈級隱藏 (Nuclear Option)
# ==========================================
custom_css = """
<style>
/* 奶茶色背景 */
.stApp {
    background-color: #F3E5D8;
}

/* 深咖啡色文字 */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stRadio label, .stCheckbox label, .stToggle label {
    color: #4E342E !important;
}

/* 標題設定 */
h1 {
    text-align: center !important;
    font-size: clamp(1.5rem, 6vw, 2.5rem) !important; 
    padding-bottom: 10px;
    white-space: nowrap;
}

/* 👇👇👇【核彈級隱藏區 - 針對所有已知物件】👇👇👇 */

/* 1. 隱藏上方 Header 與 工具列 */
header, .stApp > header {
    display: none !important;
    visibility: hidden !important;
    height: 0px !important;
}

/* 2. 隱藏右下角 Viewer Badge (Logo) */
/* Streamlit 常常改 class 名稱，我們用屬性選取器通殺 */
[data-testid="stStatusWidget"], 
[class*="viewerBadge"], 
[class*="stStatusWidget"],
.viewerBadge_container__1QSob {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* 3. 隱藏下方 Footer */
footer {
    display: none !important;
}

/* 4. 隱藏右上角選單 */
#MainMenu {
    display: none !important;
}

/* 5. 隱藏圖片放大按鈕 (讓介面更像 App) */
button[title="View fullscreen"] {
    display: none !important;
}

/* 👆👆👆 隱藏設定結束 👆👆👆 */


/* 輸入框美化 */
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    border-color: #DCC7A1 !important;
}
div[role="radiogroup"] > label, div[data-testid="stCheckbox"] label {
    padding-top: 5px;
    padding-bottom: 5px;
}
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
# 3. 內容區 (保持不變)
# ==========================================
st.title("💅 Fairy.L 報價計算機") 
st.write("---")

service_options = {
    "單色": 1000, "貓眼": 1100, "鏡面": 1300, "法式": 1500, "漸層": 1300
}
service_name = st.radio("基礎服務", list(service_options.keys())) 
service_unit_price = service_options[service_name]

st.write("") 

st.write("位置 (可複選)")
col_p1, col_p2 = st.columns(2)
with col_p1:
    pos_hand = st.checkbox("手部", value=True)
with col_p2:
    pos_foot = st.checkbox("足部 (+200)")

selected_pos = []
if pos_hand: selected_pos.append("手部")
if pos_foot: selected_pos.append("足部")
pos_count = len(selected_pos)
pos_surcharge = 200 if pos_foot else 0 

st.write("") 

remove_options = {
    "無": 0, "本店卸甲": 200, "他店卸甲": 300, "純卸甲": 500
}
remove_name = st.radio("卸甲服務", list(remove_options.keys()))
remove_price = remove_options[remove_name]

col1, col2 = st.columns(2)
with col1:
    st.write("")
    art_count = st.number_input("跳色數量 (指)", min_value=0, step=1)
    art_price = art_count * 100
with col2:
    addon_price = st.number_input("延甲/飾品金額 ($)", min_value=0, step=50)

st.write("") 

with st.container(border=True):
    st.markdown("#### 🎉 優惠活動")
    is_birthday = st.toggle("🎂 壽星優惠 (9折)", value=False)

base_service_total = service_unit_price * pos_count
subtotal = base_service_total + pos_surcharge + remove_price + art_price + addon_price
final_total = subtotal * 0.9 if is_birthday else subtotal
if pos_count == 0: final_total = 0

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
