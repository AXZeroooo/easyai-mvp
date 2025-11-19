# Streamlit Cloud 部署指南

**專案**：易AI - 八字命理與 AI 運勢分析 MVP  
**GitHub Repository**：https://github.com/AXZeroooo/easyai-mvp

---

## 📋 部署前檢查清單

- [x] GitHub Repository 已建立
- [x] 代碼已推送到 GitHub
- [x] requirements.txt 已準備
- [x] .gitignore 已設定
- [x] CSV 下載功能已實作
- [ ] Streamlit Cloud 部署（需手動操作）

---

## 🚀 部署步驟

### 步驟 1：登入 Streamlit Cloud

1. 前往 [Streamlit Community Cloud](https://share.streamlit.io)
2. 使用 GitHub 帳號登入

### 步驟 2：建立新應用

1. 點擊右上角的 **"New app"** 按鈕
2. 填寫以下資訊：

| 欄位 | 值 |
|------|-----|
| **Repository** | `AXZeroooo/easyai-mvp` |
| **Branch** | `master` |
| **Main file path** | `app.py` |
| **App URL (optional)** | `easyai-bazi` 或您想要的名稱 |

3. 點擊 **"Advanced settings"**（可選）
   - **Python version**: 3.11

### 步驟 3：設定 Secrets

在部署設定頁面，找到 **"Secrets"** 區域，加入以下內容：

```toml
# OpenAI API 配置
OPENAI_API_KEY = "sk-proj-your-actual-api-key-here"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

**重要提醒**：
- 請將 `sk-proj-your-actual-api-key-here` 替換為您的真實 OpenAI API Key
- 不要將 API Key 提交到 GitHub
- Secrets 設定僅在 Streamlit Cloud 後台可見

### 步驟 4：部署應用

1. 確認所有設定正確
2. 點擊 **"Deploy!"** 按鈕
3. 等待部署完成（約 2-5 分鐘）

---

## 🌐 部署後的 URL

部署成功後，您將獲得一個公開 URL，格式如下：

```
https://easyai-bazi.streamlit.app
```

或

```
https://[your-app-name]-[random-string].streamlit.app
```

---

## ✅ 部署驗證

部署完成後，請進行以下測試：

### 1. 基本功能測試

- [ ] 應用可正常開啟
- [ ] 日期時間輸入正常
- [ ] 點擊「大師請指點」按鈕
- [ ] 八字排盤顯示正常
- [ ] AI 運勢解析正常生成

### 2. CSV 下載測試

- [ ] 側邊欄顯示「💾 語料庫備份」區域
- [ ] 點擊「📥 下載歷史語料 CSV」按鈕
- [ ] CSV 檔案成功下載到本地
- [ ] CSV 內容包含完整的八字與 AI 解析

### 3. 行動裝置測試

- [ ] 使用手機瀏覽器開啟 URL
- [ ] 介面在小螢幕上正常顯示
- [ ] 所有功能可正常操作

---

## 📊 語料庫備份流程

### 自動記錄

每次用戶查詢運勢時，系統會自動將以下資料寫入 `corpus_data.csv`：

- 時間戳
- 出生時間
- 農曆日期
- 八字四柱
- 日主與五行
- AI 生成的運勢文案

### 手動備份

**方式 1：從前端下載**

1. 開啟 Streamlit 應用
2. 在側邊欄找到「💾 語料庫備份」
3. 點擊「📥 下載歷史語料 CSV」
4. 檔案會自動下載，檔名格式：`easyai_corpus_YYYYMMDD_HHMMSS.csv`

**方式 2：從 GitHub 查看（僅限本地開發）**

```bash
# 本地開發環境
cat corpus_data.csv
```

**注意**：Streamlit Cloud 的檔案系統會定期重置，因此：
- ✅ 建議每日從前端下載備份
- ❌ 不要依賴雲端環境的 CSV 檔案

---

## 🔧 常見問題

### Q1: 部署後顯示 "ModuleNotFoundError"

**原因**：`requirements.txt` 缺少必要的套件

**解決方案**：
1. 檢查 `requirements.txt` 是否包含所有依賴
2. 推送更新到 GitHub
3. Streamlit Cloud 會自動重新部署

### Q2: API 調用失敗（401 錯誤）

**原因**：OpenAI API Key 未正確設定

**解決方案**：
1. 前往 Streamlit Cloud 應用設定
2. 檢查 Secrets 中的 `OPENAI_API_KEY`
3. 確認格式正確：`OPENAI_API_KEY = "sk-proj-..."`
4. 儲存後重啟應用

### Q3: CSV 下載按鈕無法使用

**原因**：尚無語料記錄

**解決方案**：
1. 先進行一次運勢查詢
2. 系統會自動建立 `corpus_data.csv`
3. 下載按鈕即可使用

### Q4: 應用運行緩慢

**原因**：Streamlit Cloud 免費版資源有限

**解決方案**：
- 免費版已足夠 MVP 使用
- 如需更高效能，可考慮升級到付費方案
- 或部署到其他平台（Heroku, Railway, etc.）

---

## 📈 下一步建議

### 立即行動

1. **測試應用** - 用手機開啟 URL，輸入多組八字測試
2. **累積語料** - 目標：首批 50 筆語料
3. **備份數據** - 每日下載 CSV 備份

### 數據挖礦

- 輸入您自己、家人、朋友的八字
- 測試不同出生時間的解析品質
- 觀察 AI 生成的改運建議是否合理

### AEO 實戰

- 挑選 3-5 篇最佳 AI 解析
- 發布到社群媒體（Threads/FB）
- 標題帶上「易AI × 繁中八字實測」
- 測試 AI 搜尋引擎（Perplexity/SearchGPT）能否抓到

---

## 🔗 相關連結

- **GitHub Repository**: https://github.com/AXZeroooo/easyai-mvp
- **Streamlit Cloud**: https://share.streamlit.io
- **OpenAI Platform**: https://platform.openai.com
- **專案文檔**: README_DEPLOY.md

---

## 📞 支援

如遇到部署問題，請檢查：

1. **GitHub Issues**: 查看是否有類似問題
2. **Streamlit 文檔**: https://docs.streamlit.io
3. **OpenAI 文檔**: https://platform.openai.com/docs

---

**部署版本**：v1.1.1  
**最後更新**：2025-11-19 04:00 GMT+8

祝您部署順利！🚀
