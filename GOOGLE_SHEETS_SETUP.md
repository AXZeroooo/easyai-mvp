# Google Sheets 數據資產鎖定 - 設定指引

**目標**：將用戶查詢與 AI 回應自動寫入 Google Sheets，建立雲端數據資產。

---

## 📋 設定步驟

### 步驟 1：建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點擊右上角「選取專案」→「新增專案」
3. 專案名稱：`eeasy-ai-metaphysics`（或您想要的名稱）
4. 點擊「建立」

---

### 步驟 2：啟用 Google Sheets API

1. 在 Google Cloud Console 中，選擇剛建立的專案
2. 前往「API 和服務」→「程式庫」
3. 搜尋「Google Sheets API」
4. 點擊進入，點擊「啟用」
5. 同樣方式啟用「Google Drive API」

---

### 步驟 3：建立 Service Account

1. 前往「API 和服務」→「憑證」
2. 點擊「建立憑證」→「服務帳戶」
3. 填寫資訊：
   - **服務帳戶名稱**：`eeasy-sheets-logger`
   - **服務帳戶 ID**：自動生成
   - **說明**：eeasy.ai 數據資產記錄器
4. 點擊「建立並繼續」
5. 角色選擇：
   - 選擇「基本」→「編輯者」（或更嚴格的「Google Sheets API 使用者」）
6. 點擊「繼續」→「完成」

---

### 步驟 4：建立 Service Account Key

1. 在「憑證」頁面，找到剛建立的服務帳戶
2. 點擊服務帳戶名稱進入詳情頁
3. 切換到「金鑰」分頁
4. 點擊「新增金鑰」→「建立新的金鑰」
5. 金鑰類型選擇「JSON」
6. 點擊「建立」
7. JSON 檔案會自動下載到您的電腦

**重要**：妥善保管此 JSON 檔案，不要洩露給他人！

---

### 步驟 5：建立 Google Sheet

1. 前往 [Google Sheets](https://sheets.google.com/)
2. 點擊「空白」建立新試算表
3. 試算表名稱：`eeasy.ai - Metaphysics Corpus`（或您想要的名稱）
4. 複製試算表 URL（例如：`https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit`）
5. 點擊右上角「共用」按鈕
6. 在「新增使用者和群組」欄位中，貼上 Service Account 的電子郵件地址
   - 格式：`eeasy-sheets-logger@eeasy-ai-metaphysics.iam.gserviceaccount.com`
   - 可在 JSON 檔案中的 `client_email` 欄位找到
7. 權限選擇「編輯者」
8. **取消勾選**「通知使用者」
9. 點擊「共用」

---

### 步驟 6：設定環境變數

#### 方式 A：使用 JSON 檔案（本地開發）

```bash
# .env 檔案
GOOGLE_SHEETS_CREDENTIALS=/path/to/your-service-account-key.json
GOOGLE_SHEETS_URL=https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit
```

#### 方式 B：使用 JSON 字串（Streamlit Cloud 部署）

1. 開啟下載的 JSON 檔案
2. 複製整個 JSON 內容（包含大括號）
3. 在 Streamlit Cloud 的 Secrets 設定中加入：

```toml
# .streamlit/secrets.toml
GOOGLE_SHEETS_CREDENTIALS = '''
{
  "type": "service_account",
  "project_id": "eeasy-ai-metaphysics",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "eeasy-sheets-logger@eeasy-ai-metaphysics.iam.gserviceaccount.com",
  "client_id": "123456789...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
'''

GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit"
```

**注意**：
- JSON 內容使用三個單引號 `'''` 包裹
- 不要修改 JSON 內容，直接複製貼上
- `private_key` 欄位包含換行符 `\n`，保持原樣

---

## ✅ 測試連接

### 本地測試

```bash
cd /home/ubuntu/easyai
source venv/bin/activate
python3.11 gsheets_logger.py
```

**預期輸出**：

```
=== Google Sheets Logger 測試 ===

✅ Google Sheets 連接成功

📊 統計資訊:
   總筆數: 0
   最新記錄: None
   狀態: 已連接

✅ 測試數據寫入成功
```

### Streamlit 應用測試

1. 啟動應用：`streamlit run app.py`
2. 輸入任意出生日期時間
3. 點擊「🧠 AI 顧問請分析」
4. 查看側邊欄「📊 數據資產統計」
5. 前往 Google Sheets 確認數據已寫入

---

## 📊 Google Sheet 結構

系統會自動建立以下欄位：

| 欄位 | 說明 | 範例 |
|------|------|------|
| Timestamp | 記錄時間戳 | 2025-11-19 07:30:45 |
| Birth_DateTime | 用戶出生時間 | 1990-01-01 12:00 |
| Lunar_Date | 農曆日期 | 一九八九年腊月初五 |
| Bazi_Chart | 完整八字 | 己巳 丙子 丙寅 甲午 |
| Day_Master | 日主天干 | 丙 |
| Day_Master_Element | 日主五行 | 火 |
| AI_Response | GPT 生成的完整運勢文案 | 1. **本質分析**... |

---

## 🔧 常見問題

### Q1: 連接失敗，顯示 "401 Unauthorized"

**原因**：Service Account 沒有權限存取 Google Sheet

**解決方案**：
1. 確認已將 Service Account 的電子郵件加入 Google Sheet 的共用清單
2. 權限設定為「編輯者」
3. 重新測試連接

### Q2: 連接失敗，顯示 "API not enabled"

**原因**：Google Sheets API 或 Google Drive API 未啟用

**解決方案**：
1. 前往 Google Cloud Console
2. 確認「Google Sheets API」和「Google Drive API」都已啟用
3. 等待 1-2 分鐘讓 API 生效
4. 重新測試連接

### Q3: JSON 格式錯誤

**原因**：JSON 內容複製不完整或格式錯誤

**解決方案**：
1. 重新下載 Service Account Key JSON 檔案
2. 使用文字編輯器開啟，確認 JSON 格式正確
3. 完整複製整個 JSON 內容（包含大括號）
4. 在 Streamlit Secrets 中使用三個單引號 `'''` 包裹

### Q4: 本地可以連接，但 Streamlit Cloud 失敗

**原因**：Streamlit Cloud 的 Secrets 設定錯誤

**解決方案**：
1. 檢查 Streamlit Cloud 的 Secrets 設定
2. 確認 `GOOGLE_SHEETS_CREDENTIALS` 是完整的 JSON 字串
3. 確認 `GOOGLE_SHEETS_URL` 是正確的 Google Sheet URL
4. 重新部署應用

---

## 🎯 數據資產管理

### 定期備份

雖然數據已在 Google Sheets 中，建議仍定期匯出備份：

```python
from gsheets_logger import GoogleSheetsLogger

logger = GoogleSheetsLogger()
logger.export_to_csv("backup_20251119.csv")
```

### 數據分析

累積足夠數據後，可使用 Google Sheets 的內建功能進行分析：

- **樞紐分析表**：分析不同日主的分佈
- **圖表**：視覺化數據趨勢
- **篩選器**：快速查找特定八字

### 數據匯出

可隨時匯出為 CSV 或 Excel 格式，用於：

- 訓練專屬 AI 模型
- 數據分析與研究
- 備份與歸檔

---

## 🔒 安全提醒

1. **不要將 Service Account Key JSON 檔案提交到 GitHub**
2. **不要公開分享 Google Sheet 連結**
3. **定期檢查 Service Account 的權限設定**
4. **如果 Key 洩露，立即在 Google Cloud Console 中刪除並重新建立**

---

## 📚 相關資源

- [Google Sheets API 文檔](https://developers.google.com/sheets/api)
- [gspread 套件文檔](https://docs.gspread.org/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Streamlit Secrets 管理](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

**設定版本**：v1.0  
**最後更新**：2025-11-19

完成設定後，您的 eeasy.ai MVP 將自動將所有查詢記錄到 Google Sheets，建立寶貴的數據資產！🎉
