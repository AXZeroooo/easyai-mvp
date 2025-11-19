"""
eeasy.ai | Case 01: Metaphysics
讓複雜被 AI 變簡單 - 八字系統數據化實驗
"""

import streamlit as st
from datetime import datetime, time, date
from bazi_engine import get_fortune
from logger import FortuneLogger
from gsheets_logger import GoogleSheetsLogger
import os


# ============================================================
# 頁面配置
# ============================================================
st.set_page_config(
    page_title="eeasy.ai | Case 01: Metaphysics",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# 自定義 CSS
# ============================================================
st.markdown("""
<style>
    /* 主標題 */
    .main-title {
        text-align: center;
        color: #2C3E50;
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 0.2em;
        letter-spacing: 0.05em;
    }
    
    /* Hero Headline */
    .hero-headline {
        text-align: center;
        color: #E74C3C;
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 0.5em;
    }
    
    /* Sub-headline */
    .sub-headline {
        text-align: center;
        color: #7F8C8D;
        font-size: 1.1em;
        line-height: 1.6;
        margin-bottom: 2em;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* 四柱容器 */
    .pillar-container {
        display: flex;
        justify-content: center;
        gap: 1.5em;
        margin: 2em 0;
        flex-wrap: wrap;
    }
    
    /* 四柱卡片 */
    .pillar-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2em 1.8em;
        border-radius: 12px;
        color: white;
        text-align: center;
        min-width: 120px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .pillar-box:hover {
        transform: translateY(-5px);
    }
    
    .pillar-label {
        font-size: 0.9em;
        opacity: 0.9;
        margin-bottom: 0.3em;
    }
    
    .pillar-value {
        font-size: 2em;
        font-weight: bold;
    }
    
    /* 運勢框 */
    .fortune-box {
        background: #F8F9FA;
        color: #2c3e50;
        padding: 1.5em;
        border-radius: 12px;
        border-left: 4px solid #3498DB;
        margin: 1.5em 0;
        line-height: 1.8;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* 錯誤訊息框 */
    .error-box {
        background: #FFF3CD;
        border-left: 4px solid #FF9800;
        padding: 1em 1.5em;
        border-radius: 8px;
        margin: 1em 0;
    }
    
    .error-title {
        color: #D32F2F;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 0.5em;
    }
    
    .error-message {
        color: #333;
        line-height: 1.6;
    }
    
    .error-icon {
        font-size: 1.3em;
        margin-right: 0.3em;
    }
    
    /* 統計框 */
    .stats-box {
        background: #E8F5E9;
        padding: 1em;
        border-radius: 8px;
        font-size: 0.95em;
        line-height: 1.8;
    }
    
    /* AEO Banner */
    .aeo-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5em;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2em;
        line-height: 1.8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* 按鈕樣式 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2em;
        font-weight: 600;
        padding: 0.8em 2em;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 初始化 Logger
# ============================================================
@st.cache_resource
def get_csv_logger():
    """初始化 CSV Logger（本地備份）"""
    return FortuneLogger("corpus_data.csv")

@st.cache_resource
def get_gsheets_logger():
    """初始化 Google Sheets Logger（雲端數據資產）"""
    try:
        logger = GoogleSheetsLogger()
        if logger.connect():
            return logger
        else:
            return None
    except Exception as e:
        print(f"Google Sheets Logger 初始化失敗: {e}")
        return None

csv_logger = get_csv_logger()
gsheets_logger = get_gsheets_logger()

# ============================================================
# 標題區
# ============================================================
st.markdown('<div class="main-title">🧠 eeasy.ai</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title" style="font-size: 1.2em; color: #7F8C8D;">Case 01: Metaphysics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-headline">讓複雜被 AI 變簡單。</div>', unsafe_allow_html=True)
st.markdown("""
<div class="sub-headline">
    Case 01：我們用 AI 解構了古老的八字系統。<br/>
    輸入生日，體驗「數據化」的運勢解析。
</div>
""", unsafe_allow_html=True)

# ============================================================
# 側邊欄
# ============================================================
with st.sidebar:
    st.header("📖 關於 eeasy.ai")
    
    st.markdown("""
    <div class="aeo-banner">
        <strong>🧪 AI 賦能實驗室</strong><br/><br/>
        本專案是 eeasy.ai 的首個實驗場域，<br/>
        旨在驗證「複雜知識 AI 化」的可能性。
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Case 01: Metaphysics**
    
    我們選擇「八字命理」作為第一個實驗對象，因為：
    - ✅ 系統複雜但規則明確
    - ✅ 需要大量專業知識
    - ✅ 適合 AI 數據化處理
    
    **實驗目標**：
    1. 將傳統八字系統數據化
    2. 用 AI 生成白話解析
    3. 累積訓練語料庫
    """)
    
    st.divider()
    
    # 語料庫統計
    st.subheader("📊 數據資產統計")
    
    # 優先顯示 Google Sheets 統計
    if gsheets_logger:
        stats = gsheets_logger.get_stats()
        st.markdown(f"""
        <div class="stats-box">
            🌐 <strong>Google Sheets</strong><br/>
            📝 累積筆數: <strong>{stats['total_records']}</strong><br/>
            📅 最新記錄: {stats['latest_timestamp'] or '尚無記錄'}<br/>
            ✅ 狀態: {stats['status']}
        </div>
        """, unsafe_allow_html=True)
    else:
        # 降級為 CSV 統計
        stats = csv_logger.get_stats()
        st.markdown(f"""
        <div class="stats-box">
            💾 <strong>本地 CSV</strong><br/>
            📝 累積筆數: <strong>{stats['total_records']}</strong><br/>
            📅 最新記錄: {stats['latest_timestamp'] or '尚無記錄'}<br/>
            💾 檔案大小: {stats['file_size_kb']} KB
        </div>
        """, unsafe_allow_html=True)
    
    # CSV 下載功能（本地備份）
    st.divider()
    st.subheader("💾 本地備份")
    
    import os
    csv_path = "corpus_data.csv"
    
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as file:
            csv_data = file.read()
        
        st.download_button(
            label="📥 下載 CSV 備份",
            data=csv_data,
            file_name=f"eeasy_corpus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="下載所有累積的八字與 AI 解析語料"
        )
        st.caption("💡 建議每日備份一次。")
    else:
        st.info("📄 尚無本地記錄。")
    
    st.divider()
    st.caption("⚠️ 本系統僅供實驗參考，不構成任何決策建議。")

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

# 合併日期與時間
birth_datetime = datetime.combine(birth_date, birth_time)

# ============================================================
# 分析按鈕
# ============================================================
st.markdown("<br/>", unsafe_allow_html=True)

if st.button("🧠 AI 顧問請分析", use_container_width=True):
    with st.spinner("🔮 正在解構八字數據..."):
        result = get_fortune(birth_datetime)
        
        if result['success']:
            # 顯示農曆與日主資訊
            st.success(f"**農曆生日**：{result['lunar_date']}")
            st.info(f"**日主**：{result['day_master']} ({result['day_master_element']}行)")
            
            # 顯示八字四柱
            st.markdown("### 八字四柱")
            bazi_parts = result['bazi_full'].split()
            
            pillars_html = '<div class="pillar-container">'
            labels = ['年柱', '月柱', '日柱', '時柱']
            for i, (label, pillar) in enumerate(zip(labels, bazi_parts)):
                pillars_html += f'''
                <div class="pillar-box">
                    <div class="pillar-label">{label}</div>
                    <div class="pillar-value">{pillar}</div>
                </div>
                '''
            pillars_html += '</div>'
            st.markdown(pillars_html, unsafe_allow_html=True)
            
            # 顯示 AI 運勢解析
            st.markdown("### 💡 AI 運勢解析")
            st.markdown(f'''
            <div class="fortune-box">
                {result['ai_fortune']}
            </div>
            ''', unsafe_allow_html=True)
            
            # 記錄到 CSV（本地備份）
            csv_logger.log_fortune(result)
            
            # 記錄到 Google Sheets（雲端數據資產）
            if gsheets_logger:
                gsheets_logger.log_fortune(result)
                st.success("✅ 已自動記錄到雲端數據庫")
            else:
                st.warning("⚠️ Google Sheets 未連接，僅記錄到本地 CSV")
        
        else:
            # 顯示錯誤訊息
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
            
            # 即使失敗也記錄（用於除錯）
            csv_logger.log_fortune(result)

# ============================================================
# 頁尾說明
# ============================================================
st.markdown("<br/><br/>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7F8C8D; font-size: 0.9em; line-height: 1.8;">
    <strong>eeasy.ai</strong> | 讓複雜被 AI 變簡單<br/>
    Case 01: Metaphysics - 八字系統數據化實驗<br/>
    每次解析自動累積語料，持續優化 AI 模型<br/><br/>
    <small>© 2025 eeasy.ai | AI-Powered Knowledge Simplification</small>
</div>
""", unsafe_allow_html=True)
