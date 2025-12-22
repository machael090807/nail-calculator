import streamlit as st
import datetime

# --- 設定網頁標題與介面 ---
st.set_page_config(page_title="Fairy.L 報價", page_icon="💅")

st.title("💅 Fairy.L 報價計算機")
st.write("---")

# --- 輸入區塊 ---
# 1. 基礎服務
service_options = {
    "單色": 1333,
    "貓眼": 1100,
    "鏡面": 1300,
    "法式": 1500,
    "漸層": 1300
}
service_name = st.selectbox("基礎服務", list(service_options.keys()))
service_price = service_options[service_name]

# 2. 位置 (使用 Radio 按鈕比較好點)
position = st.radio("位置", ["手部", "足部"], horizontal=True)
pos_price = 200 if position == "足部" else 0

# 3. 卸甲服務
remove_options = {
    "無": 0,
    "本店卸甲": 200,
    "他店卸甲": 300,
    "純卸甲": 500
}
remove_name = st.selectbox("卸甲服務", list(remove_options.keys()))
remove_price = remove_options[remove_name]

# 4. 加購項目
col1, col2 = st.columns(2)
with col1:
    art_count = st.number_input("跳色數量 (指)", min_value=0, step=1)
    art_price = art_count * 100
with col2:
    addon_price = st.number_input("延甲/飾品金額 ($)", min_value=0, step=50)

# 5. 優惠
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
st.subheader(f"💰 總金額：${int(final_total)}")

# 顯示文字框讓使用者檢查
st.text_area("報價單預覽", value=quote_text, height=200)

# 這是 Streamlit 的複製按鈕 (手機上點一下會複製到剪貼簿)
st.code(quote_text, language="text")
st.caption("👆 點擊右上角的複製圖示即可複製")
