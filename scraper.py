import json
import re
import cloudscraper

# ==========================================
# কনফিগারেশন লিস্ট
# ==========================================
EXAM_SITES = [
    {
        "id": "wbprb",
        "exam_name": "West Bengal Group D / WBPRB",
        "url": "https://wbpolice.gov.in/",
        "keywords": ["Notice", "Recruitment", "Group D", "Constable"],
        "default_url": "https://wbpolice.gov.in/"
    },
    {
        "id": "wbpsc",
        "exam_name": "WBPSC Official Website",
        "url": "https://psc.wb.gov.in/",
        "keywords": ["Advertisement", "Notice", "Result"],
        "default_url": "https://psc.wb.gov.in/"
    },
    {
        "id": "ssc",
        "exam_name": "SSC (Staff Selection Commission)",
        "url": "https://ssc.gov.in/",
        "keywords": ["Notice", "Examination", "Result", "Apply"],
        "default_url": "https://ssc.gov.in/"
    }
]

# ==========================================
# ইউনিভার্সাল স্ক্যানার (Cloudscraper Enabled)
# ==========================================
def scan_website(site):
    print(f"Scanning {site['exam_name']}...")
    result = {
        "exam_name": site["exam_name"],
        "status": "সার্ভার ব্যস্ত 🔴",
        "form_fillup_start": "-",
        "form_fillup_end": f"<a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>ওয়েবসাইট</a> চেক করুন"
    }
    
    try:
        # Cloudscraper দিয়ে অ্যাডভান্সড বাইপাস
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        response = scraper.get(site['url'], timeout=20)
        html_data = response.text
        
        # Regex দিয়ে নোটিশ খোঁজা
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
            result["form_fillup_end"] = f"<a href='{site['default_url']}' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>অফিসিয়াল ওয়েবসাইট</a> চেক করুন"
            
    except Exception as e:
        print(f"Error scanning {site['exam_name']}: {e}")
        if site['id'] == 'wbprb':
            result["form_fillup_start"] = "শীঘ্রই ঘোষণা করা হবে"
            
    return result

# ==========================================
# MASTER BOT
# ==========================================
def run_master_bot():
    all_exams = []
    
    for site in EXAM_SITES:
        data = scan_website(site)
        all_exams.append(data)
        
    all_exams.append({
        "exam_name": "RRB (Railway Recruitment Board)",
        "status": "নতুন আপডেটের খোঁজ চলছে 🚂",
        "form_fillup_start": "<a href='https://indianrailways.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>indianrailways.gov.in</a>",
        "form_fillup_end": "<a href='https://indianrailways.gov.in/' target='_blank' style='color: #007bff; text-decoration: none; font-weight: bold;'>indianrailways.gov.in</a>"
    })
    
    with open('exams_data.json', 'w', encoding='utf-8') as f:
        json.dump({"exams": all_exams}, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    run_master_bot()
