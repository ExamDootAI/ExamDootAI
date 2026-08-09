import json
import re
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

EXAM_SITES = [
    {
        "id": "wbprb",
        "exam_name": "West Bengal Group D / WBPRB",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBPRB+OR+West+Bengal+Police+recruitment+notice&hl=bn&gl=IN&ceid=IN:bn",
        "default_url": "https://wbpolice.gov.in/"
    },
    {
        "id": "wbpsc",
        "exam_name": "WBPSC (West Bengal Public Service Commission)",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBPSC+OR+West+Bengal+Public+Service+Commission+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://psc.wb.gov.in/"
    },
    {
        "id": "wbbpe",
        "exam_name": "WBBPE (Primary TET / Education)",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBBPE+OR+Primary+TET+West+Bengal+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://wbbpe.wb.gov.in/"
    },
    {
        "id": "wbhrb",
        "exam_name": "West Bengal Health Recruitment Board (WBHRB)",
        "category": "wb",
        "url": "https://news.google.com/rss/search?q=WBHRB+site:wbhrb.in&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://wbhrb.in/"
    },
    {
        "id": "ssc",
        "exam_name": "SSC (Staff Selection Commission)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=SSC+Staff+Selection+Commission+recruitment+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://ssc.gov.in/"
    },
    {
        "id": "upsc",
        "exam_name": "Union Public Service Commission (UPSC)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=UPSC+Union+Public+Service+Commission+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://upsc.gov.in/"
    },
    {
        "id": "rrb",
        "exam_name": "Railway Recruitment Board (RRB)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=RRB+Railway+Recruitment+Board+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://indianrailways.gov.in/"
    },
    {
        "id": "ibps",
        "exam_name": "IBPS (Banking - PO & Clerk)",
        "category": "central",
        "url": "https://news.google.com/rss/search?q=IBPS+banking+recruitment+notice&hl=en&gl=IN&ceid=IN:en",
        "default_url": "https://www.ibps.in/"
    }
]

def scan_website(site):
    print(f"Scanning {site['exam_name']} via Google News RSS...")
    result = {
        "exam_name": site["exam_name"],
        "category": site["category"],
        "status": "Site Active 🟢",
        "form_fillup_start": "অফিশিয়াল সাইট: <a href='" + site['default_url'] + "' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>" + site['default_url'].replace('https://', '').replace('/', '') + "</a>",
        "form_fillup_end": f"বিস্তারিত জানতে <a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ক্লিক করুন</a>"
    }
    
    try:
        req = urllib.request.Request(site['url'], headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, context=ssl_context, timeout=15)
        xml_data = response.read().decode('utf-8', errors='ignore')
        
        titles = re.findall(r'<item>.*?<title>(.*?)</title>', xml_data, re.IGNORECASE | re.DOTALL)
        if titles:
            latest_news = titles[0].replace('&#39;', "'").replace('&quot;', '"')
            latest_news = latest_news[:60] + "..." if len(latest_news) > 60 else latest_news
            result["status"] = "New Update 🔔"
            result["form_fillup_start"] = f"আপডেট: {latest_news}"
            result["form_fillup_end"] = f"বিস্তারিত জানতে <a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ক্লিক করুন</a>"
            
    except Exception as e:
        print(f"Error scanning {site['exam_name']}: {e}")
            
    return result

def run_master_bot():
    all_exams = []
    for site in EXAM_SITES:
        data = scan_website(site)
        all_exams.append(data)
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_master_bot()
