"""
八字引擎核心模組
負責農曆轉換、干支計算與 OpenAI 命理解析
"""

from datetime import datetime
from lunar_python import Lunar, Solar
from openai import OpenAI
import os


def get_fortune(birth_date: datetime.date, birth_time: datetime.time) -> dict:
    """
    核心函數：計算八字並生成 AI 運勢解析
    
    Args:
        birth_date: 出生日期 (datetime.date 對象)
        birth_time: 出生時間 (datetime.time 對象)
        
    Returns:
        dict: 包含以下欄位
            - birth_datetime: 完整出生時間字串
            - lunar_date: 農曆日期
            - year_pillar: 年柱
            - month_pillar: 月柱
            - day_pillar: 日柱
            - time_pillar: 時柱
            - day_master: 日主天干
            - day_master_element: 日主五行
            - bazi_full: 完整八字字串
            - ai_fortune: AI 生成的運勢解析
            - success: 是否成功
            - error: 錯誤訊息（若有）
    """
    
    try:
        # 組合完整日期時間
        birth_datetime = datetime.combine(birth_date, birth_time)
        
        # === 步驟 1: 農曆轉換與八字計算 ===
        solar = Solar.fromYmdHms(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            birth_datetime.hour,
            birth_datetime.minute,
            birth_datetime.second
        )
        
        lunar = solar.getLunar()
        
        # 獲取四柱干支
        year_gan = lunar.getYearGan()
        year_zhi = lunar.getYearZhi()
        month_gan = lunar.getMonthGan()
        month_zhi = lunar.getMonthZhi()
        day_gan = lunar.getDayGan()
        day_zhi = lunar.getDayZhi()
        time_gan = lunar.getTimeGan()
        time_zhi = lunar.getTimeZhi()
        
        # 組合四柱
        year_pillar = f"{year_gan}{year_zhi}"
        month_pillar = f"{month_gan}{month_zhi}"
        day_pillar = f"{day_gan}{day_zhi}"
        time_pillar = f"{time_gan}{time_zhi}"
        
        # 日主五行
        wuxing_map = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        day_master_element = wuxing_map.get(day_gan, "未知")
        
        # 農曆日期
        lunar_date = f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
        
        # 完整八字
        bazi_full = f"{year_pillar} {month_pillar} {day_pillar} {time_pillar}"
        
        # === 步驟 2: OpenAI 命理解析 ===
        ai_fortune = _generate_ai_fortune(
            birth_datetime=birth_datetime,
            lunar_date=lunar_date,
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            time_pillar=time_pillar,
            day_master=day_gan,
            day_master_element=day_master_element
        )
        
        # 返回結果
        return {
            "success": True,
            "birth_datetime": birth_datetime.strftime("%Y年%m月%d日 %H時%M分"),
            "lunar_date": lunar_date,
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "time_pillar": time_pillar,
            "day_master": day_gan,
            "day_master_element": day_master_element,
            "bazi_full": bazi_full,
            "ai_fortune": ai_fortune,
            "error": None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"計算失敗：{str(e)}",
            "birth_datetime": None,
            "lunar_date": None,
            "year_pillar": None,
            "month_pillar": None,
            "day_pillar": None,
            "time_pillar": None,
            "day_master": None,
            "day_master_element": None,
            "bazi_full": None,
            "ai_fortune": None
        }


def _generate_ai_fortune(
    birth_datetime: datetime,
    lunar_date: str,
    year_pillar: str,
    month_pillar: str,
    day_pillar: str,
    time_pillar: str,
    day_master: str,
    day_master_element: str
) -> str:
    """
    內部函數：使用 OpenAI 生成命理解析
    
    Args:
        各項八字資訊
        
    Returns:
        str: AI 生成的運勢文案
    """
    
    # 構造 Prompt
    bazi_info = f"""
八字四柱：
- 年柱：{year_pillar}
- 月柱：{month_pillar}
- 日柱：{day_pillar}
- 時柱：{time_pillar}

日主：{day_master}（{day_master_element}行）
出生日期：{birth_datetime.strftime("%Y年%m月%d日 %H時")}（農曆 {lunar_date}）
"""
    
    # 傳統命理風格 System Prompt
    system_prompt = """你是一位精通傳統命理與中醫理論的專業命理師。論命風格直接明確,不講模稜兩可的話。重視取象論命,結合中醫經絡與五行生剋理論。結尾必須給出一個具體的改運建議(如方位、穿著、飲食等物理調整方式)。請根據用戶八字生成 300 字內的流日運勢分析。"""
    
    user_prompt = f"{bazi_info}\n\n請為此命盤進行流日運勢分析。"
    
    try:
        # 初始化 OpenAI 客戶端（明確指定 base_url 與 api_key）
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL")
        )
        
        # 呼叫 GPT
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # 使用預設配置的模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=600
        )
        
        fortune_text = response.choices[0].message.content.strip()
        return fortune_text
        
    except Exception as e:
        return f"⚠️ AI 解析失敗：{str(e)}\n\n請檢查 API Key 設定或網路連線。"


# === 測試代碼 ===
if __name__ == "__main__":
    # 測試範例
    from datetime import date, time
    
    test_date = date(1990, 1, 1)
    test_time = time(12, 0)
    
    result = get_fortune(test_date, test_time)
    
    if result["success"]:
        print("✅ 八字計算成功")
        print(f"出生時間: {result['birth_datetime']}")
        print(f"農曆: {result['lunar_date']}")
        print(f"八字: {result['bazi_full']}")
        print(f"日主: {result['day_master']} ({result['day_master_element']}行)")
        print(f"\nAI 解析:\n{result['ai_fortune']}")
    else:
        print(f"❌ 錯誤: {result['error']}")
