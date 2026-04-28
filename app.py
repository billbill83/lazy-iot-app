import streamlit as st
import requests
import random  # 導入隨機庫
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

# --- 核心改動：增加隨機風格的 AI 引擎 ---
def get_smart_advice(temp, hum, rain, city):
    # 1. 定義多樣化的說話風格
    styles = [
        "幽默風趣且愛開玩笑", 
        "像溫柔慈祥的長輩", 
        "像極簡主義的專業教練", 
        "像充滿活力的旅遊導遊", 
        "像愛碎碎唸但貼心的好朋友",
        "用充滿科技感和未來感的口吻"
    ]
    # 每次點擊按鈕時，隨機選一個風格
    current_style = random.choice(styles)

    # 2. 準備保底建議（當 AI 繁忙時）
    wear = "穿短袖" if temp > 28 else ("短袖加件薄外套" if temp >= 18 else "穿厚外套")
    umbrella = "記得帶傘！" if rain > 30 else "無需帶傘。"
    backup_advice = f"🧥 建議：{wear}。 \n☔ 雨具：{umbrella} \n✨ 提醒：{city}當前濕度為{hum}%，體感舒適。"

    # 3. 嘗試調用 AI，並在 Prompt 中要求多樣性
    try:
        with DDGS() as ddgs:
            # 加入隨機風格和「每次都要不同」的要求
            prompt = (f"你是住在{city}的生活管家。現在氣溫{temp}度，濕度{hum}%，降雨機率{rain}%。"
                      f"請以「{current_style}」的風格給出50字以內的建議。"
                      f"注意：請確保你的建議內容與遣詞用句具有新鮮感，不要與之前的回覆雷同。")
            
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            if response: return response
    except:
        return backup_advice
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
        with st.spinner("AI 正在為你構思新鮮建議..."):
            advice = get_smart_advice(weather['temperature'], hum, rain, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
            # 添加一個小的提示效果
            st.toast(f"切換至「{random.choice(['驚喜','獨特','全新'])}」視角生成建議")

st.caption(f"數據更新時間：{datetime.now().strftime('%H:%M:%S')}")
