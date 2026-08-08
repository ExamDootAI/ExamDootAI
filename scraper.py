import concurrent.futures
import json
import os
import time
import requests

# ডেটা ফাইল পাথ
DATA_FILE = "exams_data.json"

# টার্গেট ওয়েবসাইট বা API গুলোর তালিকা
TARGET_URLS = [
    "https://api.example.com/exams/wbprb",
    "https://api.example.com/exams/rrb",
    "https://api.example.com/exams/ssc",
]

def fetch_exam_data(url):
    """একক বট বা ওয়ার্কার যা নির্দিষ্ট লিংক থেকে ডেটা সংগ্রহ করবে"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"[Success] Data fetched from: {url}")
            return response.json()
    except Exception as e:
        print(f"[Error] Failed to fetch {url}: {e}")
    return None

def auto_scale_scraper():
    """মাল্টি-থ্রেডিং ব্যবহার করে কাজের চাপ অনুযায়ী বট বা ওয়ার্কার সংখ্যা বৃদ্ধি করবে"""
    print("--- Auto-Scaling Scraper Started ---")
    scraped_results = []
    
    # Workload অনুযায়ী একসাথে ম্যাক্সিমাম থ্রেড বা বট রান করানো হবে
    max_workers = min(5, len(TARGET_URLS))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_exam_data, url): url for url in TARGET_URLS}
        
        for future in concurrent.futures.as_completed(future_to_url):
            data = future.result()
            if data:
                scraped_results.append(data)
                
    update_json_storage(scraped_results)

def update_json_storage(new_data):
    """সংগৃহীত ডেটা নিরাপদে লোকাল JSON ফাইলে সেভ করবে"""
    try:
        existing_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        
        existing_data.append({
            "timestamp": time.time(),
            "data": new_data
        })
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
            
        print("--- Exam Data Successfully Updated & Secured ---")
    except Exception as e:
        print(f"[Storage Error] {e}")

if __name__ == "__main__":
    auto_scale_scraper()
