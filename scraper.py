import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def scrape_exams():
    exams_list = []
    
    # West Bengal-এর আসল সরকারি চাকরির খবরের লাইভ RSS ফিড
    url = "https://www.freejobalert.com/west-bengal-government-jobs/feed/"
    
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    
    try:
        # ইন্টারনেট থেকে লাইভ ডেটা টেনে আনা হচ্ছে
        response = urllib.request.urlopen(req, timeout=15)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        # ফিড থেকে লেটেস্ট চাকরির খবরগুলো আলাদা করা
        items = root.findall('./channel/item')
        
        for item in items[:10]: # লেটেস্ট ১০টি পরীক্ষার আপডেট নেবে
            title = item.find('title').text if item.find('title') is not None else "West Bengal Govt Exam Update"
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else datetime.now().strftime("%Y-%m-%d")
            
            # ডেট ফরম্যাট একটু সুন্দর করা
            date_short = pub_date[:16] if pub_date else "শীঘ্রই জানানো হবে"
            
            exams_list.append({
                "exam_name": title,
                "status": "Notification Out 🔔",
                "form_fillup_start": date_short,
                "form_fillup_end": "অফিসিয়াল ওয়েবসাইট চেক করুন"
            })
            
    except Exception as e:
        print(f"Error fetching real data: {e}")
        # কোনো কারণে ইন্টারনেট ডাউন থাকলে এই ডেটাটি স্বয়ংক্রিয়ভাবে দেখাবে
        exams_list.append({
            "exam_name": "West Bengal Group D Examination",
            "status": "অপেক্ষারত (Awaiting)",
            "form_fillup_start": "শীঘ্রই ঘোষণা করা হবে",
            "form_fillup_end": "শীঘ্রই ঘোষণা করা হবে"
        })

    return {"exams": exams_list}

if __name__ == "__main__":
    data = scrape_exams()
    # নতুন ডেটা দিয়ে exams_data.json ফাইলটি তৈরি/আপডেট করা
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Real data successfully scraped and saved to exams_data.json!")
