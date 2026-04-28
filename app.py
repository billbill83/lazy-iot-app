import streamlit as st
import requests
from datetime import datetime
from duckduckgo_search import DDGS  # 這是目前 Python 中最穩定的免 Key AI 接口

# 1. 網頁基礎配置 (保持原本的高級感)
st.set_page_config(page_title="Puter AI 智慧管家", page_icon="🌤️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .ai-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border-top: 5px solid #00d2ff; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Puter 邏輯：免 Key AI 生活管家")
st.markdown("#### 「基於雲端原生技術，實現零配置智慧決策」")
st.divider()

# 2. 地區選擇 (保持你原本的邏輯)
st.sidebar.header("📍 定位與設置")
city_map = {"澳門": "Macau", "珠海": "Zhuhai", "香港": "Hong Kong"}
selected_city = st.sidebar.selectbox("選擇城市", list(city_map.keys()))

# 3. 免 Key 數據獲取 (Open-Meteo)
@st.cache_data(ttl=300)
def get_weather(city):
    # 這也是一個無需 Key 的專業氣象 API
    coords = {"Macau": (22.19, 113.54), "Zhuhai": (22.27, 113.57), "Hong Kong": (22.31, 114.17)}
    lat, lon = coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m"
    res = requests.get(url).json()
    return res['current_weather'], res['hourly']['relative_humidity_2m'][0]

# 4. 無需 Key 的 AI 決策引擎
def get_puter_style_advice(temp, hum, desc_code):
    # 將氣象代碼轉為文字
    weather_desc = "晴朗" if desc_code == 0 else "多雲或有雨"
    
    prompt = f"現在溫度{temp}度，濕度{hum}%，天氣{weather_desc}。請給澳門學生一個簡短的穿衣、帶傘和生活建議，字數在80字以內，口吻要像好朋友。"
    
    try:
        with DDGS() as ddgs:
            # 這是核心：直接調用，無需任何 API Key
            results = ddgs.chat(prompt, model='gpt-4o-mini')
            return results
    except:
        return "⚠️ AI 暫時斷開連接，請檢查網路。"

# 5. UI 展示
weather, humidity = get_weather(selected_city)
temp = weather['temperature']

st.subheader(f"📊 {selected_city} 當前數據")
c1, c2, c3 = st.columns(3)
c1.metric("即時氣溫", f"{temp}°C")
c2.metric("環境濕度", f"{humidity}%")
c3.metric("氣候代碼", weather['weathercode'])

st.divider()

# AI 建議區塊
st.subheader("💡 Puter AI 指令")
if st.button("生成懶人決策"):
    with st.spinner("正在呼叫雲端 AI 引擎..."):
        advice = get_puter_style_advice(temp, humidity, weather['weathercode'])
        st.markdown(f"""
        <div class="ai-card">
            <p style="color: #555; line-height: 1.6; font-size: 1.1rem;">{advice}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.caption(f"系統運行中 | 技術支持：Puter-Style API | 更新時間：{datetime.now().strftime('%H:%M:%S')}")
