import streamlit as st
import requests
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="AI 懶人生活管家", page_icon="🤖", layout="centered")

# 自定義 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .ai-card { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 10px solid #00d2ff; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        color: #333;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 免 Key 智慧生活助手")
st.markdown("#### 「無需驗證，讓 AI 決定你的出門穿搭」")
st.divider()

# --- 2. 地區選擇與座標綁定 ---
# 這裡解決了你圖片中的 KeyError 問題，確保選單和座標完全一致
city_coords = {
    "澳門": {"lat": 22.19, "lon": 113.54},
    "珠海": {"lat": 22.27, "lon": 113.57},
    "香港": {"lat": 22.31, "lon": 114.17},
    "廣州": {"lat": 23.13, "lon": 113.26},
    "深圳": {"lat": 22.54, "lon": 114.05}
}

selected_city = st.sidebar.selectbox("📍 選擇你的城市", list(city_coords.keys()))

# --- 3. 數據獲取 (使用免 Key 的 Open-Meteo) ---
@st.cache_data(ttl=600)
def fetch_weather(city_name):
    coords = city_coords[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability"
    try:
        res = requests.get(url, timeout=10).json()
        current = res['current_weather']
        # 取得當前小時的濕度與降雨機率
        humidity = res['hourly']['relative_humidity_2m'][0]
        rain_chance = res['hourly']['precipitation_probability'][0]
        return current, humidity, rain_chance
    except Exception as e:
        st.error(f"數據獲取失敗: {e}")
        return None, None, None

# --- 4. 免 Key AI 建議邏輯 ---
def get_ai_advice(temp, hum, rain, city):
    # 建立一個清晰的指令給 AI
    prompt = f"""
    你是一個貼心的生活管家。現在{city}的環境數據如下：
    氣溫：{temp}度，濕度：{hum}%，降雨機率：{rain}%。
    請給出 100 字以內的建議，包含：
    1. 穿衣建議（考慮體感）。
    2. 要不要帶傘（根據降雨率）。
    3. 溫馨提醒。
    請用溫暖有禮貌的中文回覆。
    """
    try:
        with DDGS() as ddgs:
            # 調用免 Key 的 AI 接口
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response
    except Exception:
        return "⚠️ AI 目前繁忙，請稍後再試。建議參考數值：體感略涼，建議帶備薄外套。"

# --- 5. 畫面呈現 ---
weather_data, hum_data, rain_data = fetch_weather(selected_city)

if weather_data:
    temp = weather_data['temperature']
    
    # 儀表板
    st.subheader(f"📊 {selected_city} 實時數據")
    col1, col2, col3 = st.columns(3)
    col1.metric("氣溫", f"{temp}°C")
    col2.metric("濕度", f"{hum_data}%")
    col3.metric("降雨機率", f"{rain_data}%")
    
    st.divider()
    
    # AI 建議按鈕
    st.subheader("💡 AI 懶人決策建議")
    if st.button("獲取 AI 出門指令"):
        with st.spinner("AI 正在分析雲端數據..."):
            advice = get_ai_advice(temp, hum_data, rain_data, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)

# 頁尾
st.divider()
st.caption(f"系統運行中 | 更新時間：{datetime.now().strftime('%H:%M:%S')} | Data by Open-Meteo")
