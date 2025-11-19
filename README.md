# 易AI - 每日運勢 MVP

**AEO 導向的八字命理與 AI 運勢分析系統**

專門研究 **易經 × AI × 台灣場景** 的創新應用。使用 Boss 自研八字計算引擎，結合 AI 命理與傳統命理系統邏輯，提供繁體中文使用者專屬的 AI 流日解析。

---

## 🌟 功能特色

- ✅ **自動農曆轉換**：陽曆轉農曆，精準計算干支
- ✅ **八字排盤**：自動計算年月日時四柱
- ✅ **AI 命理解析**：整合 OpenAI GPT，傳統命理風格論命
- ✅ **改運建議**：提供具體的方位、穿著、飲食建議
- ✅ **數據收割**：自動累積訓練語料庫（CSV 格式）
- ✅ **模組化架構**：核心邏輯、數據記錄、前端分離

---

## 📦 技術架構

### 核心技術棧

- **前端框架**：Streamlit
- **農曆計算**：lunar-python
- **AI 引擎**：OpenAI GPT-4.1-mini（或 Manus LLM Proxy）
- **數據處理**：Pandas
- **語言**：Python 3.11+

### 專案結構

```
easyai/
├── app.py                  # Streamlit 主應用（前端）
├── bazi_engine.py         # 八字計算與 AI 分析核心引擎
├── logger.py              # 數據收割模組（語料庫累積）
├── requirements.txt       # Python 依賴清單
├── run.sh                 # 快速啟動腳本
├── corpus_data.csv        # 語料庫數據（自動生成）
├── .streamlit/
│   └── secrets.toml      # Streamlit 密鑰配置
├── .env.example          # 環境變數範例
└── README.md             # 本文件
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 建立虛擬環境（推薦）
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴套件
pip install -r requirements.txt
```

### 2. 配置環境變數

#### 🔧 重要：環境變數配置

本專案需要以下環境變數才能正常運作：

| 變數 | 必要性 | 說明 | 範例 |
|------|--------|------|------|
| `OPENAI_API_KEY` | ✅ 必要 | OpenAI API Key | `sk-proj-xxx...` |
| `OPENAI_BASE_URL` | ⚠️ 建議 | API 端點 URL | `https://api.openai.com/v1` |

#### 配置方法

**方法 A：使用 Streamlit Secrets（推薦本地開發）**

編輯 `.streamlit/secrets.toml`：

```toml
OPENAI_API_KEY = "sk-proj-your-actual-api-key"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

**方法 B：使用環境變數**

```bash
export OPENAI_API_KEY="sk-proj-your-actual-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

**方法 C：使用 .env 檔案**

建立 `.env` 檔案：

```bash
OPENAI_API_KEY=sk-proj-your-actual-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

#### 🌐 Manus 環境說明

如果您在 **Manus 沙盒環境**中運行，環境變數已預設配置：

```bash
OPENAI_API_KEY=sk-XzyZG2yfXrQFHtj2bvxJxg
OPENAI_BASE_URL=https://api.manus.im/api/llm-proxy/v1
```

**無需手動設定**，可直接運行。

### 3. 運行應用

**方式 1：使用啟動腳本（推薦）**

```bash
chmod +x run.sh
./run.sh
```

**方式 2：手動啟動**

```bash
streamlit run app.py
```

應用將自動在瀏覽器開啟（預設 http://localhost:8501）

---

## 📚 模組說明

### A. 核心引擎 (`bazi_engine.py`)

**主要函數：`get_fortune(birth_date, birth_time)`**

- **輸入**：
  - `birth_date`: datetime.date 對象
  - `birth_time`: datetime.time 對象

- **輸出**：dict 包含以下欄位
  - `success`: 是否成功
  - `birth_datetime`: 出生時間字串
  - `lunar_date`: 農曆日期
  - `year_pillar`, `month_pillar`, `day_pillar`, `time_pillar`: 四柱干支
  - `day_master`: 日主天干
  - `day_master_element`: 日主五行
  - `bazi_full`: 完整八字字串
  - `ai_fortune`: AI 生成的運勢解析
  - `error`: 錯誤訊息（若有）

**環境變數依賴**：
- ✅ `OPENAI_API_KEY`（必要）
- ✅ `OPENAI_BASE_URL`（建議）

**測試範例：**

```python
from datetime import date, time
from bazi_engine import get_fortune

result = get_fortune(date(1990, 1, 1), time(12, 0))
print(result['bazi_full'])  # 己巳 丙子 丙寅 甲午
print(result['ai_fortune'])  # AI 生成的運勢文案
```

### B. 數據收割 (`logger.py`)

**主要類別：`FortuneLogger`**

- **初始化**：`logger = FortuneLogger("corpus_data.csv")`
- **記錄數據**：`logger.log_fortune(fortune_data)`
- **獲取統計**：`stats = logger.get_stats()`
- **匯出文字**：`logger.export_to_text("corpus_text.txt")`

**語料庫欄位：**

| 欄位 | 說明 |
|------|------|
| Timestamp | 記錄時間戳 |
| Birth_DateTime | 用戶出生時間 |
| Lunar_Date | 農曆日期 |
| Bazi_Chart | 完整八字 |
| Day_Master | 日主天干 |
| Day_Master_Element | 日主五行 |
| AI_Output | GPT 生成的完整運勢文案 |

**測試範例：**

```python
from logger import FortuneLogger

logger = FortuneLogger()
stats = logger.get_stats()
print(f"累積筆數: {stats['total_records']}")
```

### C. 前端介面 (`app.py`)

- **AEO 聲明**：置頂顯示專案定位
- **輸入區**：日期選擇器 + 時間選擇器
- **輸出區**：四柱展示（4 Columns）+ AI 解析（Markdown）
- **側邊欄**：使用說明 + 語料庫統計
- **自動記錄**：每次生成運勢自動存入 CSV

---

## 🌐 部署到 Streamlit Cloud

### 步驟

1. **推送代碼到 GitHub**

```bash
git init
git add .
git commit -m "Initial commit: EasyAI MVP with data logging"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **登入 Streamlit Cloud**
   - 前往 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 帳號登入

3. **部署應用**
   - 點擊 "New app"
   - 選擇您的 GitHub repository
   - Main file path: `app.py`
   - 點擊 "Deploy"

4. **設定 Secrets**
   - 在 Streamlit Cloud 應用設定中
   - 找到 "Secrets" 區域
   - 貼上以下內容：
     ```toml
     OPENAI_API_KEY = "sk-proj-your-actual-api-key"
     OPENAI_BASE_URL = "https://api.openai.com/v1"
     ```

---

## 🐛 故障排除

### 問題 1：401 External tokens are not supported

**原因**：環境變數 `OPENAI_BASE_URL` 未正確設定

**解決方案**：

1. 檢查環境變數：
   ```bash
   echo $OPENAI_BASE_URL
   ```

2. 設定正確的 base_url：
   ```bash
   export OPENAI_BASE_URL="https://api.openai.com/v1"
   ```

3. 或在 `.streamlit/secrets.toml` 中加入：
   ```toml
   OPENAI_BASE_URL = "https://api.openai.com/v1"
   ```

### 問題 2：API Key 無效

**原因**：API Key 過期或無效

**解決方案**：

1. 前往 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 生成新的 API Key
3. 更新環境變數或 secrets.toml

### 問題 3：無法啟動應用

**檢查清單**：
- Python 版本是否為 3.11+
- 是否已安裝所有依賴
- 是否已啟動虛擬環境

---

## 📊 數據收割與語料庫

### 目的

每次用戶查詢運勢，系統會自動將以下資料存入 `corpus_data.csv`：

- 用戶輸入的生辰資訊
- 計算出的八字干支
- AI 生成的完整運勢文案

**這份語料庫未來可用於：**

1. 訓練專屬的命理 AI 模型
2. 分析用戶偏好與查詢模式
3. 優化 Prompt 與輸出品質
4. 建立繁體中文命理知識庫

### 匯出語料

```python
from logger import FortuneLogger

logger = FortuneLogger()
logger.export_to_text("corpus_text.txt")  # 匯出為純文字格式
```

---

## 🎯 使用範例

1. 開啟應用（http://localhost:8501）
2. 輸入出生日期：1990-01-01
3. 輸入出生時間：12:00
4. 點擊「大師請指點」
5. 查看八字排盤與 AI 運勢解析
6. 系統自動記錄到 `corpus_data.csv`

---

## ⚠️ 注意事項

- 本系統僅供娛樂參考，不構成任何決策建議
- 需要有效的 OpenAI API Key 才能使用 AI 分析功能
- API 調用會產生費用，請注意使用量
- 語料庫檔案 `corpus_data.csv` 會持續累積，請定期備份
- **環境變數配置**：確保 `OPENAI_BASE_URL` 正確設定

---

## 🔧 開發指南

### 測試核心模組

```bash
# 測試八字引擎
python3.11 bazi_engine.py

# 測試數據記錄器
python3.11 logger.py
```

### 自訂 System Prompt

編輯 `bazi_engine.py` 中的 `_generate_ai_fortune()` 函數：

```python
system_prompt = """你是一位精通『天紀』與『人紀』的命理大師..."""
```

### 調整 AI 模型

修改 `bazi_engine.py` 中的模型參數：

```python
response = client.chat.completions.create(
    model="gpt-4.1-mini",  # 可改為其他模型
    temperature=0.8,       # 調整創意度
    max_tokens=600         # 調整輸出長度
)
```

---

## 📄 授權

MIT License

---

## 🙏 致謝

- **傳統命理大師**：論命風格與中醫經絡理論
- **lunar-python**：農曆轉換庫
- **OpenAI**：GPT 語言模型
- **Streamlit**：快速原型開發框架

---

## 📞 技術支援

如遇到問題，請查閱：

1. **BUGFIX_REPORT.md** - 已知問題與解決方案
2. **QUICKSTART.md** - 快速開始指南
3. **DEPLOYMENT.md** - 部署指南

---

**易AI © 2025** | 繼承傳統命理大師論命精神 · 直斷生殺 · 取象為上

*每次解析自動累積語料，持續優化 AI 命理模型*
