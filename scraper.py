import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

# Exam sources configuration
SOURCES = [
    {
        "name": "West Bengal Group D / WBPRB",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBPRB+West+Bengal+Police+recruitment&hl=en&gl=IN&ceid=IN:en"
    },
    {
        "name": "WBPSC (West Bengal Public Service Commission)",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBPSC+West+Bengal+Public+Service+Commission+notice&hl=en&gl=IN&ceid=IN:en"
    },
    {
        "name": "SSC (Staff Selection Commission)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=SSC+Staff+Selection+Commission+notice&hl=en&gl=IN&ceid=IN:en"
    },
    {
        "name": "Union Public Service Commission (UPSC)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=UPSC+recruitment+notification&hl=en&gl=IN&ceid=IN:en"
    },
    {
        "name": "Railway Recruitment Board (RRB)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=RRB+Railway+Recruitment+Board+notice&hl=en&gl=IN&ceid=IN:en"
    }
]

def clean_text(text):
    if not text:
        return ""
    clean = re.sub('<.*?>', '', text)
    return clean.strip()

def fetch_exam_data():
    exams_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for source in SOURCES:
        try:
            req = urllib.request.Request(source["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            items = root.findall('.//item')
            
            status_text = "Site Active 🟢"
            fillup_start = "অফিসিয়াল নোটিশ অনুযায়ী আপডেট দেখুন"
            fillup_end = "বিস্তারিত জানতে বিস্তারিত লিঙ্কে ক্লিক করুন"
            
            if items:
                latest_item = items[0]
                title = clean_text(latest_item.find('title').text) if latest_item.find('title') is not None else ""
                link = latest_item.find('link').text if latest_item.find('link') is not None else ""
                
                if title:
                    status_text = "New Update 🔔"
                    fillup_start = f"আপডেট: {title[:80]}..."
                    fillup_end = f"বিস্তারিত জানতে <a href='{link}' target='_blank' rel='noopener noreferrer'>ক্লিক করুন</a>"
            
            exams_list.append({
                "exam_name": source["name"],
                "category": source["category"],
                "status": status_text,
                "form_fillup_start": fillup_start,
                "form_fillup_end": fillup_end
            })
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")
            exams_list.append({
                "exam_name": source["name"],
                "category": source["category"],
                "status": "Site Active 🟢",
                "form_fillup_start": "অফিসিয়াল সাইট: <a href='https://indianrailways.gov.in' target='_blank' rel='noopener noreferrer'>indianrailways.gov.in</a>" if "RRB" in source["name"] else "অফিসিয়াল সাইট চেক করুন",
                "form_fillup_end": "বিস্তারিত জানতে অফিসিয়াল ওয়েবসাইটে যান"
            })

    output_data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "exams": exams_list
    }

    with open("exams_data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    print("exams_data.json successfully updated!")
 
if __name__ == "__main__":
    fetch_exam_data()
