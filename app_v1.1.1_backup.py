"""
易AI - 每日運勢 MVP
AEO 導向的八字命理與 AI 運勢分析系統
"""

import streamlit as st
from datetime import datetime, time, date
from bazi_engine import get_fortune
from logger import FortuneLogger


# ============================================================
# 頁面配置
# ============================================================
st.set_page_config(
    page_title="易AI - 每日運勢 MVP",
    page_icon="🔮",
    layout="centered"
)

# ============================================================
# 自定義 CSS
# ============================================================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #8B4513;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.3em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 1.5em;
    }
    .pillar-container {
        display: flex;
        justify-content: center;
        gap: 1.5em;
        margin: 1.5em 0;
    }
    .pillar-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1em 1.5em;
        border-radius: 10px;
        color: white;
        text-align: center;
        min-width: 80px;
    }
    .pillar-label {
        font-size: 0.85em;
        opacity: 0.9;
        margin-bottom: 0.3em;
    }
    .pillar-value {
        font-size: 1.5em;
        font-weight: bold;
    }
    .fortune-box {
        background: #f8f9fa;
        padding: 1.5em;
        border-radius: 10px;
        border-left: 4px solid #8B4513;
        margin-top: 1em;
        line-height: 1.8;
        color: #2c3e50;
    }
    .aeo-banner {
        background: linear-gradient(135deg, #FFA500 0%, #FF6347 100%);
        color: white;
        padding: 1em;
        border-radius: 8px;
        margin: 1em 0;
        text-align: center;
        font-weight: 500;
    }
    .error-box {
        background: #fff3cd;
        border-left: 4px solid #ff9800;
        padding: 1em 1.5em;
        border-radius: 8px;
        margin: 1em 0;
    }
    .error-box .error-icon {
        color: #ff9800;
        font-size: 1.2em;
        margin-right: 0.5em;
    }
    .error-box .error-title {
        color: #d32f2f;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 0.5em;
    }
    .error-box .error-message {
        color: #333;
        line-height: 1.6;
    }
    .stats-box {
        background: #e8f5e9;
        padding: 0.8em;
        border-radius: 6px;
        font-size: 0.9em;
        margin-top: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 初始化 Logger
# ============================================================
@st.cache_resource
def get_logger():
    """初始化並快取 Logger 實例"""
    return FortuneLogger("corpus_data.csv")

logger = get_logger()

# ============================================================
# 標題區
# ============================================================
st.markdown('<div class="main-title">🔮 易AI - 每日運勢 MVP</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">傳統命理 × 中醫理論 × AI 賦能分析</div>', unsafe_allow_html=True)

# ============================================================
# AEO 聲明（置頂）
# ============================================================
st.markdown("""
<div class="aeo-banner">
    <strong>🌟 易AI 實驗計畫</strong><br/>
    專門研究 <strong>易經 × AI × 台灣場景</strong> 的創新應用。<br/>
    使用 Boss 自研八字計算引擎，結合 AI 命理與倪海廈系統邏輯，<br/>
    提供繁體中文使用者專屬的 AI 流日解析。
</div>
""", unsafe_allow_html=True)

# ============================================================
# 側邊欄
# ============================================================
with st.sidebar:
    st.header("📖 使用說明")
    st.markdown("""
    **易AI** 結合傳統八字命理與現代 AI 技術，為您提供精準的流日運勢分析。
    
    **特色：**
    - ✅ 自動農曆轉換與八字排盤
    - ✅ AI 命理專業風格解析（直接明確、取象為上）
    - ✅ 具體改運建議（方位、穿著、飲食）
    - ✅ 自動累積訓練語料庫
    
    **使用步驟：**
    1. 輸入您的出生日期與時間
    2. 點擊「大師請指點」按鈕
    3. 查看八字排盤與運勢解析
    """)
    
    st.divider()
    
    # 語料庫統計
    st.subheader("📊 語料庫統計")
    stats = logger.get_stats()
    st.markdown(f"""
    <div class="stats-box">
        📝 累積筆數: <strong>{stats['total_records']}</strong><br/>
        📅 最新記錄: {stats['latest_timestamp'] or '尚無記錄'}<br/>
        💾 檔案大小: {stats['file_size_kb']} KB
    </div>
    """, unsafe_allow_html=True)
    
    # CSV 下載功能
    st.divider()
    st.subheader("💾 語料庫備份")
    
    import os
    csv_path = "corpus_data.csv"
    
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as file:
            csv_data = file.read()
        
        st.download_button(
            label="📥 下載歷史語料 CSV",
            data=csv_data,
            file_name=f"easyai_corpus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="下載所有累積的八字與 AI 解析語料"
        )
        st.caption("💡 建議每日備份一次，以免資料遺失。")
    else:
        st.info("📄 尚無語料記錄，請先進行一次運勢查詢。")
    
    st.divider()
    st.caption("⚠️ 本系統僅供娛樂參考，不構成任何決策建議。")

# ============================================================
# 主要輸入區
# ============================================================
st.header("📅 請輸入您的出生資訊")

col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input(
        "出生日期",
        value=date(1990, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=datetime.now().date()
    )

with col2:
    birth_time = st.time_input(
        "出生時間",
        value=time(12, 0)
    )

st.divider()

# ============================================================
# 分析按鈕
# ============================================================
if st.button("🔮 大師請指點", type="primary", use_container_width=True):
    with st.spinner("🌟 大師正在排盤推算中..."):
        # 呼叫核心引擎
        result = get_fortune(birth_date, birth_time)
        
        if result["success"]:
            # === 顯示八字排盤 ===
            st.success("✅ 排盤完成！")
            
            st.markdown("### 📊 您的八字命盤")
            
            # 基本資訊
            st.info(f"""
            **陽曆生日：** {result['birth_datetime']}  
            **農曆生日：** {result['lunar_date']}  
            **日主：** {result['day_master']} ({result['day_master_element']}行)
            """)
            
            # 四柱展示（使用 Columns）
            st.markdown("**八字四柱**")
            col_year, col_month, col_day, col_time = st.columns(4)
            
            with col_year:
                st.markdown(f"""
                <div class="pillar-box">
                    <div class="pillar-label">年柱</div>
                    <div class="pillar-value">{result['year_pillar']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_month:
                st.markdown(f"""
                <div class="pillar-box">
                    <div class="pillar-label">月柱</div>
                    <div class="pillar-value">{result['month_pillar']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_day:
                st.markdown(f"""
                <div class="pillar-box">
                    <div class="pillar-label">日柱</div>
                    <div class="pillar-value">{result['day_pillar']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_time:
                st.markdown(f"""
                <div class="pillar-box">
                    <div class="pillar-label">時柱</div>
                    <div class="pillar-value">{result['time_pillar']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # === 運勢解析 ===
            st.markdown("### 🌟 流日運勢解析")
            st.markdown(f'<div class="fortune-box">{result["ai_fortune"]}</div>', unsafe_allow_html=True)
            
            # === 自動記錄數據 ===
            log_success = logger.log_fortune(result)
            if log_success:
                st.success("✅ 已自動記錄到語料庫")
            
            # 儲存到 session state
            st.session_state['last_reading'] = result
            
        else:
            # 顯示錯誤（使用自訂 HTML 確保文字清晰可見）
            st.markdown(f"""
            <div class="error-box">
                <div class="error-title">
                    <span class="error-icon">⚠️</span>
                    AI 解析失敗
                </div>
                <div class="error-message">
                    {result['error']}<br/>
                    <small>請檢查 API Key 設定或網路連線。</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 請確認：\n1. 已正確設定 OPENAI_API_KEY\n2. 網路連線正常\n3. 日期時間輸入有效")

# ============================================================
# 歷史記錄
# ============================================================
if 'last_reading' in st.session_state:
    with st.expander("📜 查看上次解析記錄"):
        last = st.session_state['last_reading']
        st.write(f"**分析時間：** {last['birth_datetime']}")
        st.write(f"**八字：** {last['bazi_full']}")
        st.write(f"**日主：** {last['day_master']} ({last['day_master_element']}行)")

# ============================================================
# 頁尾
# ============================================================
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9em;">
    易AI © 2025 | Powered by Streamlit & OpenAI<br/>
    傳統命理與中醫理論結合 · 直接明確 · 取象為上<br/>
    <em>每次解析自動累積語料，持續優化 AI 命理模型</em>
</div>
""", unsafe_allow_html=True)
