"""
數據收割模組
負責將用戶輸入與 AI 輸出存入 CSV，累積訓練語料庫
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path


class FortuneLogger:
    """運勢數據記錄器"""
    
    def __init__(self, csv_path: str = "corpus_data.csv"):
        """
        初始化記錄器
        
        Args:
            csv_path: CSV 檔案路徑（預設為 corpus_data.csv）
        """
        self.csv_path = csv_path
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """確保 CSV 檔案存在，若不存在則建立"""
        if not os.path.exists(self.csv_path):
            # 建立空白 DataFrame 並寫入檔案
            df = pd.DataFrame(columns=[
                "Timestamp",
                "Birth_DateTime",
                "Lunar_Date",
                "Bazi_Chart",
                "Day_Master",
                "Day_Master_Element",
                "AI_Output"
            ])
            df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            print(f"✅ 已建立新的語料庫檔案: {self.csv_path}")
    
    def log_fortune(self, fortune_data: dict) -> bool:
        """
        記錄一筆運勢數據
        
        Args:
            fortune_data: 從 bazi_engine.get_fortune() 返回的結果字典
            
        Returns:
            bool: 是否成功記錄
        """
        try:
            # 檢查是否成功生成
            if not fortune_data.get("success", False):
                print(f"⚠️ 跳過記錄：運勢生成失敗")
                return False
            
            # 準備記錄資料
            record = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Birth_DateTime": fortune_data.get("birth_datetime", ""),
                "Lunar_Date": fortune_data.get("lunar_date", ""),
                "Bazi_Chart": fortune_data.get("bazi_full", ""),
                "Day_Master": fortune_data.get("day_master", ""),
                "Day_Master_Element": fortune_data.get("day_master_element", ""),
                "AI_Output": fortune_data.get("ai_fortune", "")
            }
            
            # 讀取現有數據
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            # 新增記錄
            df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
            
            # 寫回檔案
            df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            
            print(f"✅ 已記錄數據到 {self.csv_path} (共 {len(df)} 筆)")
            return True
            
        except Exception as e:
            print(f"❌ 記錄失敗：{str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """
        獲取語料庫統計資訊
        
        Returns:
            dict: 包含總筆數、最新記錄時間等資訊
        """
        try:
            if not os.path.exists(self.csv_path):
                return {
                    "total_records": 0,
                    "latest_timestamp": None,
                    "file_size_kb": 0
                }
            
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            file_size = os.path.getsize(self.csv_path) / 1024  # KB
            
            return {
                "total_records": len(df),
                "latest_timestamp": df["Timestamp"].iloc[-1] if len(df) > 0 else None,
                "file_size_kb": round(file_size, 2)
            }
            
        except Exception as e:
            print(f"❌ 獲取統計失敗：{str(e)}")
            return {
                "total_records": 0,
                "latest_timestamp": None,
                "file_size_kb": 0
            }
    
    def export_to_text(self, output_path: str = "corpus_text.txt") -> bool:
        """
        將語料庫匯出為純文字格式（方便訓練）
        
        Args:
            output_path: 輸出文字檔路徑
            
        Returns:
            bool: 是否成功匯出
        """
        try:
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for _, row in df.iterrows():
                    f.write(f"=== 八字: {row['Bazi_Chart']} ===\n")
                    f.write(f"日主: {row['Day_Master']} ({row['Day_Master_Element']}行)\n")
                    f.write(f"出生: {row['Birth_DateTime']}\n")
                    f.write(f"農曆: {row['Lunar_Date']}\n")
                    f.write(f"\n【運勢解析】\n{row['AI_Output']}\n")
                    f.write("\n" + "="*50 + "\n\n")
            
            print(f"✅ 已匯出純文字語料到 {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 匯出失敗：{str(e)}")
            return False


# === 測試代碼 ===
if __name__ == "__main__":
    # 測試記錄器
    logger = FortuneLogger("test_corpus.csv")
    
    # 模擬一筆數據
    test_data = {
        "success": True,
        "birth_datetime": "1990年01月01日 12時00分",
        "lunar_date": "一九八九年臘月初五",
        "bazi_full": "己巳 丙子 丙寅 甲午",
        "day_master": "丙",
        "day_master_element": "火",
        "ai_fortune": "此命日主丙火，生於子月，水旺之時。年柱己巳，巳火為根，月柱丙子，水火相濟。時柱甲午，木火通明。整體格局偏弱，需借木火之力。\n\n流日運勢：今日宜向南方行走，穿著紅色或紫色衣物，以助火勢。飲食宜溫熱，避免生冷。"
    }
    
    # 記錄數據
    logger.log_fortune(test_data)
    
    # 獲取統計
    stats = logger.get_stats()
    print(f"\n語料庫統計: {stats}")
    
    # 匯出文字
    logger.export_to_text("test_corpus.txt")
