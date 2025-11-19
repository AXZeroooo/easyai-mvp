"""
Google Sheets Logger for eeasy.ai
數據資產鎖定模組 - 將用戶查詢與 AI 回應寫入 Google Sheets
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os


class GoogleSheetsLogger:
    """Google Sheets 數據記錄器"""
    
    def __init__(self, credentials_json=None, sheet_url=None):
        """
        初始化 Google Sheets Logger
        
        Args:
            credentials_json: Google Service Account JSON 字串或檔案路徑
            sheet_url: Google Sheets URL
        """
        self.credentials_json = credentials_json or os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
        self.sheet_url = sheet_url or os.environ.get("GOOGLE_SHEETS_URL")
        self.client = None
        self.worksheet = None
        
    def connect(self):
        """連接到 Google Sheets"""
        try:
            # 定義權限範圍
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # 解析憑證
            if isinstance(self.credentials_json, str):
                if self.credentials_json.startswith('{'):
                    # JSON 字串
                    creds_dict = json.loads(self.credentials_json)
                else:
                    # 檔案路徑
                    with open(self.credentials_json, 'r') as f:
                        creds_dict = json.load(f)
            else:
                raise ValueError("credentials_json 必須是 JSON 字串或檔案路徑")
            
            # 建立憑證
            credentials = Credentials.from_service_account_info(
                creds_dict,
                scopes=scopes
            )
            
            # 建立 gspread 客戶端
            self.client = gspread.authorize(credentials)
            
            # 開啟 Google Sheet
            if self.sheet_url:
                self.worksheet = self.client.open_by_url(self.sheet_url).sheet1
            else:
                raise ValueError("未設定 GOOGLE_SHEETS_URL")
            
            # 檢查是否需要初始化標題列
            if not self.worksheet.row_values(1):
                self._initialize_headers()
            
            return True
            
        except Exception as e:
            print(f"❌ Google Sheets 連接失敗: {e}")
            return False
    
    def _initialize_headers(self):
        """初始化 Google Sheet 標題列"""
        headers = [
            "Timestamp",
            "Birth_DateTime",
            "Lunar_Date",
            "Bazi_Chart",
            "Day_Master",
            "Day_Master_Element",
            "AI_Response"
        ]
        self.worksheet.append_row(headers)
    
    def log_fortune(self, fortune_data):
        """
        記錄運勢數據到 Google Sheets
        
        Args:
            fortune_data: 包含八字與 AI 解析的字典
        
        Returns:
            bool: 是否成功記錄
        """
        try:
            # 確保已連接
            if not self.worksheet:
                if not self.connect():
                    return False
            
            # 準備數據行
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                fortune_data.get("birth_datetime", ""),
                fortune_data.get("lunar_date", ""),
                fortune_data.get("bazi_full", ""),
                fortune_data.get("day_master", ""),
                fortune_data.get("day_master_element", ""),
                fortune_data.get("ai_fortune", "")
            ]
            
            # 寫入 Google Sheet
            self.worksheet.append_row(row)
            
            print(f"✅ 已記錄數據到 Google Sheets")
            return True
            
        except Exception as e:
            print(f"❌ Google Sheets 記錄失敗: {e}")
            return False
    
    def get_stats(self):
        """
        獲取語料庫統計資訊
        
        Returns:
            dict: 統計資訊
        """
        try:
            if not self.worksheet:
                if not self.connect():
                    return {
                        "total_records": 0,
                        "latest_timestamp": None,
                        "status": "未連接"
                    }
            
            # 獲取所有數據
            all_values = self.worksheet.get_all_values()
            
            # 扣除標題列
            total_records = len(all_values) - 1 if len(all_values) > 1 else 0
            
            # 獲取最新記錄時間
            latest_timestamp = None
            if total_records > 0:
                latest_timestamp = all_values[-1][0]  # 第一欄是時間戳
            
            return {
                "total_records": total_records,
                "latest_timestamp": latest_timestamp,
                "status": "已連接"
            }
            
        except Exception as e:
            print(f"❌ 獲取統計失敗: {e}")
            return {
                "total_records": 0,
                "latest_timestamp": None,
                "status": f"錯誤: {str(e)}"
            }
    
    def export_to_csv(self, output_path="corpus_export.csv"):
        """
        匯出 Google Sheet 數據為 CSV
        
        Args:
            output_path: 輸出檔案路徑
        
        Returns:
            bool: 是否成功匯出
        """
        try:
            if not self.worksheet:
                if not self.connect():
                    return False
            
            # 獲取所有數據
            all_values = self.worksheet.get_all_values()
            
            # 寫入 CSV
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(all_values)
            
            print(f"✅ 已匯出數據到 {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 匯出失敗: {e}")
            return False


# 測試代碼
if __name__ == "__main__":
    print("=== Google Sheets Logger 測試 ===\n")
    
    # 測試連接
    logger = GoogleSheetsLogger()
    
    if logger.connect():
        print("✅ Google Sheets 連接成功\n")
        
        # 測試統計
        stats = logger.get_stats()
        print(f"📊 統計資訊:")
        print(f"   總筆數: {stats['total_records']}")
        print(f"   最新記錄: {stats['latest_timestamp']}")
        print(f"   狀態: {stats['status']}\n")
        
        # 測試寫入
        test_data = {
            "birth_datetime": "1990-01-01 12:00",
            "lunar_date": "一九八九年腊月初五",
            "bazi_full": "己巳 丙子 丙寅 甲午",
            "day_master": "丙",
            "day_master_element": "火",
            "ai_fortune": "測試運勢解析內容..."
        }
        
        if logger.log_fortune(test_data):
            print("✅ 測試數據寫入成功")
        
    else:
        print("❌ Google Sheets 連接失敗")
        print("請確認：")
        print("1. GOOGLE_SHEETS_CREDENTIALS 環境變數已設定")
        print("2. GOOGLE_SHEETS_URL 環境變數已設定")
        print("3. Service Account 有權限存取該 Google Sheet")
