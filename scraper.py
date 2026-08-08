import json
import re
import urllib.request
import urllib.parse
import ssl
from deep_translator import GoogleTranslator

# SSL কনফিগারেশন
ssl_context = ssl._create_unverified_context()

# আপনার আসল ওয়েবসাইট এবং লিংকগুলোর তালিকা
EXAM_SITES = [
    {
        "id": "wbprb",
        "exam_name": "West Bengal Police Recruitment",
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

# ভাষা তালিকা
TARGET_LANGUAGES = ['bn', 'en', 'hi', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa']

def translate_to_all(text):
    """টেক্সটকে সব ভাষায় অনুবাদ করার ফাংশন"""
    translations = {}
    for lang in TARGET_LANGUAGES:
        try:
            translations[lang] = GoogleTranslator(source='auto', target=lang).translate(text)
        except:
            translations[lang] = text
    return translations

def scan_website(site):
    print(f"Scanning {site['exam_name']}...")
    
    # প্রাথমিক ফলাফল (মাল্টি-ল্যাঙ্গুয়েজে)
    result = {
        "exam_name": translate_to_all(site["exam_name"]),
        "status": translate_to_all("সার্ভার ব্যস্ত"),
        "form_fillup_start": "-",
        "form_fillup_end": "বিস্তারিত দেখুন"
    }
    
    try:
        # এখানে আপনার আগের লজিক কাজ করবে
        # ... (আপনার আগের scan_website লজিক এখানে বসবে)
        # জাস্ট প্রতিটি টেক্সট ফিল্ডকে translate_to_all() দিয়ে মুড়িয়ে দেবেন
        result["status"] = translate_to_all("নতুন নোটিশ উপলব্ধ 🔔")
        result["form_fillup_start"] = translate_to_all("আজকের আপডেট দেখুন")
    except Exception as e:
        print(f"Error: {e}")
            
    return result

def run_master_bot():
    all_exams = []
    for site in EXAM_SITES:
        all_exams.append(scan_website(site))
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
    print("--- Data Updated Successfully ---")

if __name__ == "__main__":
    run_master_bot()
