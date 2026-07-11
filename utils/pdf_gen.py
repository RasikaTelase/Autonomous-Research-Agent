# # from fpdf import FPDF
# # import re


# # def _break_long_words(s: str, max_len: int = 60) -> str:
# #     """Insert spaces into very long unbroken sequences so FPDF can wrap them.

# #     FPDF will raise "Not enough horizontal space to render a single character"
# #     when encountering a single token longer than the printable width. This
# #     helper splits tokens longer than max_len by inserting spaces every
# #     max_len characters.
# #     """
# #     if not s:
# #         return s
# #     # Replace any continuous non-whitespace sequence longer than max_len
# #     pattern = r"(\S{%d,})" % max_len

# #     def _split_match(m):
# #         token = m.group(0)
# #         parts = [token[i : i + max_len] for i in range(0, len(token), max_len)]
# #         return " ".join(parts)

# #     return re.sub(pattern, _split_match, s)


# # def clean_text(text: str) -> str:
# #     """Sanitize text for FPDF: remove unsupported characters and break long tokens.

# #     - Ensures input is a string
# #     - Breaks long unbroken tokens so FPDF can wrap
# #     - Encodes to latin-1 with replacement to drop unsupported glyphs
# #     """
# #     if not isinstance(text, str):
# #         text = str(text)
# #     # First make sure very long words/URLs have break points
# #     safe = _break_long_words(text, max_len=60)
# #     # Encode to latin-1 to drop unsupported unicode, then decode back
# #     return safe.encode("latin-1", "replace").decode("latin-1")

# # def generate_pdf_report(data, web_url):
# #     pdf = FPDF()
# #     pdf.add_page()
# #     pdf.set_auto_page_break(auto=True, margin=15)
    
# #     # Header
# #     pdf.set_font("Helvetica", "B", 16)
# #     title = clean_text(f"COMPANY RESEARCH REPORT: {data.get('company_name', 'N/A').upper()}")
# #     pdf.multi_cell(0, 10, title, align="C")
# #     pdf.ln(5)
    
# #     # Basic Info
# #     pdf.set_font("Helvetica", "", 12)
# #     pdf.multi_cell(0, 8, clean_text(f"Website: {web_url}"))
# #     pdf.multi_cell(0, 8, clean_text(f"Phone: {data.get('phone', 'Not Provided')}"))
# #     pdf.multi_cell(0, 8, clean_text(f"Address: {data.get('address', 'Not Provided')}"))
# #     pdf.ln(5)
    
# #     # Summary (if available)
# #     summary_text = data.get('summary') or data.get('company_summary')
# #     if summary_text:
# #         pdf.set_font("Helvetica", "B", 12)
# #         pdf.multi_cell(0, 8, clean_text("Company Summary:"))
# #         pdf.set_font("Helvetica", "", 11)
# #         pdf.multi_cell(0, 6, clean_text(summary_text))
# #         pdf.ln(5)

# #     # Products
# #     pdf.set_font("Helvetica", "B", 12)
# #     pdf.multi_cell(0, 8, clean_text("Products & Services:"))
# #     pdf.set_font("Helvetica", "", 11)
# #     for prod in data.get('products_services', []):
# #         pdf.multi_cell(0, 6, clean_text(f"- {prod}"))
# #     pdf.ln(5)
    
# #     # Pain Points
# #     pdf.set_font("Helvetica", "B", 12)
# #     pdf.multi_cell(0, 8, clean_text("AI-Generated Pain Points:"))
# #     pdf.set_font("Helvetica", "", 11)
# #     for pain in data.get('pain_points', []):
# #         pdf.multi_cell(0, 6, clean_text(f"- {pain}"))
# #     pdf.ln(5)
    
# #     # Competitors
# #     pdf.set_font("Helvetica", "B", 12)
# #     pdf.multi_cell(0, 8, clean_text("Competitors:"))
# #     pdf.set_font("Helvetica", "", 11)
# #     for comp in data.get('competitors', []):
# #         comp_name = comp.get('name', 'Unknown')
# #         comp_web = comp.get('website', '')
# #         pdf.multi_cell(0, 6, clean_text(f"- {comp_name} ({comp_web})"))
        
# #     return pdf.output(dest='S')




# from fpdf import FPDF
# import re

# def clean_text(text):
#     """Sanitize and break text for FPDF to prevent width constraint crashes."""
#     if not text:
#         return "Not Provided"
    
#     text = str(text)
    
#     # 1. Replace problematic Unicode with ASCII equivalents
#     replacements = {
#         '"': '"', '"': '"', ''': "'", ''': "'", 
#         '–': '-', '—': '-', '…': '...',
#         '®': '(R)', '™': '(TM)', '©': '(C)'
#     }
#     for bad_char, good_char in replacements.items():
#         text = text.replace(bad_char, good_char)
    
#     # 2. Encode to latin-1 to drop unsupported chars
#     text = text.encode('latin-1', 'replace').decode('latin-1')
    
#     # 3. AGGRESSIVE word breaking: insert space every 30 chars in any word
#     def wrap_words(s):
#         words = s.split(' ')
#         result = []
#         for word in words:
#             # For each word, if it's longer than 30 chars, break it up
#             if len(word) > 30:
#                 # Insert a space every 30 characters
#                 wrapped = ' '.join([word[i:i+30] for i in range(0, len(word), 30)])
#                 result.append(wrapped)
#             else:
#                 result.append(word)
#         return ' '.join(result)
    
#     text = wrap_words(text)
    
#     # 4. Also try to replace very long URLs with shortened text
#     text = re.sub(r'https?://[^\s]{40,}', 'WEBSITE_URL', text)
    
#     return text

# def generate_pdf_report(data, web_url):
#     """Generate a PDF report with explicit width handling to avoid FPDF crashes."""
#     try:
#         pdf = FPDF(format='A4')
#         pdf.add_page()
        
#         # Set tight margins: 8mm all around
#         pdf.set_margins(8, 8, 8)
#         pdf.set_auto_page_break(auto=True, margin=8)
        
#         # Usable width: A4 is 210mm, minus 16mm for margins = 194mm
#         usable_width = 194
        
#         # Title
#         pdf.set_font("Helvetica", "B", 12)
#         title = clean_text(f"COMPANY RESEARCH REPORT: {data.get('company_name', 'N/A')}")
#         pdf.cell(0, 6, title, ln=True, align="C")
#         pdf.ln(2)
        
#         # Website
#         pdf.set_font("Helvetica", "", 9)
#         website_text = clean_text(f"Website: {web_url}")
#         pdf.multi_cell(w=usable_width, h=4, txt=website_text, border=0)
        
#         # Phone
#         phone_text = clean_text(f"Phone: {data.get('phone', 'Not Provided')}")
#         pdf.multi_cell(w=usable_width, h=4, txt=phone_text, border=0)
        
#         # Address
#         address_text = clean_text(f"Address: {data.get('address', 'Not Provided')}")
#         pdf.multi_cell(w=usable_width, h=4, txt=address_text, border=0)
        
#         pdf.ln(2)
        
#         # Summary
#         summary_text = data.get('summary') or data.get('company_summary')
#         if summary_text and summary_text != "Not Provided":
#             pdf.set_font("Helvetica", "B", 10)
#             pdf.cell(0, 5, "Company Summary:", ln=True)
#             pdf.set_font("Helvetica", "", 9)
#             pdf.multi_cell(w=usable_width, h=4, txt=clean_text(summary_text), border=0)
#             pdf.ln(1)

#         # Products
#         pdf.set_font("Helvetica", "B", 10)
#         pdf.cell(0, 5, "Products & Services:", ln=True)
#         pdf.set_font("Helvetica", "", 9)
#         for prod in data.get('products_services', []):
#             pdf.multi_cell(w=usable_width, h=4, txt=clean_text(f"- {prod}"), border=0)
#         pdf.ln(1)
        
#         # Pain Points
#         pdf.set_font("Helvetica", "B", 10)
#         pdf.cell(0, 5, "AI-Generated Pain Points:", ln=True)
#         pdf.set_font("Helvetica", "", 9)
#         for pain in data.get('pain_points', []):
#             pdf.multi_cell(w=usable_width, h=4, txt=clean_text(f"- {pain}"), border=0)
#         pdf.ln(1)
        
#         # Competitors
#         pdf.set_font("Helvetica", "B", 10)
#         pdf.cell(0, 5, "Competitors:", ln=True)
#         pdf.set_font("Helvetica", "", 9)
#         for comp in data.get('competitors', []):
#             comp_name = comp.get('name', 'Unknown')
#             comp_web = comp.get('website', 'N/A')
#             pdf.multi_cell(w=usable_width, h=4, txt=clean_text(f"- {comp_name} ({comp_web})"), border=0)
        
#         # Output PDF
#         try:
#             pdf_bytes = pdf.output()
#             if isinstance(pdf_bytes, str):
#                 pdf_bytes = pdf_bytes.encode('latin-1')
#             return pdf_bytes if pdf_bytes else None
#         except (TypeError, AttributeError):
#             pdf_bytes = pdf.output(dest='S')
#             if isinstance(pdf_bytes, str):
#                 pdf_bytes = pdf_bytes.encode('latin-1')
#             return pdf_bytes if pdf_bytes else None
            
#     except Exception as e:
#         print(f"[PDF ERROR] {type(e).__name__}: {e}")
#         return None






from fpdf import FPDF
import textwrap

def clean_text(text):
    """Text ko pure ASCII mein convert karta hai taaki fonts crash na hon."""
    if not text:
        return "Not Provided"
    text = str(text).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    return text.encode('ascii', 'ignore').decode('ascii')

def generate_pdf_report(data, web_url):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # --- Helper Function for Safe Writing ---
        def add_line(text, is_bold=False, size=11):
            # FIX: Only using 'Helvetica' as it is a guaranteed built-in core font in FPDF
            pdf.set_font("Helvetica", "B" if is_bold else "", size)
            lines = textwrap.wrap(clean_text(text), width=80, break_long_words=True)
            if not lines:
                pdf.cell(0, 6, "", ln=1)
            for line in lines:
                pdf.cell(0, 6, line, ln=1)

        # --- HEADER ---
        add_line(f"COMPANY RESEARCH REPORT: {data.get('company_name', 'N/A').upper()}", is_bold=True, size=16)
        pdf.ln(5)
        
        # --- BASIC INFO ---
        add_line(f"Website: {web_url}")
        add_line(f"Phone: {data.get('phone', 'Not Provided')}")
        add_line(f"Address: {data.get('address', 'Not Provided')}")
        pdf.ln(5)
        
        # --- SUMMARY ---
        summary_text = data.get('summary') or data.get('company_summary')
        if summary_text:
            add_line("Company Summary:", is_bold=True, size=12)
            add_line(summary_text)
            pdf.ln(5)

        # --- PRODUCTS ---
        add_line("Products & Services:", is_bold=True, size=12)
        prods = data.get('products_services', [])
        if isinstance(prods, list):
            for p in prods: add_line(f"- {p}")
        else:
            add_line(f"- {prods}")
        pdf.ln(5)
        
        # --- PAIN POINTS ---
        add_line("AI-Generated Pain Points:", is_bold=True, size=12)
        pains = data.get('pain_points', [])
        if isinstance(pains, list):
            for p in pains: add_line(f"- {p}")
        else:
            add_line(f"- {pains}")
        pdf.ln(5)
        
        # --- COMPETITORS ---
        add_line("Competitors:", is_bold=True, size=12)
        comps = data.get('competitors', [])
        if isinstance(comps, list):
            for c in comps:
                if isinstance(c, dict):
                    add_line(f"- {c.get('name', 'Unknown')} ({c.get('website', '')})")
                else:
                    add_line(f"- {c}")
        else:
            add_line(f"- {comps}")

        # ==========================================
        # THE ULTIMATE SAFE OUTPUT (Handles FPDF v1 & v2)
        # ==========================================
        out = pdf.output(dest='S')
        if isinstance(out, str):
            # FPDF 1 returns a string
            return out.encode('latin-1')
        else:
            # FPDF 2 returns a bytearray
            return bytes(out)

    except Exception as e:
        print(f"\n---> CRITICAL PDF ERROR: {e} <---\n")
        return None