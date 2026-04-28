import streamlit as st
import requests
import random
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁基礎配置 ---
st.set_page_config(page_title="AI 超能生活管家 Pro", page_icon="🌤️", layout="centered")

# 自定義 CSS 讓介面更有質感
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .ai-card { 
        background-color: #ffffff; 
        padding: 30px; 
        border-radius: 25px; 
        border-right: 8px solid #ff4b4b;
        border-left: 8px solid #1c83e1; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        font-size: 1.15rem;
        line-height: 1.6;
        color: #1f1f1f;
    }
    .metric-box {
        background: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌤️ AI 超能生活管家 Pro")
st.write("結合實時氣象與多樣化 AI 邏輯，為你的出門決策把關。")
st.divider()

# --- 2. 地區座標庫 ---
city_coords = {
    "澳門 - 北區": {"lat": 22.21, "lon": 113.55},
    "澳門 - 氹仔": {"lat": 22.15, "lon": 113.56},
    "香港 - 中環": {"lat": 22.28, "lon": 114.15},
    "珠海 - 橫琴": {"lat": 22.14, "lon": 113.54},
    "深圳 - 福田": {"lat": 22.54, "lon": 114.05},
    "廣州 - 天河": {"lat": 23.13, "lon": 113.26}
}
selected_city = st.sidebar.selectbox("📍 切換追蹤地點", list(city_coords.keys()))

# --- 3. 強化版數據獲取 ---
@st.cache_data(ttl=600)
def fetch_weather_pro(city_name):
    c = city_coords[city_name]
    # 增加 uv_index 與 windspeed 獲取
    url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability,uv_index,windspeed_10m"
    res = requests.get(url).json()
    
    current = res['current_weather']
    # 取得當前小時的索引
    now_hour = datetime.now().hour
    return {
        "temp": current['temperature'],
        "wind": current['windspeed'],
        "hum": res['hourly']['relative_humidity_2m'][now_hour],
        "rain": res['hourly']['precipitation_probability'][now_hour],
        "uv": res['hourly']['uv_index'][now_hour]
    }

# --- 4. 多樣化決策引擎 ---
def get_ai_decision(data, city):
    # 風格庫：增加衝突感與趣味性
    styles = [
        "毒舌健身教練", "溫柔的幼兒園老師", "冷酷的賽博龐克特工", 
        "過度擔心的老奶奶", "充滿活力的旅遊博主", "大數據分析機器人"
    ]
    
    # 任務重點：確保涵蓋所有用戶要求的維度
    tasks = [
        "請針對『洋蔥式穿法』給出具體層次建議。",
        "請根據 UV 指數給出『防曬霜 SPF/PA』與遮陽具建議。",
        "請針對『髮型與抗濕度』給出造型建議。",
        "請預測『體感溫度』並判斷是否需要厚外套或薄風衣。",
        "請評估『雨具等級』（折疊傘、長柄傘或乾脆待在室內）。"
    ]

    selected_style = random.choice(styles)
    selected_task = random.choice(tasks)

    try:
        with DDGS() as ddgs:
            # 構建結構化 Prompt
            prompt = (
                f"你是{city}的{selected_style}。現在氣溫{data['temp']}°C、"
                f"濕度{data['hum']}%、降雨機率{data['rain']}%、"
                f"UV指數{data['uv']}、風速{data['wind']}km/h。 "
                f"請在 80 字內給出穿衣（外套種類）、防曬、雨具的具體建議。 "
                f"特別重點：{selected_task}"
            )
            
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response if response else "AI 正在重新觀測雲象，請稍後再試。"
    except Exception as e:
        return f"🚧 AI 連結暫時中斷。建議：{data['temp']}°C 穿件薄外套，降雨率{data['rain']}% 記得帶把傘！"

# --- 5. 介面呈現 ---
data = fetch_weather_pro(selected_city)

# 頂部氣象卡片
st.subheader(f"📊 {selected_city} 當前狀況")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🌡️ 氣溫", f"{data['temp']}°")
col2.metric("💧 濕度", f"{data['hum']}%")
col3.metric("☔ 降雨", f"{data['rain']}%")
col4.metric("☀️ UV", f"{data['uv']}")
col5.metric("🌬️ 風速", f"{int(data['wind'])}k/h")

st.divider()

# 動態決策區
st.subheader("🤖 AI 智慧生活建議")
st.write("每次點擊都會更換 AI 風格與建議維度：")

if st.button("✨ 獲取個性化生活提案", use_container_width=True):
    with st.spinner("🚀 AI 正在分析大氣數據與穿搭趨勢..."):
        advice = get_ai_decision(data, selected_city)
        st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
        
        # 額外小提示
        if data['uv'] > 5:
            st.warning("提醒：紫外線較強，別忘了塗防曬！")
        if data['rain'] > 40:
            st.info("提醒：降雨機率較高，建議攜帶堅固的雨傘。")
        if data['temp'] < 20 or data['wind'] > 15:
            st.snow() # 稍微裝飾一下
            st.error("提醒：體感較涼或風大，請務必帶上外套。")

st.caption(f"數據來源：Open-Meteo & DuckDuckGo AI | 最後更新：{datetime.now().strftime('%H:%M:%S')}")
