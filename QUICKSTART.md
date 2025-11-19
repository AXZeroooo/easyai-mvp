# 易AI - 快速開始指南

5 分鐘快速啟動您的 AI 命理應用！

---

## ⚡ 最快啟動方式

### 步驟 1: 安裝依賴

```bash
pip install -r requirements.txt
```

### 步驟 2: 設定 API Key

**如果您的環境已有 `OPENAI_API_KEY`，跳過此步驟。**

否則，建立 `.streamlit/secrets.toml`：

```toml
OPENAI_API_KEY = "sk-your-actual-api-key"
```

### 步驟 3: 啟動應用

```bash
./run.sh
```

或

```bash
streamlit run app.py
```

### 步驟 4: 開始使用

瀏覽器會自動開啟 http://localhost:8501

---

## 🎯 使用流程

1. **輸入出生資訊**
   - 選擇出生日期
   - 選擇出生時間

2. **點擊「大師請指點」**
   - 系統自動計算八字
   - AI 生成運勢解析

3. **查看結果**
   - 八字四柱展示
   - 流日運勢解析
   - 改運建議

4. **自動記錄**
   - 數據自動存入 `corpus_data.csv`
   - 側邊欄顯示語料庫統計

---

## 📂 核心檔案說明

| 檔案 | 說明 |
|------|------|
| `app.py` | Streamlit 前端介面 |
| `bazi_engine.py` | 八字計算與 AI 分析核心 |
| `logger.py` | 數據收割與語料庫管理 |
| `corpus_data.csv` | 語料庫數據（自動生成） |

---

## 🔧 測試模組

### 測試八字引擎

```bash
python3.11 bazi_engine.py
```

**預期輸出：**
```
✅ 八字計算成功
出生時間: 1990年01月01日 12時00分
農曆: 一九八九年腊月初五
八字: 己巳 丙子 丙寅 甲午
日主: 丙 (火行)

AI 解析:
此命日主丙火，坐寅木生助...
```

### 測試數據記錄器

```bash
python3.11 logger.py
```

**預期輸出：**
```
✅ 已建立新的語料庫檔案: test_corpus.csv
✅ 已記錄數據到 test_corpus.csv (共 1 筆)
語料庫統計: {'total_records': 1, ...}
✅ 已匯出純文字語料到 test_corpus.txt
```

---

## 📊 查看語料庫

### CSV 格式

```bash
cat corpus_data.csv
```

### 純文字格式

```python
from logger import FortuneLogger

logger = FortuneLogger()
logger.export_to_text("corpus_text.txt")
```

---

## 🚨 常見問題

### Q: 無法啟動應用

**A:** 檢查 Python 版本與依賴安裝

```bash
python3.11 --version
pip list | grep streamlit
```

### Q: API Key 錯誤

**A:** 確認環境變數或 secrets.toml 設定

```bash
echo $OPENAI_API_KEY
cat .streamlit/secrets.toml
```

### Q: 語料庫無法寫入

**A:** 檢查檔案權限

```bash
ls -lah corpus_data.csv
chmod 644 corpus_data.csv
```

---

## 📚 進階功能

### 自訂 System Prompt

編輯 `bazi_engine.py` 第 124 行：

```python
system_prompt = """你是一位精通『天紀』與『人紀』的命理大師..."""
```

### 調整 AI 模型參數

編輯 `bazi_engine.py` 第 134-139 行：

```python
response = client.chat.completions.create(
    model="gpt-4.1-mini",  # 模型選擇
    temperature=0.8,       # 創意度 (0-2)
    max_tokens=600         # 輸出長度
)
```

### 匯出語料庫

```python
from logger import FortuneLogger

logger = FortuneLogger()
stats = logger.get_stats()
print(f"累積 {stats['total_records']} 筆數據")

logger.export_to_text("my_corpus.txt")
```

---

## 🌐 部署到雲端

詳見 [DEPLOYMENT.md](DEPLOYMENT.md)

---

**開始您的 AI 命理之旅！** 🔮
