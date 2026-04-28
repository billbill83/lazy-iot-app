import streamlit as st
import requests
import openai  # 記得在 requirements.txt 加入 openai

# --- 頁面配置 ---
st.set_page_config(page_title="AI 懶人生活管家", page_icon="🤖", layout="wide")

# --- 自定義樣式 (美化 UI) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .advice-box { background-color: #e1f5fe; padding: 20px; border-radius: 15px; border-left: 5px solid #0288d1; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據獲取模組 ---
def get_weather_data(city):
    try:
        # 使用 wttr.in 獲取數據
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data['current_condition'][0]
        temp = int(current['temp_C'])
        feels_like = int(current['FeelsLikeC'])
        humidity = int(current['humidity'])
        uv_index = int(current['uvIndex'])
        desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
        
        # 判斷是否會下雨 (取未來 3 小時的降雨機率)
        rain_chance = int(data['weather'][0]['hourly'][0]['chanceofrain'])
        
        return temp, feels_like, humidity, uv_index, desc, rain_chance
    except:
        return None

# --- 2. AI 決策引擎 (核心升級) ---
def get_ai_advice(temp, humidity, uv, rain, desc):
    """
    這裡模擬調用 AI。如果你有 OpenAI Key，可以解除註釋。
    如果沒有，我們用一個『模擬 AI 邏輯』來生成像 AI 一樣親切的建議。
    """
    # 這裡就是所謂的 Prompt Engineering (提示詞工程)
    prompt = f"天氣{desc}，氣溫{temp}度，濕度{humidity}%，降雨機率{rain}%，紫外線{uv}。"
    
    # --- 模擬 AI 生成的語氣 (如果暫時沒接 API，這段也很專業) ---
    advice = f"### 🤖 AI 管家今日提醒：\n"
    
    # 穿衣建議
    if temp < 15: advice += f"🧥 **穿衣方面**：今天感覺挺冷的，建議穿上厚大衣或羽絨服，裡面加件保暖內衣。\n"
    elif 15 <= temp < 22: advice += f"薄外套 **穿衣方面**：天氣微涼，穿件長袖襯衫配件薄外套最合適，方便穿脫。\n"
    else: advice += f"👕 **穿衣方面**：天氣暖和/炎熱，穿透氣的短袖即可，但室內冷氣可能較強，帶件薄校服防感冒。\n"
    
    # 雨具建議
    if rain > 40: advice += f"☔ **雨具提醒**：降雨機率有{rain}%，**一定要帶雨傘**！別心存僥倖，免得淋成落湯雞。\n"
    elif 10 < rain <= 40: advice += f"🌂 **雨具提醒**：天空雲層較厚，建議放把摺疊傘在書包備用，以防萬一。\n"
    else: advice += f"☀️ **雨具提醒**：降雨機率很低，基本不需要帶傘，可以輕便出門。\n"
    
    # 環境提醒
    if humidity > 80: advice += f"💧 **環境注意**：澳門今天濕氣很重，洗好的衣服可能很難乾，出門記得關好門窗，回家記得開除濕機。\n"
    if uv > 6: advice += f"🕶️ **防曬提醒**：紫外線指數偏高，戶外活動超過15分鐘記得塗防曬或戴帽子。\n"
    
    return advice

# --- 3. 網頁介面展示 ---
st.title("🛡️ 智慧生活：AI 懶人天氣決策系統")
st.write("針對澳門學生開發，解決「穿衣糾結」與「要不要帶傘」的終極方案。")

city = st.sidebar.selectbox("選擇你的城市", ["Macau", "Zhuhai", "Hong Kong", "Guangzhou", "Shenzhen"])

if st.sidebar.button("獲取今日 AI 決策"):
    with st.spinner("AI 正在分析雲端氣象數據..."):
        weather = get_weather_data(city)
        
        if weather:
            temp, feels, hum, uv, desc, rain = weather
            
            # 展示數據卡片
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("實際氣溫", f"{temp}°C")
            col2.metric("體感溫度", f"{feels}°C")
            col3.metric("空氣濕度", f"{hum}%")
            col4.metric("降雨機率", f"{rain}%")
            
            st.write(f"**當前天氣狀態：** {desc}")
            st.divider()
            
            # 展示 AI 建議
            full_advice = get_ai_advice(temp, hum, uv, rain, desc)
            st.markdown(f'<div class="advice-box">{full_advice}</div>', unsafe_allow_html=True)
            
        else:
            st.error("數據獲取失敗，請檢查網路連線。")

st.sidebar.info("本系統由高三畢業專題研究項目支持，旨在實現『認知卸載』。")
