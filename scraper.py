import json
import re
import urllib.request
import urllib.parse
import ssl

# সাধারণ সাইটের জন্য SSL মাস্টার-কি
ssl_context = ssl._create_unverified_context()

# আপনার ScraperAPI Key (WBPSC-এর জন্য)
API_KEY = "0bacbfa123fb6b3ff27bd417951af2fe"

# ==========================================
# কনফিগারেশন লিস্ট (Hybrid + Google News RSS + All Official Sites)
# ==========================================
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
        "exam_name": "WBPSC (West Bengal Public Service Commission)",
        "url": "https://psc.wb.gov.in/",
        "keywords": ["Advertisement", "Notice", "Result"],
        "default_url": "https://psc.wb.gov.in/",
        "method": "scraperapi"
    },
    {
        "id": "wbbpe",
        "exam_name": "WBBPE (Primary TET / Education)",
        "url": "https://wbbpe.org/",
        "keywords": ["Notice", "Notification", "TET"],
        "default_url": "https://wbbpe.org/",
        "method": "basic"
    },
    {
        "id": "wbhrb",
        "exam_name": "West Bengal Health Recruitment Board (WBHRB)",
        "url": "https://wbhrb.in/",
        "keywords": ["Advertisement", "Notice"],
        "default_url": "https://wbhrb.in/",
        "method": "basic"
    },
    {
        "id": "ssc",
        "exam_name": "SSC (Staff Selection Commission)",
        "url": "https://ssc.gov.in/",
        "keywords": ["Notice", "Examination", "Result", "Apply"],
        "default_url": "https://ssc.gov.in/",
        "method": "basic"
    },
    {
        "id": "upsc",
        "exam_name": "UPSC (Union Public Service Commission)",
        "url": "https://upsc.gov.in/",
        "keywords": ["Notification", "Examination"],
        "default_url": "https://upsc.gov.in/",
        "method": "basic"
    },
    {
        "id": "rrb",
        "exam_name": "RRB (Railway Recruitment Board)",
        "url": "https://indianrailways.gov.in/",
        "keywords": ["Recruitment", "Notice", "Railway"],
        "default_url": "https://indianrailways.gov.in/",
        "method": "basic"
    },
    {
        "id": "ibps",
        "exam_name": "IBPS (Banking - PO & Clerk)",
        "url": "https://www.ibps.in/",
        "keywords": ["CRP", "Notification", "CWE"],
        "default_url": "https://www.ibps.in/",
        "method": "basic"
    }
]

# ==========================================
# ইউনিভার্সাল স্ক্যানার
# ==========================================
def scan_website(site):
    print(f"Scanning {site['exam_name']}...")
    result = {
        "exam_name": site["exam_name"],
        "status": "সার্ভার ব্যস্ত 🔴",
        "form_fillup_start": "অফিশিয়াল সাইট: <a href='" + site['default_url'] + "' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>" + site['default_url'].replace('https://', '').replace('/', '') + "</a>",
        "form_fillup_end": f"বিস্তারিত জানতে <a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ক্লিক করুন</a>"
    }
    
    try:
        if site['method'] == 'google_news':
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
            else:
                result["status"] = "Site Active 🟢"
                result["form_fillup_start"] = "নতুন কোনো আপডেট নেই"
                
        elif site['method'] == 'scraperapi':
            target_url = urllib.parse.quote(site['url'])
            api_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={target_url}&country_code=in"
            
            req = urllib.request.Request(api_url)
            response = urllib.request.urlopen(req, timeout=30)
            html_data = response.read().decode('utf-8', errors='ignore')
            
            keywords_pattern = "|".join(site['keywords'])
            regex_str = rf'<a[^>]*>([^<]*(?:{keywords_pattern})[^<]*)</a>'
            notices = re.findall(regex_str, html_data, re.IGNORECASE)
            
            clean_notices = []
            for n in notices:
                clean_text = n.strip().replace('\n', '').replace('\r', '')
                if clean_text and len(clean_text) > 5 and clean_text not in clean_notices:
                    clean_notices.append(clean_text)
            
            if clean_notices:
                latest_notice = clean_notices[0][:60] + "..." if len(clean_notices[0]) > 60 else clean_notices[0]
                result["status"] = "New Update 🔔"
                result["form_fillup_start"] = f"নোটিশ: {latest_notice}"
                result["form_fillup_end"] = f"বিস্তারিত জানতে <a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ক্লিক করুন</a>"
            else:
                result["status"] = "Site Active 🟢"
                result["form_fillup_start"] = "আজ নতুন কোনো নোটিশ নেই"

        elif site['method'] == 'basic':
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(site['url'], headers=headers)
            response = urllib.request.urlopen(req, context=ssl_context, timeout=15)
            html_data = response.read().decode('utf-8', errors='ignore')
            
            keywords_pattern = "|".join(site['keywords'])
            regex_str = rf'<a[^>]*>([^<]*(?:{keywords_pattern})[^<]*)</a>'
            notices = re.findall(regex_str, html_data, re.IGNORECASE)
            
            clean_notices = []
            for n in notices:
                clean_text = n.strip().replace('\n', '').replace('\r', '')
                if clean_text and len(clean_text) > 5 and clean_text not in clean_notices:
                    clean_notices.append(clean_text)
            
            if clean_notices:
                latest_notice = clean_notices[0][:60] + "..." if len(clean_notices[0]) > 60 else clean_notices[0]
                result["status"] = "New Update 🔔"
                result["form_fillup_start"] = f"নোটিশ: {latest_notice}"
                result["form_fillup_end"] = f"বিস্তারিত জানতে <a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ক্লিক করুন</a>"
            else:
                result["status"] = "Site Active 🟢"
                result["form_fillup_start"] = "আজ নতুন কোনো নোটিশ নেই"
                
    except Exception as e:
        print(f"Error scanning {site['exam_name']}: {e}")
            
    return result

# ==========================================
# MASTER BOT
# ==========================================
def run_master_bot():
    all_exams = []
    
    for site in EXAM_SITES:
        data = scan_website(site)
        all_exams.append(data)
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_master_bot()
