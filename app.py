import streamlit as st
import requests
from datetime import datetime
from duckduckgo_search import DDGS

# 網頁基礎配置
st.set_page_config(page_title="AI 懶人生活管家", page_icon="🤖", layout="centered")

# CSS 樣式優化
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .ai-card { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 10px solid #00d2ff; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 智慧生活決策助手")
st.divider()

# 地區座標
city_coords = {
    "澳門": {"lat": 22.19, "lon": 113.54},
    "珠海": {"lat": 22.27, "lon": 113.57},
    "香港": {"lat": 22.31, "lon": 114.17}
}
selected_city = st.sidebar.selectbox("📍 選擇城市", list(city_coords.keys()))

# 獲取天氣
@st.cache_data(ttl=600)
def fetch_weather(city_name):
    c = city_coords[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability"
    res = requests.get(url).json()
    return res['current_weather'], res['hourly']['relative_humidity_2m'][0], res['hourly']['precipitation_probability'][0]

# --- 核心改動：雙保險 AI 引擎 ---
def get_smart_advice(temp, hum, rain, city):
    # 先準備一個「保底建議」（邏輯引擎）
    if temp > 28: wear = "穿短袖，注意防曬"
    elif 18 <= temp <= 28: wear = "短袖加件薄外套"
    else: wear = "穿厚外套，注意保暖"
    
    umbrella = "記得帶傘！" if rain > 30 else "無需帶傘。"
    
    backup_advice = f"🧥 建議：{wear}。 \n☔ 雨具：{umbrella} \n✨ 提醒：{city}當前濕度為{hum}%，體感舒適。"

    # 嘗試調用 AI
    try:
        with DDGS() as ddgs:
            prompt = f"你是澳門管家。氣溫{temp}度,濕度{hum}%,雨率{rain}%。給出50字穿衣帶傘建議。"
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            if response: return response
    except:
        return backup_advice  # 如果 AI 繁忙，直接回傳保底建議，用戶感覺不到出錯
    return backup_advice

# 介面渲染
weather, hum, rain = fetch_weather(selected_city)
if weather:
    st.subheader(f"📊 {selected_city} 實時環境")
    c1, c2, c3 = st.columns(3)
    c1.metric("氣溫", f"{weather['temperature']}°C")
    c2.metric("濕度", f"{hum}%")
    c3.metric("降雨", f"{rain}%")
    
    st.divider()
    
    st.subheader("💡 AI 懶人決策指令")
    if st.button("獲取今日決策"):
        with st.spinner("AI 正在思考中..."):
            advice = get_smart_advice(weather['temperature'], hum, rain, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)

st.caption(f"數據更新時間：{datetime.now().strftime('%H:%M:%S')}")
