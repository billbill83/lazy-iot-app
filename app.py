import streamlit as st
import requests
import random
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁基礎配置 ---
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
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 智慧生活決策助手 (動態增強版)")
st.divider()

# --- 2. 擴充地區座標庫 ---
city_coords = {
    "澳門 - 北區": {"lat": 22.21, "lon": 113.55},
    "澳門 - 中區": {"lat": 22.19, "lon": 113.54},
    "澳門 - 氹仔島": {"lat": 22.15, "lon": 113.56},
    "澳門 - 路環島": {"lat": 22.12, "lon": 113.56},
    "珠海 - 拱北/香洲": {"lat": 22.27, "lon": 113.57},
    "珠海 - 橫琴": {"lat": 22.14, "lon": 113.54},
    "香港 - 中環": {"lat": 22.28, "lon": 114.15},
    "香港 - 九龍": {"lat": 22.31, "lon": 114.17},
    "廣州": {"lat": 23.13, "lon": 113.26},
    "深圳": {"lat": 22.54, "lon": 114.05}
}
selected_city = st.sidebar.selectbox("📍 選擇詳細位置", list(city_coords.keys()))

# --- 3. 數據獲取 ---
@st.cache_data(ttl=600)
def fetch_weather(city_name):
    c = city_coords[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability"
    res = requests.get(url).json()
    return res['current_weather'], res['hourly']['relative_humidity_2m'][0], res['hourly']['precipitation_probability'][0]

# --- 4. 隨機問題與隨機風格引擎 ---
def get_dynamic_ai_advice(temp, hum, rain, city):
    # 每次點擊隨機選一個「說話語氣」
    styles = ["幽默搞怪", "專業嚴謹", "溫柔貼心", "極簡冷酷", "像個老派紳士"]
    
    # 每次點擊隨機選一個「關注重點」讓問題本身發生變化
    perspectives = [
        "請特別從『戶外穿搭美學』的角度給建議。",
        "請特別從『皮膚保養與防潮』的角度給建議。",
        "請從『今天適不適合戶外運動』的角度出發。",
        "請用『趕時間上學的學生』視角給出最直接的指令。",
        "請加入一個關於今天天氣的『冷知識』並給出建議。"
    ]
    
    selected_style = random.choice(styles)
    selected_perspective = random.choice(perspectives)

    try:
        with DDGS() as ddgs:
            # 這裡的問題（Prompt）每次點擊都會因為上面的隨機選擇而完全不同
            prompt = (f"你是住在{city}的生活管家。氣溫{temp}度，濕度{hum}%，降雨率{rain}%。 "
                      f"請用「{selected_style}」的語氣給出50字以內建議。 "
                      f"重點：{selected_perspective}")
            
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response if response else "AI 暫時休息，請參考：建議穿輕便服飾。"
    except:
        return f"🧥 建議：溫度{temp}度，穿輕便外衣。☔ 降雨{rain}%，視情況帶傘。"

# --- 5. 介面呈現 ---
weather, hum, rain = fetch_weather(selected_city)
if weather:
    st.subheader(f"📊 {selected_city} 實時環境")
    c1, c2, c3 = st.columns(3)
    c1.metric("氣溫", f"{weather['temperature']}°C")
    c2.metric("濕度", f"{hum}%")
    c3.metric("降雨", f"{rain}%")
    
    st.divider()
    
    st.subheader("💡 每按一次都有新驚喜")
    if st.button("獲取動態決策"):
        with st.spinner("AI 正在切換思維模式..."):
            advice = get_dynamic_ai_advice(weather['temperature'], hum, rain, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
            st.toast("AI 已切換視角！")

st.caption(f"最後更新：{datetime.now().strftime('%H:%M:%S')}")
