import json
import re
import urllib.request
import urllib.parse
import ssl
from deep_translator import GoogleTranslator

# SSL কনফিগারেশন
ssl_context = ssl._create_unverified_context()
API_KEY = "0bacbfa123fb6b3ff27bd417951af2fe"

# আপনার আসল সাইট লিস্ট
EXAM_SITES = [
    {
        "id": "wbprb",
        "exam_name": "West Bengal Group D / WBPRB",
        "url": "https://news.google.com/rss/search?q=WBPRB+OR+West+Bengal+Police+recruitment+notice&hl=bn&gl=IN&ceid=IN:bn",
        "default_url": "https://wbpolice.gov.in/",
        "method": "google_news" 
    },
    {
        "id": "wbpsc",
        "exam_name": "WBPSC Official Website",
        "url": "https://psc.wb.gov.in/",
        "keywords": ["Advertisement", "Notice", "Result"],
        "default_url": "https://psc.wb.gov.in/",
        "method": "scraperapi"
    },
    {
        "id": "ssc",
        "exam_name": "SSC (Staff Selection Commission)",
        "url": "https://ssc.gov.in/",
        "keywords": ["Notice", "Examination", "Result", "Apply"],
        "default_url": "https://ssc.gov.in/",
        "method": "basic"
    }
]

def translate_text(text, target='bn'):
    """অনুবাদ করার ফাংশন"""
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return text

def scan_website(site):
    print(f"Scanning {site['exam_name']}...")
    
    # প্রাথমিক লজিক (আপনার পুরানো কোড থেকে)
    # এখানে আমরা ডেটা তুলে সেটিকে অনুবাদ করছি
    try:
        # (এখানে আপনার আগের scan_website লজিকগুলো আছে...)
        # উদাহরণ হিসেবে একটি লাইন নিচে দিচ্ছি:
        exam_name_bn = translate_text(site['exam_name'], 'bn')
        
        return {
            "exam_name": {"bn": exam_name_bn, "en": site['exam_name']},
            "status": "New Update 🔔", # চাইলে এটিকেও অনুবাদ করতে পারেন
            "form_fillup_start": "আপডেট চেক করুন",
            "form_fillup_end": site['default_url']
        }
    except Exception as e:
        return {"error": str(e)}

def run_master_bot():
    all_exams = []
    for site in EXAM_SITES:
        all_exams.append(scan_website(site))
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
    print("--- Data Updated Successfully ---")

if __name__ == "__main__":
    run_master_bot()
