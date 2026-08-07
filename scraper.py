import json
import urllib.request
import urllib.error
import re
from datetime import datetime

# ==========================================
# BOT 1: West Bengal Official Bot (WBPSC / WBPRB / Group D)
# ==========================================
def bot_west_bengal():
    exams = []
    print("Running WB Bot...")
    
    # 1. West Bengal Group D Recruitment Board (আপনার স্পেশাল টার্গেট)
    exams.append({
        "exam_name": "West Bengal Group D Examination",
        "status": "অফিসিয়াল আপডেটের অপেক্ষায় ⏳",
        "form_fillup_start": "শীঘ্রই ঘোষণা করা হবে",
        "form_fillup_end": "অফিসিয়াল ওয়েবসাইটে নজর রাখুন"
    })
    
    # 2. WBPSC Official Website Check
    url_wbpsc = "https://psc.wb.gov.in/"
    try:
        # সরকারি ওয়েবসাইটে মানুষের মতো হিট করার চেষ্টা
        req = urllib.request.Request(url_wbpsc, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        # সফল হলে এই ডেটা দেখাবে
        exams.append({
            "exam_name": "WBPSC (Public Service Commission)",
            "status": "Site Active 🟢",
            "form_fillup_start": "psc.wb.gov.in চেক করুন",
            "form_fillup_end": "psc.wb.gov.in চেক করুন"
        })
    except urllib.error.URLError:
        # সরকারি সাইট ব্লক করলে বা সার্ভার ডাউন থাকলে
        exams.append({
            "exam_name": "WBPSC Official Website",
            "status": "সার্ভার ব্যস্ত / Protected 🔴",
            "form_fillup_start": "-",
            "form_fillup_end": "-"
        })
        
    return exams

# ==========================================
# BOT 2: Central Govt Official Bot (SSC / UPSC / Railway)
# ==========================================
def bot_central_govt():
    exams = []
    print("Running Central Govt Bot...")
    
    # 1. SSC (Staff Selection Commission)
    url_ssc = "https://ssc.gov.in/"
    try:
        req = urllib.request.Request(url_ssc, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        exams.append({
            "exam_name": "SSC (Staff Selection Commission)",
            "status": "Site Active 🟢",
            "form_fillup_start": "ssc.gov.in চেক করুন",
            "form_fillup_end": "ssc.gov.in চেক করুন"
        })
    except:
        exams.append({
            "exam_name": "SSC (Staff Selection Commission)",
            "status": "সার্ভার ব্যস্ত 🔴",
            "form_fillup_start": "-",
            "form_fillup_end": "-"
        })

    # 2. Indian Railways (RRB)
    exams.append({
        "exam_name": "RRB (Railway Recruitment Board)",
        "status": "নতুন আপডেটের খোঁজ চলছে 🚂",
        "form_fillup_start": "indianrailways.gov.in",
        "form_fillup_end": "indianrailways.gov.in"
    })
    
    return exams

# ==========================================
# MASTER BOT (কমান্ডার - যে সবাইকে একসাথে চালাবে)
# ==========================================
def run_master_bot():
    all_exams = []
    
    # একে একে সব বটকে কাজে লাগানো হচ্ছে
    all_exams.extend(bot_west_bengal())
    all_exams.extend(bot_central_govt())
    
    # সব বটের ডেটা একসাথে JSON ফাইলে সেভ করা
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
        
    print("Master Bot সফলভাবে সমস্ত রাজ্যের ডেটা সেভ করেছে!")

# স্ক্রিপ্ট রান করার নির্দেশ
if __name__ == "__main__":
    run_master_bot()
