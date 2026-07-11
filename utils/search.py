import requests
import json

def get_official_website(company_name, api_key):
    if not api_key: return None
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = json.dumps({"q": f"{company_name} official website home page"})
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            results = response.json().get("organic", [])
            if results:
                return results[0].get("link")
    except Exception as e:
        print("Serper Error:", e)
    return None