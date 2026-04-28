import streamlit as st
import requests
import random
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁基礎配置 (恢復原始 UI 風格) ---
st.set_page_config(page_title="AI 智慧生活管家", page_icon="🤖", layout="centered")

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
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 智慧生活決策助手 (精確增強版)")
st.divider()

# --- 2. 擴充地區庫 (澳門精細點 + 中國主要城市) ---
city_coords = {
    # 澳門精細區域
    "澳門 - 青洲": {"lat": 22.21, "lon": 113.53},
    "澳門 - 黑沙環": {"lat": 22.20, "lon": 113.55},
    "澳門 - 氹仔島": {"lat": 22.15, "lon": 113.56},
    "澳門 - 黑沙海灘": {"lat": 22.12, "lon": 113.56},
    "澳門 - 中區": {"lat": 22.19, "lon": 113.54},
    # 中國主要省份/城市
    "北京": {"lat": 39.90, "lon": 116.40},
    "上海": {"lat": 31.23, "lon": 121.47},
    "廣州": {"lat": 23.13, "lon": 113.26},
    "深圳": {"lat": 22.54, "lon": 114.05},
    "珠海 - 拱北": {"lat": 22.27, "lon": 113.57},
    "成都": {"lat": 30.65, "lon": 104.06},
    "杭州": {"lat": 30.27, "lon": 120.15},
    "西安": {"lat": 34.34, "lon": 108.93},
    "武漢": {"lat": 30.59, "lon": 114.30},
    "南京": {"lat": 32.06, "lon": 118.79},
    "台北": {"lat": 25.03, "lon": 121.56},
    "香港": {"lat": 22.31, "lon": 114.17}
}
selected_city = st.sidebar.selectbox("📍 選擇詳細位置", list(city_coords.keys()))

# --- 3. 強化版數據獲取 ---
@st.cache_data(ttl=600)
def fetch_weather_full(city_name):
    c = city_coords[city_name]
    # 請求更多實用數據：體感溫度, 濕度, 降雨機率, UV指數, 風速
    url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability,apparent_temperature,uv_index,windspeed_10m&timezone=auto"
    try:
        res = requests.get(url).json()
        now_hour = datetime.now().hour
        current = res['current_weather']
        return {
            "temp": current['temperature'],
            "app_temp": res['hourly']['apparent_temperature'][now_hour],
            "hum": res['hourly']['relative_humidity_2m'][now_hour],
            "rain": res['hourly']['precipitation_probability'][now_hour],
            "uv": res['hourly']['uv_index'][now_hour],
            "wind": res['hourly']['windspeed_10m'][now_hour]
        }
    except:
        return None

# --- 4. 決策引擎 ---
def get_ai_advice(data, city):
    styles = ["幽默搞怪", "專業嚴謹", "溫柔貼心", "極簡冷酷", "像個老派紳士"]
    perspectives = [
        "穿搭與層次建議 (是否帶外套)",
        "皮膚保養與防曬建議",
        "雨具準備與出門安全性",
        "運動與戶外活動可行性",
        "體感溫度應對策略"
    ]
    
    selected_style = random.choice(styles)
    selected_perspective = random.choice(perspectives)

    try:
        with DDGS() as ddgs:
            prompt = (f"你是住在{city}的生活管家。目前數據：溫度{data['temp']}°C(體感{data['app_temp']}°C)，"
                      f"濕度{data['hum']}%，降雨率{data['rain']}%，UV指數{data['uv']}，風速{data['wind']}km/h。 "
                      f"請以「{selected_style}」語氣給出具體建議。 "
                      f"必須涵蓋：穿幾層衣物、是否帶外套、是否塗防曬、是否帶雨具。 "
                      f"重點關注：{selected_perspective}")
            
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response if response else "AI 暫時休息，請參考：建議穿輕便服飾。"
    except:
        return f"🧥 建議：體感{data['app_temp']}度。建議穿層次性衣物。☔ 降雨{data['rain']}%，視情況帶傘。☀️ UV為{data['uv']}，注意防曬。"

# --- 5. 介面呈現 ---
data = fetch_weather_full(selected_city)

if data:
    st.subheader(f"📊 {selected_city} 實時環境參數")
    
    # 第一排數據：溫度與體感
    c1, c2, c3 = st.columns(3)
    c1.metric("實際氣溫", f"{data['temp']}°C")
    c2.metric("體感溫度", f"{data['app_temp']}°C")
    c3.metric("空氣濕度", f"{data['hum']}%")
    
    # 第二排數據：防護相關
    c4, c5, c6 = st.columns(3)
    c4.metric("降雨機率", f"{data['rain']}%")
    c5.metric("UV 指數", f"{data['uv']}")
    c6.metric("當前風速", f"{data['wind']} km/h")
    
    st.divider()
    
    st.subheader("💡 AI 動態決策建議")
    if st.button("獲取今日出門提案"):
        with st.spinner("AI 正在分析大氣數據..."):
            advice = get_ai_advice(data, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
            # 移除了 balloons，改用 toast 提示
            st.toast("建議已生成！", icon="✅")
else:
    st.error("無法獲取氣象數據，請檢查網路連結。")

st.caption(f"最後更新：{datetime.now().strftime('%H:%M:%S')} | 數據來源：Open-Meteo")
