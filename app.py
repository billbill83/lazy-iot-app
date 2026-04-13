import streamlit as st
import requests
from datetime import datetime

# 1. 網頁配置
st.set_page_config(page_title="AI 實時生活管家", page_icon="🤖")

# 自定義 CSS 讓介面更美觀（懶人也要看漂亮的介面）
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_ Harris=True)

st.title("🤖 AI + IoT 實時生活管家")
st.caption("專為高三學生設計：把生活調成「懶人友好」模式")

# 2. 地區選擇（加入澳門與內地熱門城市）
# 左側選單分類
region = st.sidebar.selectbox("🌍 選擇區域", ["澳門", "大灣區/廣東", "主要城市"])

if region == "澳門":
    city_map = {"澳門": "Macau"}
elif region == "大灣區/廣東":
    city_map = {"珠海": "Zhuhai", "廣州": "Guangzhou", "深圳": "Shenzhen", "中山": "Zhongshan", "東莞": "Dongguan"}
else:
    city_map = {"北京": "Beijing", "上海": "Shanghai", "成都": "Chengdu", "杭州": "Hangzhou"}

selected_city_name = st.sidebar.selectbox("📍 選擇城市", list(city_map.keys()))
english_city = city_map[selected_city_name]

# 3. 獲取實時 IoT 數據 (帶有防錯機制)
@st.cache_data(ttl=300) # 每 5 分鐘快取一次
def get_weather(city):
    try:
        # 使用 wttr.in 的 JSON 介面
        resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        if resp.status_code == 200:
            return resp.json()
    except:
        return None
    return None

data = get_weather(english_city)

if data:
    # 提取數據
    current = data['current_condition'][0]
    temp = current['temp_C']
    feels_like = current['FeelsLikeC']
    humidity = current['humidity']
    uv = current['uvIndex']
    # 隨機處理天氣描述（如果是英文就顯示英文，有中文顯示中文）
    desc = current.get('lang_zh', [{}])[0].get('value', current['weatherDesc'][0]['value'])

    # 4. 數據儀表板
    st.subheader(f"📊 {selected_city_name} 實時環境監測")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("氣溫", f"{temp}°C")
    col2.metric("體感", f"{feels_like}°C")
    col3.metric("濕度", f"{humidity}%")
    col4.metric("紫外線", uv)

    st.markdown("---")

    # 5. AI 懶人決策邏輯
    st.subheader("💡 AI 懶人指令")
    
    # 這裡就是 AI 的「大腦」：根據 IoT 數據給出生活建議
    advice_list = []
    
    # 穿衣邏輯
    t = int(temp)
    if t < 15: advice_list.append("🧥 **穿衣重點**：冷空氣來襲！穿上羽絨服或厚大衣，別讓感冒斷了你的複習節奏。")
    elif t < 22: advice_list.append("🧥 **穿衣重點**：氣溫偏涼，建議「洋蔥式穿法」（內搭短袖+外加衛衣/外套）。")
    else: advice_list.append("👕 **穿衣重點**：天氣炎熱，短袖即可，但記得帶件薄外套進空調房。")

    # 針對澳門/南方濕度的邏輯
    h = int(humidity)
    if h > 80: advice_list.append("💧 **環境警告**：濕度爆表！室內記得開除濕，否則書本會發霉，人也容易昏沉。")

    # 紫外線邏輯
    u = int(uv)
    if u > 5: advice_list.append("☀️ **戶外警告**：紫外線強烈，如果要出門買宵夜/補習，記得走有遮陽的地方。")

    # 下雨邏輯
    if "rain" in desc.lower() or "雨" in desc:
        advice_list.append("☔ **裝備提醒**：偵測到降雨機率，**懶人必備**：直接放把傘在書包，省得跑回家拿。")
    else:
        advice_list.append("✅ **裝備提醒**：目前無雨，可以空手出門，身心輕鬆。")

    # 顯示建議
    for advice in advice_list:
        st.info(advice)

else:
    st.error("⚠️ 數據抓取失敗。可能是網路問題，或者 API 暫時繁忙。請點擊下方的刷新按鈕。")

if st.button("🔄 刷新實時數據"):
    st.rerun()

# 頁尾
st.markdown("---")
st.caption(f"最後更新：{datetime.now().strftime('%H:%M:%S')} | 本系統自動整合 IoT 氣候數據與 AI 決策模型")
