import json
import re
import requests


def analyze_with_openrouter(crawled_text, website_url, api_key, model_choice):
    if not api_key or not model_choice:
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = """You are an elite Corporate Intelligence Analyst. 
    Your objective is to provide a COMPLETE, CLEAN, and ACCURATE research report.
    
    CRITICAL INSTRUCTIONS:
    1. USE YOUR OWN BRAIN: The scraped text provided to you might be incomplete, block pages, or contain website navigation junk (like "Skip to content", "Menu", etc.). 
    2. FILL IN THE BLANKS: If the scraped text is missing the HQ Address, Phone Number, or proper details, YOU MUST use your own pre-trained AI knowledge to provide them. NEVER output "Not Provided" for well-known companies (like Wipro, TCS, Apple, etc.). You know their details, so output them!
    3. CLEAN SUMMARY: Write a professional 2-sentence summary of the company. Do NOT copy-paste website navigation text.
    4. PRODUCTS & PAIN POINTS: List 3-4 actual products and 3-4 realistic business pain points.
    5. COMPETITORS: Provide 3-4 real competitors with their official website URLs.
    
    OUTPUT FORMAT:
    Return ONLY a strictly valid JSON object matching this exact schema:
    {
      "company_name": "Exact Company Name",
      "summary": "Clean 2-sentence professional summary",
      "phone": "Official Phone Number (Use your knowledge if missing)",
      "address": "Official HQ Address (Use your knowledge if missing)",
      "products_services": ["Product 1", "Service 2"],
      "pain_points": ["Pain point 1", "Pain point 2"],
      "competitors": [{"name": "Comp1", "website": "https://comp1.com"}]
    }"""

    user_prompt = f"Website: {website_url}\n\nExtracted Text:\n{crawled_text}"

    payload = {
        "model": model_choice,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 1200,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not content:
            return None

        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        parsed = json.loads(cleaned)
        return normalize_agent_output(parsed, crawled_text=crawled_text, website_url=website_url)

    except Exception as exc:
        print("OpenRouter Error:", exc)
        return None


def normalize_agent_output(payload, crawled_text=None, website_url=None):
    if not isinstance(payload, dict):
        return None

    company_name = payload.get("company_name") or "Not Provided"
    # Prefer an explicit company summary from the model; otherwise fall back to crawled text
    company_summary = payload.get("company_summary") or payload.get("summary")
    if not company_summary:
        if crawled_text and len(crawled_text) > 50:
            company_summary = (crawled_text[:700].rsplit(" ", 1)[0]) + "..."
        else:
            company_summary = "Not Provided"

    phone = payload.get("phone") or "Not Provided"
    address = payload.get("address") or "Not Provided"

    # Basic regex fallback in case the model did not fill phone/address
    if phone == "Not Provided" and crawled_text:
        phone = extract_phone(crawled_text) or "Not Provided"
    if address == "Not Provided" and crawled_text:
        address = extract_address(crawled_text) or "Not Provided"

    products_services = payload.get("products_services")
    if not isinstance(products_services, list) or not products_services:
        products_services = extract_products_services(crawled_text) or ["Not Provided"]

    competitors = payload.get("competitors")
    if not isinstance(competitors, list) or not competitors:
        competitors = extract_competitors(crawled_text) or []

    pain_points = payload.get("pain_points")
    if not isinstance(pain_points, list) or len(pain_points) < 3:
        pain_points = [
            "Operational inefficiency",
            "Limited scalability",
            "High manual effort"
        ]

    competitors = payload.get("competitors")
    if not isinstance(competitors, list):
        competitors = []

    cleaned_competitors = []
    for item in competitors:
        if isinstance(item, dict):
            cleaned_competitors.append({
                "name": item.get("name") or "Not Provided",
                "website": item.get("website") or "Not Provided"
            })

    if not cleaned_competitors:
        cleaned_competitors = [{"name": "Not Provided", "website": "Not Provided"}]

    return {
        "company_name": str(company_name),
        "company_summary": str(company_summary),
        "phone": str(phone),
        "address": str(address),
        "products_services": [str(item) for item in products_services[:5]],
        "pain_points": [str(item) for item in pain_points[:4]],
        "competitors": cleaned_competitors[:4]
    }


def extract_phone(text):
    phone_patterns = [
        r"\+?\d[\d\s\-()]{7,}\d",
        r"\(\d{2,4}\)\s*\d{6,}",
        r"\d{3}[\-\.\s]\d{3}[\-\.\s]\d{4}"
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone_candidate = match.group(0)
            return re.sub(r"\s+", " ", phone_candidate).strip()
    return None


def extract_address(text):
    address_patterns = [
        r"\d{1,5}\s+[A-Za-z0-9.,\s]+\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way|Pl|Place|Crescent|Circle|Terrace|Trail|Parkway|Pkwy)\b",
        r"\d{1,5}\s+[A-Za-z0-9.,\s]+\b(?:Building|Tower|Suite|Floor|Level)\b"
    ]
    for pattern in address_patterns:
        match = re.search(pattern, text)
        if match:
            address_candidate = match.group(0)
            return re.sub(r"\s+", " ", address_candidate).strip()
    return None


def extract_products_services(text):
    if not text:
        return None
    services = []
    patterns = [
        r"(?:Products|Services)\s*[:\-]\s*([A-Za-z0-9,\s&()]+)",
        r"(?:We offer|Our offerings include|Our services include)\s*([A-Za-z0-9,\s&()]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidates = [item.strip() for item in match.group(1).split(",") if item.strip()]
            if candidates:
                return candidates[:5]
    return None


def extract_competitors(text):
    if not text:
        return None
    competitor_names = []
    common_companies = [
        "Accenture", "Deloitte", "IBM", "Infosys", "Capgemini", "Tata Consultancy Services", "Wipro", "HCL"
    ]
    for company in common_companies:
        if re.search(rf"\b{re.escape(company)}\b", text, re.IGNORECASE):
            competitor_names.append(company)
    if not competitor_names:
        return None
    return [{"name": name, "website": "Not Provided"} for name in competitor_names[:4]]
    phone_patterns = [
        r"\+?\d[\d\s\-()]{7,}\d",
        r"\(\d{2,4}\)\s*\d{6,}",
        r"\d{3}[\-\.\s]\d{3}[\-\.\s]\d{4}"
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            phone_candidate = match.group(0)
            return re.sub(r"\s+", " ", phone_candidate).strip()
    return None


def extract_address(text):
    address_patterns = [
        r"\d{1,5}\s+[A-Za-z0-9.,\s]+\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way|Pl|Place|Crescent|Circle|Terrace|Trail|Parkway|Pkwy)\b",
        r"\d{1,5}\s+[A-Za-z0-9.,\s]+\b(?:Building|Tower|Suite|Floor|Level)\b"
    ]
    for pattern in address_patterns:
        match = re.search(pattern, text)
        if match:
            address_candidate = match.group(0)
            return re.sub(r"\s+", " ", address_candidate).strip()
    return None