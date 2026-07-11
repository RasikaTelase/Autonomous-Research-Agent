# import requests
# from bs4 import BeautifulSoup

# try:
#     from requests_html import HTMLSession
#     HAS_REQUESTS_HTML = True
# except ImportError:
#     HAS_REQUESTS_HTML = False


# def intelligent_crawl(url):
#     """
#     Fetch and parse a webpage, remove unwanted tags, and extract clean text.
#     Tries requests-html (with JS rendering) first, falls back to plain requests.
#     Returns up to 12000 characters of clean text.
#     """
#     if not url:
#         return ""
    
#     # Add http:// if no scheme is provided
#     if not url.startswith(("http://", "https://")):
#         url = "https://" + url
    
#     try:
#         text = _scrape_with_js_rendering(url) if HAS_REQUESTS_HTML else None
        
#         if not text or len(text.strip()) < 50:
#             text = _scrape_plain_requests(url)
        
#         return text[:12000] if text else ""
    
#     except Exception as e:
#         print(f"Scraper Error: {e}")
#         return ""


# def _scrape_with_js_rendering(url):
#     """Use requests-html to render JavaScript and extract content."""
#     try:
#         session = HTMLSession()
#         response = session.get(url, timeout=20)
        
#         # Try to render JavaScript
#         response.html.render(timeout=10, sleep=1)
        
#         soup = BeautifulSoup(response.html.html, "html.parser")
#         return _extract_clean_text(soup)
    
#     except Exception as e:
#         print(f"JS rendering failed: {e}")
#         return None


# def _scrape_plain_requests(url):
#     """Fallback: use plain requests with better headers."""
#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Accept-Encoding": "gzip, deflate",
#             "Connection": "keep-alive",
#             "Upgrade-Insecure-Requests": "1"
#         }
        
#         response = requests.get(url, headers=headers, timeout=15)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.content, "html.parser")
#         return _extract_clean_text(soup)
    
#     except Exception as e:
#         print(f"Plain request failed: {e}")
#         return None


# def _extract_clean_text(soup):
#     """Extract clean text from BeautifulSoup object."""
#     try:
#         # Remove unwanted tags
#         for tag in soup.find_all(["script", "style", "nav", "footer", "noscript", "meta", "link", "head"]):
#             tag.decompose()
        
#         # Extract meta description as a concise summary
#         meta_desc = ""
#         desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
#         if desc_tag and desc_tag.get("content"):
#             meta_desc = desc_tag.get("content").strip()

#         # Extract main page text
#         text = soup.get_text(separator=" ", strip=True)
        
#         # Clean up whitespace
#         text = " ".join(text.split())

#         # Prepend meta description if available
#         if meta_desc:
#             combined = meta_desc + "\n\n" + text
#         else:
#             combined = text

#         return combined if combined else None
    
#     except Exception as e:
#         print(f"Text extraction failed: {e}")
#         return None





import requests
from bs4 import BeautifulSoup
import re

def intelligent_crawl(target_url):
    try:
        # Hackathon Pro-Tip: Using r.jina.ai to bypass JavaScript and Bot blockers for free
        jina_url = f"https://r.jina.ai/{target_url}"
        
        # Adding realistic browser headers to trick basic blockers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        res = requests.get(jina_url, headers=headers, timeout=15)
        
        # If Jina successfully converted the JS site to text
        if res.status_code == 200 and len(res.text) > 50:
            clean_text = res.text
        else:
            # Fallback: Standard BeautifulSoup method if Jina fails
            direct_res = requests.get(target_url, headers=headers, timeout=10)
            soup = BeautifulSoup(direct_res.text, "html.parser")
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            clean_text = soup.get_text(separator=" ")
            
        # Clean up extra spaces and limit tokens for OpenRouter
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text[:12000] 
        
    except Exception as e:
        print(f"Scraping Error: {e}")
        # Return a fallback string so the AI still tries its best with just the company name
        return "Website content blocked by firewall. Please rely on your internal knowledge to generate the report for this company."