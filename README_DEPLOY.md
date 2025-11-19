# 易AI - 八字命理與 AI 運勢分析 MVP

**傳統命理 × 中醫理論 × AI 賦能分析**

專門研究 **易經 × AI × 台灣場景** 的創新應用。使用自研八字計算引擎，結合 AI 命理與傳統命理系統邏輯，提供繁體中文使用者專屬的 AI 流日解析。

---

## 🌟 功能特色

- ✅ **自動農曆轉換** - 陽曆轉農曆，精準計算干支
- ✅ **八字排盤** - 自動計算年月日時四柱
- ✅ **AI 命理解析** - 整合 OpenAI GPT，傳統命理風格論命
- ✅ **改運建議** - 提供具體的方位、穿著、飲食建議
- ✅ **數據收割** - 自動累積訓練語料庫（CSV 格式）
- ✅ **語料備份** - 一鍵下載歷史語料 CSV

---

## 🚀 快速開始

### 線上使用

訪問 Streamlit Cloud 部署版本：
**[https://easyai-mvp.streamlit.app](https://easyai-mvp.streamlit.app)** *(待部署)*

### 本地運行

```bash
# 1. 克隆專案
git clone https://github.com/AXZeroooo/easyai-mvp.git
cd easyai-mvp

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定環境變數
cp .env.example .env
# 編輯 .env，填入您的 OPENAI_API_KEY

# 4. 運行應用
streamlit run app.py
```

---

## 📦 專案結構

```
easyai-mvp/
├── app.py              # Streamlit 前端應用
├── bazi_engine.py     # 八字計算與 AI 分析引擎
├── logger.py          # 數據收割模組
├── requirements.txt   # Python 依賴清單
├── .env.example       # 環境變數範例
└── README.md          # 本文件
```

---

## ⚙️ 環境變數配置

本專案需要以下環境變數：

| 變數 | 說明 | 範例 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API Key | `sk-proj-xxx...` |
| `OPENAI_BASE_URL` | API 端點（可選） | `https://api.openai.com/v1` |

### Streamlit Cloud 配置

在 Streamlit Cloud 的 **Secrets** 設定中加入：

```toml
OPENAI_API_KEY = "sk-proj-your-actual-api-key"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

---

## 💾 數據持久化

### 語料庫備份

應用會自動將每次查詢的八字與 AI 解析記錄到 `corpus_data.csv`。

**備份方式**：
1. 在側邊欄找到「💾 語料庫備份」區域
2. 點擊「📥 下載歷史語料 CSV」按鈕
3. CSV 檔案會自動下載到您的裝置

**建議**：每日備份一次，以免資料遺失（Streamlit Cloud 會定期重置檔案系統）。

### 語料庫欄位

| 欄位 | 說明 |
|------|------|
| Timestamp | 記錄時間戳 |
| Birth_DateTime | 用戶出生時間 |
| Lunar_Date | 農曆日期 |
| Bazi_Chart | 完整八字 |
| Day_Master | 日主天干 |
| Day_Master_Element | 日主五行 |
| AI_Output | GPT 生成的完整運勢文案 |

---

## 🎯 使用範例

1. 開啟應用
2. 輸入出生日期：1990-01-01
3. 輸入出生時間：12:00
4. 點擊「大師請指點」
5. 查看八字排盤與 AI 運勢解析
6. 系統自動記錄到語料庫

---

## 📊 技術棧

- **前端框架**：Streamlit
- **農曆計算**：lunar-python
- **AI 引擎**：OpenAI GPT-4.1-mini
- **數據處理**：Pandas
- **語言**：Python 3.11+

---

## 📝 版本記錄

查看 [CHANGELOG.md](CHANGELOG.md) 了解詳細的版本變更記錄。

### 最新版本：v1.1.1

- ✅ 修復 UI 文字對比度問題
- ✅ 新增 CSV 下載功能
- ✅ 優化錯誤訊息顯示
- ✅ 移除特定人名引用

---

## ⚠️ 注意事項

- 本系統僅供娛樂參考，不構成任何決策建議
- 需要有效的 OpenAI API Key 才能使用 AI 分析功能
- API 調用會產生費用，請注意使用量
- 語料庫檔案會持續累積，請定期備份

---

## 📄 授權

MIT License

---

## 🙏 致謝

- **傳統命理大師** - 論命風格與中醫經絡理論
- **lunar-python** - 農曆轉換庫
- **OpenAI** - GPT 語言模型
- **Streamlit** - 快速原型開發框架

---

**易AI © 2025** | 傳統命理與中醫理論結合 · 直接明確 · 取象為上

*每次解析自動累積語料，持續優化 AI 命理模型*
