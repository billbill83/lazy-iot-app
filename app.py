import streamlit as st
import requests
import random
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁配置 ---
st.set_page_config(page_title="AI 智慧生活管家", page_icon="🤖", layout="centered")

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
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 智慧生活決策助手 (大灣區版)")
st.markdown("#### 「AI 驅動：精準到區域的穿衣與出門建議」")
st.divider()

# --- 2. 擴充地區座標庫 ---
# 這裡增加了澳門細分區域及大灣區城市，徹底解決「地區太少」的問題
city_coords = {
    "澳門 - 北區 (花地瑪)": {"lat": 22.21, "lon": 113.55},
    "澳門 - 中區 (大堂/風順堂)": {"lat": 22.19, "lon": 113.54},
    "澳門 - 氹仔島": {"lat": 22.15, "lon": 113.56},
    "澳門 - 路環島": {"lat": 22.12, "lon": 113.56},
    "珠海 - 拱北/香洲": {"lat": 22.27, "lon": 113.57},
    "珠海 - 橫琴": {"lat": 22.14, "lon": 113.54},
    "香港 - 中環": {"lat": 22.28, "lon": 114.15},
    "香港 - 九龍": {"lat": 22.31, "lon": 114.17},
    "廣州": {"lat": 23.13, "lon": 113.26},
    "深圳": {"lat": 22.54, "lon": 114.05},
    "中山": {"lat": 22.52, "lon": 113.39},
    "東莞": {"lat": 23.02, "lon": 113.75},
    "佛山": {"lat": 23.02, "lon": 113.12}
}

selected_city = st.sidebar.selectbox("📍 選擇詳細位置", list(city_coords.keys()))

# --- 3. 數據獲取引擎 ---
@st.cache_data(ttl=600)
def fetch_weather(city_name):
    c = city_coords[city_name]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability"
    try:
        res = requests.get(url, timeout=10).json()
        current = res['current_weather']
        humidity = res['hourly']['relative_humidity_2m'][0]
        rain_chance = res['hourly']['precipitation_probability'][0]
        return current, humidity, rain_chance
    except:
        return None, None, None

# --- 4. 隨機風格 AI 決策引擎 ---
def get_ai_advice(temp, hum, rain, city):
    # 說話風格清單，確保每次生成都不一樣
    styles = ["幽默搞怪", "專業嚴謹", "像溫柔的家長", "極簡主義", "充滿活力的導遊", "大哥哥/大姊姊"]
    selected_style = random.choice(styles)
    
    # 保底建議邏輯 (當 AI 繁忙時使用)
    wear_logic = "短袖加薄外套" if 15 <= temp <= 25 else ("短袖" if temp > 25 else "厚外套")
    rain_logic = "一定要帶傘" if rain > 30 else "不用帶傘"
    backup = f"🧥 建議：{wear_logic}。☔ 雨具：{rain_logic}。✨ 提示：{city}目前體感舒適。"

    try:
        with DDGS() as ddgs:
            # 透過 Prompt 加入風格和隨機要求
            prompt = (f"你是住在{city}的生活管家，現在氣溫{temp}度，濕度{hum}%，降雨率{rain}%。 "
                      f"請用「{selected_style}」的語氣給出50字以內的穿衣與帶傘建議。 "
                      f"注意：每次的回覆內容、用詞和句式必須獨特且有變化。")
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response if response else backup
    except:
        return backup

# --- 5. 介面呈現 ---
weather, hum, rain = fetch_weather(selected_city)

if weather:
    st.subheader(f"📊 {selected_city} 實時環境數據")
    col1, col2, col3 = st.columns(3)
    col1.metric("氣溫", f"{weather['temperature']}°C")
    col2.metric("濕度", f"{hum}%")
    col3.metric("降雨機率", f"{rain}%")
    
    st.divider()
    
    st.subheader("💡 AI 懶人智慧決策")
    if st.button("獲取今日專屬指令"):
        with st.spinner("AI 正在為您構思建議..."):
            advice = get_ai_advice(weather['temperature'], hum, rain, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
            st.toast("建議已更新！") # 小提醒：告訴用戶內容已變化

st.divider()
st.caption(f"系統運行中 | 更新時間：{datetime.now().strftime('%H:%M:%S')} | Data: Open-Meteo & AI")
