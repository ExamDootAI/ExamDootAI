import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# ==========================================
# BOT 1: West Bengal Official Bot
# ==========================================
def bot_west_bengal():
    exams = []
    
    # West Bengal Group D 
    exams.append({
        "exam_name": "West Bengal Group D Examination",
        "status": "অফিসিয়াল আপডেটের অপেক্ষায় ⏳",
        "form_fillup_start": "শীঘ্রই ঘোষণা করা হবে",
        "form_fillup_end": "<a href='https://wbpolice.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>অফিসিয়াল ওয়েবসাইটে</a> নজর রাখুন"
    })
    
    # WBPSC Check
    url_wbpsc = "https://psc.wb.gov.in/"
    try:
        req = urllib.request.Request(url_wbpsc, headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=10)
        exams.append({
            "exam_name": "WBPSC Official Website",
            "status": "Site Active 🟢",
            "form_fillup_start": "<a href='https://psc.wb.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>psc.wb.gov.in</a> চেক করুন",
            "form_fillup_end": "-"
        })
    except:
        exams.append({
            "exam_name": "WBPSC Official Website",
            "status": "সার্ভার ব্যস্ত / Protected 🔴",
            "form_fillup_start": "-",
            "form_fillup_end": "-"
        })
    return exams

# ==========================================
# BOT 2: Central Govt (SSC Real Data)
# ==========================================
def bot_central_govt():
    exams = []
    print("Running Central Govt Bot (SSC Real Data)...")
    
    # SSC-এর আসল ওয়েবসাইট থেকে ডেটা নেওয়ার চেষ্টা
    url_ssc = "https://ssc.gov.in/"
    try:
        req = urllib.request.Request(url_ssc, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        response = urllib.request.urlopen(req, timeout=15)
        html_data = response.read().decode('utf-8')
        
        notices = re.findall(r'<a[^>]*>([^<]*(?:Notice|Examination|Result|Apply)[^<]*)</a>', html_data, re.IGNORECASE)
        
        clean_notices = []
        for n in notices:
            clean_text = n.strip().replace('\n', '').replace('\r', '')
            if clean_text and clean_text not in clean_notices:
                clean_notices.append(clean_text)
        
        if clean_notices:
            latest_notice = clean_notices[0][:60] + "..." if len(clean_notices[0]) > 60 else clean_notices[0]
            exams.append({
                "exam_name": "SSC (Staff Selection Commission)",
                "status": "New Update 🔔",
                "form_fillup_start": f"নোটিশ: {latest_notice}",
                "form_fillup_end": "বিস্তারিত জানতে <a href='https://ssc.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ssc.gov.in</a> দেখুন"
            })
        else:
            exams.append({
                "exam_name": "SSC (Staff Selection Commission)",
                "status": "Site Active 🟢",
                "form_fillup_start": "আজ নতুন কোনো নোটিশ নেই",
                "form_fillup_end": "<a href='https://ssc.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ssc.gov.in</a> চেক করুন"
            })
            
    except Exception as e:
        exams.append({
            "exam_name": "SSC (Staff Selection Commission)",
            "status": "সার্ভার ব্যস্ত 🔴",
            "form_fillup_start": "-",
            "form_fillup_end": "-"
        })

    # RRB 
    exams.append({
        "exam_name": "RRB (Railway Recruitment Board)",
        "status": "নতুন আপডেটের খোঁজ চলছে 🚂",
        "form_fillup_start": "<a href='https://indianrailways.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>indianrailways.gov.in</a>",
        "form_fillup_end": "<a href='https://indianrailways.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>indianrailways.gov.in</a>"
    })
    
    return exams

# ==========================================
# MASTER BOT
# ==========================================
def run_master_bot():
    all_exams = []
    all_exams.extend(bot_west_bengal())
    all_exams.extend(bot_central_govt())
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_master_bot()

