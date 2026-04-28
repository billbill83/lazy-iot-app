import streamlit as st
import requests
import random
from datetime import datetime
from duckduckgo_search import DDGS

# --- 1. 網頁基礎配置 (更適合手機瀏覽) ---
st.set_page_config(page_title="AI 澳門生活管家", page_icon="🇲🇴", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .ai-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        border-top: 5px solid #00a8ff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #333;
        font-size: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #00a8ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇲🇴 AI 智慧生活管家 (澳門精細版)")

# --- 2. 精細化地區座標庫 ---
# 加入了你提到的青洲、黑沙環、黑沙等
city_coords = {
    "澳門 - 青洲 (Ilha Verde)": {"lat": 22.2105, "lon": 113.5375},
    "澳門 - 黑沙環 (Areia Preta)": {"lat": 22.2070, "lon": 113.5530},
    "澳門 - 中區/新馬路": {"lat": 22.1930, "lon": 113.5410},
    "澳門 - 氹仔舊城區": {"lat": 22.1530, "lon": 113.5570},
    "澳門 - 路環黑沙 (Hac Sa)": {"lat": 22.1260, "lon": 113.5660},
    "珠海 - 拱北口岸": {"lat": 22.2210, "lon": 113.5500}
}
selected_city = st.sidebar.selectbox("📍 選擇詳細觀測點", list(city_coords.keys()))

# --- 3. 穩定版數據獲取函數 ---
@st.cache_data(ttl=300) # 緩存5分鐘，避免頻繁請求
def fetch_weather_safe(city_name):
    try:
        c = city_coords[city_name]
        # 使用 Open-Meteo，增加 fallback 備用參數
        url = f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}&current_weather=true&hourly=relative_humidity_2m,precipitation_probability,uv_index&timezone=auto"
        response = requests.get(url, timeout=5)
        res = response.json()
        
        if 'current_weather' not in res:
            return None
            
        now_hour = datetime.now().hour
        return {
            "temp": res['current_weather']['temperature'],
            "wind": res['current_weather']['windspeed'],
            "hum": res['hourly']['relative_humidity_2m'][now_hour],
            "rain": res['hourly']['precipitation_probability'][now_hour],
            "uv": res['hourly']['uv_index'][now_hour]
        }
    except:
        return None

# --- 4. 多樣化決策引擎 ---
def get_smart_advice(data, city):
    # 豐富風格庫
    styles = ["專業管家", "毒舌室友", "幽默達人", "極簡主義者", "養生專家"]
    # 豐富關注點
    focus_points = [
        "穿衣層次與外套建議 (是否需要防風)",
        "防曬措施 (SPF、帽子、墨鏡)",
        "雨具準備 (傘、防水鞋、室內避雨)",
        "體感溫度與濕度應對 (髮型、皮膚保養)",
        "戶外活動可行性 (適合散步還是留在家看劇)"
    ]
    
    style = random.choice(styles)
    focus = random.choice(focus_points)

    try:
        with DDGS() as ddgs:
            # 構建強大的系統提示
            prompt = (
                f"你是{city}的AI助手，風格為「{style}」。"
                f"當前氣候：溫度{data['temp']}°C, 濕度{data['hum']}%, 降雨{data['rain']}%, UV{data['uv']}。"
                f"請針對以下重點給出50字內建議，必須包含『穿衣層次』、『是否帶外套』、『防曬』與『雨具』。"
                f"重點：{focus}"
            )
            response = ddgs.chat(prompt, model='gpt-4o-mini')
            return response
    except:
        # 當 AI 連線失敗時的本地硬核邏輯 (Hard-coded Logic)
        advice = f"🧥 溫度 {data['temp']}°C，"
        advice += "建議穿件防風外套。" if data['temp'] < 22 else "短袖即可，帶件薄衫防冷氣。"
        advice += " ☀️ UV強烈，記得防曬。" if data['uv'] > 5 else ""
        advice += " ☔ 降雨率高，出門請帶傘。" if data['rain'] > 30 else " ☁️ 天氣尚可，不需帶傘。"
        return advice

# --- 5. UI 呈現邏輯 ---
data = fetch_weather_safe(selected_city)

if data:
    # 數據儀表盤
    st.subheader(f"📊 {selected_city} 實時環境")
    m1, m2, m3 = st.columns(3)
    m1.metric("氣溫", f"{data['temp']}°C")
    m2.metric("降雨", f"{data['rain']}%")
    m3.metric("UV指數", f"{data['uv']}")
    
    st.divider()
    
    # 決策按鈕
    if st.button("🔄 獲取 AI 穿搭與出門建議"):
        with st.spinner("🧠 AI 正在思考最適合澳門的穿搭..."):
            advice = get_smart_advice(data, selected_city)
            st.markdown(f'<div class="ai-card">{advice}</div>', unsafe_allow_html=True)
            st.balloons()
else:
    st.error("⚠️ 暫時無法獲取該微小區域的氣象數據，請嘗試切換至相鄰區域。")

st.caption(f"📍 精確座標數據 | 更新時間: {datetime.now().strftime('%H:%M:%S')}")
