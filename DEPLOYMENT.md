# 易AI 部署指南

本文件提供完整的本地運行與雲端部署指南。

---

## 🖥️ 本地運行

### 前置需求

- Python 3.11 或以上
- pip 套件管理器
- 有效的 OpenAI API Key

### 步驟

#### 1. 克隆或下載專案

```bash
git clone <your-repo-url>
cd easyai
```

#### 2. 建立虛擬環境

```bash
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

#### 4. 配置 API Key

**方法 A：環境變數**

```bash
export OPENAI_API_KEY="sk-your-actual-api-key"
```

**方法 B：Streamlit Secrets**

建立 `.streamlit/secrets.toml`：

```toml
OPENAI_API_KEY = "sk-your-actual-api-key"
```

#### 5. 啟動應用

**使用啟動腳本（推薦）：**

```bash
chmod +x run.sh
./run.sh
```

**手動啟動：**

```bash
streamlit run app.py
```

#### 6. 訪問應用

開啟瀏覽器，訪問 http://localhost:8501

---

## ☁️ 部署到 Streamlit Cloud

### 步驟

#### 1. 準備 GitHub Repository

```bash
# 初始化 Git（如果尚未初始化）
git init

# 新增所有檔案
git add .

# 提交
git commit -m "Initial commit: EasyAI MVP"

# 連結遠端倉庫
git remote add origin https://github.com/your-username/easyai.git

# 推送
git push -u origin main
```

#### 2. 登入 Streamlit Cloud

1. 前往 https://share.streamlit.io
2. 使用 GitHub 帳號登入
3. 授權 Streamlit 訪問您的 GitHub

#### 3. 建立新應用

1. 點擊 "New app" 按鈕
2. 選擇您的 GitHub repository
3. 設定以下參數：
   - **Branch**: main
   - **Main file path**: app.py
   - **App URL**: 自訂或使用預設

#### 4. 配置 Secrets

1. 在應用設定頁面找到 "Secrets" 區域
2. 貼上以下內容：

```toml
OPENAI_API_KEY = "sk-your-actual-api-key"
```

3. 點擊 "Save"

#### 5. 部署

點擊 "Deploy" 按鈕，等待部署完成（約 2-5 分鐘）

#### 6. 訪問應用

部署完成後，您會獲得一個公開 URL，例如：
```
https://your-app-name.streamlit.app
```

---

## 🐳 Docker 部署（進階）

### Dockerfile

建立 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 建置與運行

```bash
# 建置映像
docker build -t easyai .

# 運行容器
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="sk-your-actual-api-key" \
  easyai
```

訪問 http://localhost:8501

---

## 🔒 安全性建議

### API Key 保護

1. **絕對不要**將 API Key 硬編碼在代碼中
2. **絕對不要**將 `.streamlit/secrets.toml` 提交到 Git
3. 使用 `.gitignore` 排除敏感檔案：

```gitignore
.streamlit/secrets.toml
.env
corpus_data.csv
```

### 環境隔離

- 本地開發使用虛擬環境
- 生產環境使用容器化部署
- 定期更新依賴套件

---

## 📊 監控與維護

### 語料庫管理

定期備份 `corpus_data.csv`：

```bash
# 備份
cp corpus_data.csv corpus_data_backup_$(date +%Y%m%d).csv

# 壓縮
tar -czf corpus_backup.tar.gz corpus_data.csv
```

### 日誌檢查

Streamlit Cloud 提供應用日誌：

1. 進入應用設定頁面
2. 點擊 "Logs" 查看運行日誌
3. 監控錯誤與異常

### 效能優化

- 使用 `@st.cache_resource` 快取 Logger 實例
- 定期清理過大的語料庫檔案
- 監控 API 調用次數與費用

---

## 🆘 常見問題

### Q1: 無法啟動應用

**檢查清單：**
- Python 版本是否為 3.11+
- 是否已安裝所有依賴
- 是否已啟動虛擬環境

### Q2: API Key 錯誤

**檢查清單：**
- API Key 是否有效
- 環境變數或 secrets.toml 是否正確設定
- API Key 是否有足夠的額度

### Q3: 語料庫無法寫入

**檢查清單：**
- 檔案權限是否正確
- 磁碟空間是否充足
- CSV 檔案是否被其他程式佔用

### Q4: 部署到 Streamlit Cloud 失敗

**檢查清單：**
- requirements.txt 是否完整
- Secrets 是否正確設定
- GitHub repository 是否為 public 或已授權

---

## 📞 技術支援

如遇到問題，請檢查：

1. **GitHub Issues**: 查看已知問題與解決方案
2. **Streamlit 文檔**: https://docs.streamlit.io
3. **OpenAI 文檔**: https://platform.openai.com/docs

---

**祝您部署順利！** 🚀
