import streamlit as st
import requests
from datetime import datetime

# 1. 網頁配置
st.set_page_config(page_title="AI 實時生活管家", page_icon="🤖")

# 自定義 CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI + IoT 實時生活管家")
st.caption("專為高三學生設計：把生活調成「懶人友好」模式")

# 2. 地區選擇（支援澳門與內地城市）
region = st.sidebar.selectbox("🌍 選擇區域", ["澳門", "廣東地區", "其他城市"])

if region == "澳門":
    city_map = {"澳門": "Macau"}
elif region == "廣東地區":
    city_map = {
        "珠海": "Zhuhai", 
        "廣州": "Guangzhou", 
        "深圳": "Shenzhen", 
        "中山": "Zhongshan", 
        "東莞": "Dongguan",
        "江門": "Jiangmen"
    }
else:
    city_map = {
        "北京": "Beijing", 
        "上海": "Shanghai", 
        "成都": "Chengdu", 
        "杭州": "Hangzhou",
        "武漢": "Wuhan"
    }

selected_city_name = st.sidebar.selectbox("📍 選擇城市", list(city_map.keys()))
english_city = city_map[selected_city_name]

# 3. 獲取實時數據
@st.cache_data(ttl=300)
def get_weather(city):
    try:
        # 使用 wttr.in 獲取數據
        resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        return None
    return None

data = get_weather(english_city)

if data:
    current = data['current_condition'][0]
    temp = current['temp_C']
    feels_like = current['FeelsLikeC']
    humidity = current['humidity']
    uv = current['uvIndex']
    desc = current['weatherDesc'][0]['value']

    # 4. 數據儀表板
    st.subheader(f"📊 {selected_city_name} 實時環境監測")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("氣溫", f"{temp}°C")
    col2.metric("體感", f"{feels_like}°C")
    col3.metric("濕度", f"{humidity}%")
    col4.metric("紫外線", uv)

    st.markdown("---")

    # 5. AI 懶人決策
    st.subheader("💡 AI 懶人指令")
    
    advice_list = []
    t = int(temp)
    h = int(humidity)
    u = int(uv)

    # 穿衣邏輯
    if t < 15: 
        advice_list.append("🧥 **穿衣建議**：冷空氣發威，羽絨或厚大衣準備好，別凍著了影響複習。")
    elif t < 23: 
        advice_list.append("🧥 **穿衣建議**：氣溫適中但微涼，建議穿衛衣或薄外套，方便穿脫。")
    else: 
        advice_list.append("👕 **穿衣建議**：外面挺熱的，短袖上陣，但進空調房記得披件校服。")

    # 濕度邏輯（針對澳門/南方）
    if h > 80: 
        advice_list.append("💧 **環境警報**：濕度太高了！家裡記得開除濕，不然人會昏昏欲睡，效率極低。")
    
    # 紫外線與降雨
    if u > 6: 
        advice_list.append("☀️ **紫外線強**：出門補習記得走騎樓，防曬做得好，心情不會燥。")
    
    if "rain" in desc.lower() or "shower" in desc.lower():
        advice_list.append("☔ **裝備提醒**：雲端偵測到降雨可能，出門一定要帶傘！")
    else:
        advice_list.append("✅ **裝備提醒**：目前天氣穩定，可以輕鬆出門。")

    for advice in advice_list:
        st.info(advice)

else:
    st.error("⚠️ 無法連線到氣象數據伺服器，請稍後刷新重試。")

if st.button("🔄 刷新數據"):
    st.rerun()

st.markdown("---")
st.caption(f"數據更新時間：{datetime.now().strftime('%H:%M:%S')} | 基於 IoT 雲端數據採集")
