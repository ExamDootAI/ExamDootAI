import concurrent.futures
import json
import os
import time
import requests
from deep_translator import GoogleTranslator

# ডেটা ফাইল পাথ
DATA_FILE = "exams_data.json"

# টার্গেট ওয়েবসাইট বা API গুলোর তালিকা
TARGET_URLS = [
    "https://api.example.com/exams/wbprb",
    "https://api.example.com/exams/rrb",
    "https://api.example.com/exams/ssc",
]

# যে ভাষাগুলোতে অনুবাদ করতে চান (ভারতের প্রধান ভাষাগুলোসহ)
TARGET_LANGUAGES = ['bn', 'en', 'hi', 'ta', 'te', 'mr', 'gu', 'kn', 'ml', 'pa']

def translate_text(text, target_lang):
    """টেক্সটকে নির্দিষ্ট ভাষায় অনুবাদ করার ফাংশন"""
    try:
        if not text or not isinstance(text, str):
            return text
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translation Error for {target_lang}]: {e}")
        return text

def fetch_exam_data(url):
    """একক বট বা ওয়ার্কার যা নির্দিষ্ট লিংক থেকে ডেটা সংগ্রহ করবে এবং মাল্টি-ল্যাঙ্গুয়েজে রূপান্তর করবে"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"[Success] Data fetched from: {url}")
            raw_data = response.json()
            
            multilingual_exams = []
            items = raw_data if isinstance(raw_data, list) else [raw_data]
            
            for item in items:
                exam_name_raw = item.get("exam_name", "Exam Update")
                status_raw = item.get("status", "Active")
                
                exam_names = {}
                statuses = {}
                
                for lang in TARGET_LANGUAGES:
                    exam_names[lang] = translate_text(exam_name_raw, lang)
                    statuses[lang] = translate_text(status_raw, lang)
                
                multilingual_exams.append({
                    "exam_name": exam_names,
                    "status": statuses,
                    "form_fillup_start": item.get("form_fillup_start", "N/A"),
                    "form_fillup_end": item.get("form_fillup_end", "N/A")
                })
                
            return multilingual_exams
    except Exception as e:
        print(f"[Error] Failed to fetch {url}: {e}")
    return None

def auto_scale_scraper():
    """মাল্টি-থ্রেডিং ব্যবহার করে কাজের চাপ অনুযায়ী বট বা ওয়ার্কার সংখ্যা বৃদ্ধি করবে"""
    print("--- Auto-Scaling Multi-Language Scraper Started ---")
    scraped_results = []
    
    max_workers = min(5, len(TARGET_URLS))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_exam_data, url): url for url in TARGET_URLS}
        
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            if data:
                if isinstance(data, list):
                    scraped_results.extend(data)
                else:
                    scraped_results.append(data)
                
    update_json_storage(scraped_results)

def update_json_storage(new_data):
    """সংগৃহীত মাল্টি-ল্যাঙ্গুয়েজ ডেটা নিরাপদে লোকাল JSON ফাইলে সেভ করবে"""
    try:
        storage_data = {
            "timestamp": time.time(),
            "exams": new_data
        }
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(storage_data, f, ensure_ascii=False, indent=4)
            
        print("--- Multi-Language Exam Data Successfully Updated & Secured ---")
    except Exception as e:
        print(f"[Storage Error] {e}")

if __name__ == "__main__":
    auto_scale_scraper()
