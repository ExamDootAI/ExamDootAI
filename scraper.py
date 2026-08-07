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
    
    # West Bengal Group D (আপনার স্পেশাল টার্গেট)
    exams.append({
        "exam_name": "West Bengal Group D Examination",
        "status": "অফিসিয়াল আপডেটের অপেক্ষায় ⏳",
        "form_fillup_start": "শীঘ্রই ঘোষণা করা হবে",
        "form_fillup_end": "অফিসিয়াল ওয়েবসাইটে নজর রাখুন"
    })
    
    # WBPSC Check
    url_wbpsc = "https://psc.wb.gov.in/"
    try:
        req = urllib.request.Request(url_wbpsc, headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=10)
        exams.append({
            "exam_name": "WBPSC Official Website",
            "status": "Site Active 🟢",
            "form_fillup_start": "psc.wb.gov.in চেক করুন",
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
        
        # Regex দিয়ে "Notice", "Examination", বা "Apply" লেখা লেটেস্ট আপডেট খোঁজা
        notices = re.findall(r'<a[^>]*>([^<]*(?:Notice|Examination|Result|Apply)[^<]*)</a>', html_data, re.IGNORECASE)
        
        # নোটিশগুলো পরিষ্কার করা (HTML ট্যাগ সরানো)
        clean_notices = []
        for n in notices:
            clean_text = n.strip().replace('\n', '').replace('\r', '')
            if clean_text and clean_text not in clean_notices:
                clean_notices.append(clean_text)
        
        if clean_notices:
            # লেটেস্ট নোটিশটি ওয়েবসাইটে দেখানোর জন্য
            latest_notice = clean_notices[0][:60] + "..." if len(clean_notices[0]) > 60 else clean_notices[0]
            exams.append({
                "exam_name": "SSC (Staff Selection Commission)",
                "status": "New Update 🔔",
                "form_fillup_start": f"নোটিশ: {latest_notice}",
                "form_fillup_end": "বিস্তারিত জানতে ssc.gov.in দেখুন"
            })
        else:
            exams.append({
                "exam_name": "SSC (Staff Selection Commission)",
                "status": "Site Active 🟢",
                "form_fillup_start": "আজ নতুন কোনো নোটিশ নেই",
                "form_fillup_end": "ssc.gov.in চেক করুন"
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
        "form_fillup_start": "indianrailways.gov.in",
        "form_fillup_end": "indianrailways.gov.in"
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
