import streamlit as st
import random
from datetime import datetime

# 網頁標題與設定
st.set_page_config(page_title="懶人出門決策器", page_icon="🤖")
st.title("🤖 AI + IoT 懶人出門助手")
st.subheader("把生活調成「懶人友好」模式")

# 模擬 IoT 數據抓取
def get_simulated_iot_data():
    weathers = ["下大雨 🌧️", "烈日 ☀️", "陰天 ☁️", "寒流 ❄️"]
    return {
        "temp": random.randint(12, 36),
        "weather": random.choice(weathers),
        "bus_min": random.randint(1, 15)
    }

# 介面排版
data = get_simulated_iot_data()

col1, col2, col3 = st.columns(3)
col1.metric("室外溫度", f"{data['temp']} °C")
col2.metric("當前天氣", data['weather'])
col3.metric("公車到站", f"{data['bus_min']} 分鐘")

st.divider()

# AI 決策邏輯展示
st.write("### 🤖 AI 管家給您的懶人指令：")

# 這裡模擬 AI 根據 IoT 數據生成的建議
if data['temp'] > 30:
    wear = "短袖 + 小風扇"
elif data['temp'] < 18:
    wear = "發熱衣 + 擋風外套"
else:
    wear = "一件薄長袖"

if "雨" in data['weather']:
    kit = "拿自動傘，穿防水鞋"
else:
    kit = "什麼都不用帶，空手萬歲"

if data['bus_min'] <= 3:
    action = "🏃 **別看了！現在跑出去剛好趕上！**"
else:
    action = f"🍵 還可以慢慢晃 {data['bus_min']-3} 分鐘再出門。"

st.info(f"👉 **建議穿著：** {wear}")
st.info(f"👉 **必備裝備：** {kit}")
st.success(f"👉 **行動指令：** {action}")

# 底部按鈕
if st.button('重新刷新環境數據'):
    st.rerun()
