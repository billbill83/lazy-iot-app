import streamlit as st
import requests
from datetime import datetime

# 1. 網頁基礎配置
st.set_page_config(page_title="AI 懶人生活管家", page_icon="🤖", layout="centered")

# 自定義 CSS (提升視覺高級感)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    div.stButton > button:first-child { background-color: #007bff; color: white; border-radius: 10px; width: 100%; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI + IoT 懶人生活管家")
st.markdown("#### 「讓技術處理繁瑣，讓你專注於高三衝刺」")
st.divider()

# 2. 地區選擇邏輯 (支持澳門、廣東及內地城市)
st.sidebar.header("📍 位置設置")
region = st.sidebar.selectbox("選擇區域", ["澳門", "廣東地區", "其他主要城市"])

if region == "澳門":
    city_map = {"澳門": "Macau"}
elif region == "廣東地區":
    city_map = {
        "珠海": "Zhuhai", "廣州": "Guangzhou", "深圳": "Shenzhen", 
        "中山": "Zhongshan", "東莞": "Dongguan", "佛山": "Foshan"
    }
else:
    city_map = {
        "北京": "Beijing", "上海": "Shanghai", "成都": "Chengdu", 
        "杭州": "Hangzhou", "南京": "Nanjing", "武漢": "Wuhan"
    }

selected_city_name = st.sidebar.selectbox("選擇城市", list(city_map.keys()))
english_city = city_map[selected_city_name]

# 3. 實時數據獲取 (模擬 IoT 雲端數據採集)
@st.cache_data(ttl=300)
def fetch_weather_data(city):
    try:
        # 使用 wttr.in JSON API
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None
    return None

data = fetch_weather_data(english_city)

if data:
    # 提取數據
    current = data['current_condition'][0]
    temp = int(current['temp_C'])
    feels_like = int(current['FeelsLikeC'])
    humidity = int(current['humidity'])
    uv = int(current['uvIndex'])
    desc = current['weatherDesc'][0]['value'].lower()

    # 4. 數據儀表板呈現
    st.subheader(f"📊 {selected_city_name} 實時環境參數")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("氣溫", f"{temp}°C")
    c2.metric("體感", f"{feels_like}°C")
    c3.metric("濕度", f"{humidity}%")
    c4.metric("紫外線", uv)

    st.divider()

    # 5. 核心 AI 決策引擎 (廣泛且多樣的穿衣與生活建議)
    st.subheader("💡 AI 懶人決策指令")
    
    advices = []

    # A. 基礎穿衣架構
    if feels_like >= 32:
        wear = "🔥 **極熱提醒**：穿著最輕便的背心或吸濕排汗短袖，儘量減少皮膚覆蓋面積。"
    elif 26 <= feels_like < 32:
        wear = "👕 **夏季標準**：棉質短袖 T-Shirt 搭配短褲。建議選擇淺色系以減少熱吸收。"
    elif 20 <= feels_like < 26:
        wear = "👔 **舒適穿搭**：短袖外加一件薄款襯衫或抗 UV 防曬長袖，適應微涼。"
    elif 15 <= feels_like < 20:
        wear = "🧥 **春秋疊穿**：長袖衛衣 (Hoodie) 或薄針織衫，早晚建議加一件輕便夾克。"
    elif 10 <= feels_like < 15:
        wear = "🧣 **冬季防禦**：保暖內衣 (發熱衣) + 羊毛衫 + 防風外套。"
    else:
        wear = "❄️ **嚴寒警告**：羽絨服 + 圍巾 + 手套。多層保暖勝過一件厚衣。"

    advices.append(wear)

    # B. 針對特定場景的擴展建議
    # 溫差提醒
    if abs(temp - feels_like) > 5:
        advices.append("🌡️ **溫差注意**：氣溫與體感差異顯著，強烈建議採用『洋蔥式穿法』以便隨時增減。")
    
    # 補習班/室內空調提醒
    if temp > 25:
        advices.append("🏫 **空調房場景**：雖然室外熱，但室內冷氣可能較強。包裡請預備一件薄外套，避免溫差導致感冒影響學習。")

    # 南方濕冷/濕熱提醒
    if humidity > 80:
        if temp < 18:
            advices.append("💧 **濕冷預警**：當前濕度極高，寒氣具備『穿透屬性』，最外層必須防風。")
        elif temp > 28:
            advices.append("💦 **悶熱警告**：環境潮濕悶熱，建議穿著亞麻或速乾材質，防止出汗後衣服黏身影響專注力。")

    # 紫外線與雨水提醒
    if uv >= 6:
        advices.append("🕶️ **防曬建議**：紫外線偏強，如需長距離步行，請使用遮陽傘或穿著物理防曬服。")
    
    if "rain" in desc or "shower" in desc:
        advices.append("☔ **裝備指令**：監測到降雨可能，出門必須攜帶雨具，建議穿著防水性能較好的鞋子。")
    else:
        advices.append("✅ **裝備指令**：目前天氣穩定，可輕裝簡從，無需攜帶雨傘。")

    # 渲染建議
    for a in advices:
        st.info(a)

else:
    st.error("❌ 獲取實時數據失敗。請檢查網絡或更換城市重試。")

# 6. 底部刷新按鈕
if st.button("🔄 刷新實時環境數據"):
    st.rerun()

st.divider()
st.caption(f"系統運行中：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 數據源: Open IoT Weather Node")
