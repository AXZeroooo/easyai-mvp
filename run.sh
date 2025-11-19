#!/bin/bash
# 易AI 快速啟動腳本

echo "🔮 易AI - 每日運勢 MVP"
echo "========================"
echo ""

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "📦 建立虛擬環境..."
    python3.11 -m venv venv
fi

# 啟動虛擬環境
echo "🔧 啟動虛擬環境..."
source venv/bin/activate

# 安裝依賴
echo "📥 安裝依賴套件..."
pip install -r requirements.txt -q

# 檢查 API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  警告: 未偵測到 OPENAI_API_KEY 環境變數"
    echo "   請確保已在 .streamlit/secrets.toml 中設定"
fi

# 啟動應用
echo ""
echo "🚀 啟動 Streamlit 應用..."
echo "========================"
streamlit run app.py
