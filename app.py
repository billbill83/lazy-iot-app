import streamlit as st
import requests
from datetime import datetime

# 1. 網頁基礎設置
st.set_page_config(page_title="AI 實時生活管家", page_icon="🌤️")
st.title("🌤️ AI + IoT 實時生活管家")
st.markdown("---")

# 2. 地區選擇（實實在在的多地區支援）
city_map = {
    "台北": "Taipei",
    "台中": "Taichung",
    "高雄": "Kaohsiung",
    "新竹": "Hsinchu",
    "台南": "Tainan"
}
selected_city = st.sidebar.selectbox("📍 選擇您的所在地區", list(city_map.keys()))
english_city = city_map[selected_city]

# 3. 獲取實時 IoT 數據 (調用 Open Data API)
@st.cache_data(ttl=600)  # 每 10 分鐘更新一次數據，節省效能
def get_realtime_weather(city):
    try:
        # 使用 wttr.in 獲取 JSON 格式數據
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()
        
        current = data['current_condition'][0]
        return {
            "temp": current['temp_C'],
            "desc": current['lang_zh'] if 'lang_zh' in current else current['weatherDesc'][0]['value'],
            "humidity": current['humidity'],
            "uv": current['uvIndex'],
            "feels_like": current['FeelsLikeC']
        }
    except:
        return None

weather = get_realtime_weather(english_city)

if weather:
    # 4. 數據儀表板
    st.subheader(f"📊 {selected_city} 實時環境數據")
    c1, c2, c3 = st.columns(3)
    c1.metric("實時氣溫", f"{weather['temp']} °C")
    c2.metric("體感溫度", f"{weather['feels_like']} °C")
    c3.metric("紫外線指數", weather['uvIndex'])

    c4, c5, _ = st.columns(3)
    c4.metric("空氣濕度", f"{weather['humidity']}%")
    c5.metric("當前天氣", weather['desc'])

    st.divider()

    # 5. AI 懶人決策（針對高三生實用場景）
    st.subheader("🤖 AI 懶人決策建議")
    
    temp = int(weather['temp'])
    uv = int(weather['uv'])
    hum = int(weather['humidity'])

    # 模擬 AI 邏輯分析
    tips = []
    
    # 穿衣建議
    if temp < 18:
        tips.append("🧥 **穿衣**：今天有點冷，穿件厚外套吧，感冒了會影響複習進度。")
    elif temp > 28:
        tips.append("👕 **穿衣**：外面很熱，穿排汗短袖，免得進補習班冷氣房前先滿身大汗。")
    else:
        tips.append("👔 **穿衣**：氣溫舒適，薄長袖或短袖加薄外套是最佳選擇。")

    # 讀書環境建議 (IoT 應用場景)
    if hum > 75:
        tips.append("💧 **環境**：濕度太高容易昏昏欲睡，建議開啟除濕機，讀書效率會更高。")
    
    # 戶外活動建議
    if uv > 6:
        tips.append("☀️ **防護**：紫外線爆表！如果要出門買飯，記得撐傘或走騎樓，別被曬暈了。")
    
    # 實用總結
    if "雨" in weather['desc']:
        tips.append("☔ **裝備**：偵測到降雨，出門務必帶傘，鞋子建議穿防水的。")
    else:
        tips.append("👟 **裝備**：天氣適合運動，讀書讀累了可以去操場跑兩圈。")

    for tip in tips:
        st.write(tip)

else:
    st.error("暫時無法獲取實時數據，請檢查網路連接或稍後再試。")

# 6. 腳註
st.caption(f"數據更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("這是一個結合物聯網數據與 AI 決策的懶人友善助手原型。")
