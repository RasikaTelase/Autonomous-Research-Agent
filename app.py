# import os
# from pathlib import Path
# import streamlit as st
# from urllib.parse import urlparse

# # Import modular functions
# from utils.search import get_official_website
# from utils.scraper import intelligent_crawl
# from utils.ai_agent import analyze_with_openrouter
# from utils.pdf_gen import generate_pdf_report
# from utils.discord_bot import send_to_discord

# # Page UI Config
# st.set_page_config(page_title="Company Research AI", layout="wide")

# # Sidebar for Settings
# st.sidebar.title("⚙️ Configuration")
# config_path = Path(".env")
# if "openrouter_key" not in st.session_state:
#     st.session_state.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
# if "serper_key" not in st.session_state:
#     st.session_state.serper_key = os.getenv("SERPER_API_KEY", "")
# if "discord_token" not in st.session_state:
#     st.session_state.discord_token = ""
# if "discord_channel" not in st.session_state:
#     st.session_state.discord_channel = ""
# if "app_name" not in st.session_state:
#     st.session_state.app_name = ""
# if "app_email" not in st.session_state:
#     st.session_state.app_email = ""

# openrouter_key = st.sidebar.text_input("OpenRouter API Key", type="password", key="openrouter_key")
# serper_key = st.sidebar.text_input("Serper API Key", type="password", key="serper_key")
# selected_model = st.sidebar.selectbox("AI Model", ["google/gemini-2.5-flash", "meta-llama/llama-3-70b-instruct"])

# if st.sidebar.button("Save API keys for next time"):
#     lines = []
#     if openrouter_key:
#         lines.append(f"OPENROUTER_API_KEY={openrouter_key}")
#     if serper_key:
#         lines.append(f"SERPER_API_KEY={serper_key}")
#     config_path.write_text("\n".join(lines))
#     st.sidebar.success("API keys saved to .env")

# st.sidebar.markdown("---")
# st.sidebar.subheader("Discord Integration (Bonus)")
# discord_token = st.sidebar.text_input("Bot Token", type="password", key="discord_token")
# discord_channel = st.sidebar.text_input("Channel ID", key="discord_channel")
# app_name = st.sidebar.text_input("Your Name", key="app_name")
# app_email = st.sidebar.text_input("Your Email", key="app_email")

# # Main Interface
# st.title("AI-Powered Company Research Assistant")
# st.markdown("Enter a company name (e.g., Stripe) or a website URL to generate an automated research report.")

# query = st.text_input("Enter company name or URL...", key="user_query")
# search_clicked = st.button("Analyze Company")

# if search_clicked and query:
#     if not openrouter_key or not serper_key:
#         st.error("❌ Please enter OpenRouter and Serper API keys in the sidebar first!")
#         st.stop()

#     st.markdown(f"**You asked:** {query}")
#     try:
#         # 1. Resolve URL
#         is_url = urlparse(query).scheme in ('http', 'https')
#         target_url = query if is_url else get_official_website(query, serper_key)
        
#         if not target_url:
#             st.error("❌ Failed to find website. Check company name or try a direct URL.")
#             st.stop()
            
#         st.write(f"**🌐 Target Website:** {target_url}")
        
#         # 2. Crawl Website
#         raw_text = intelligent_crawl(target_url)
        
#         if not raw_text or len(raw_text.strip()) < 50:
#             st.error("⚠️ Could not extract meaningful content from the website. It might be blocked or require JavaScript.")
#             st.stop()
        
#         # 3. AI Analysis
#         report_data = analyze_with_openrouter(raw_text, target_url, openrouter_key, selected_model)
        
#         if not report_data:
#             st.error("❌ AI analysis failed. Check your OpenRouter API key or try again.")
#             st.stop()

#         # Pre-generate PDF bytes so we can expose a download button in the top-right
#         pdf_bytes = generate_pdf_report(report_data, target_url)
#         filename = f"{report_data.get('company_name', 'Report')}.pdf"

#         # Layout: main content on the left, download button in a narrow right column
#         col_main, col_action = st.columns([8, 1])

#         # Action column (top-right) - download button
#         with col_action:
#             if pdf_bytes:
#                 st.download_button("📥 Download", data=pdf_bytes, file_name=filename, mime="application/pdf")
#             else:
#                 st.warning("PDF generation failed. Please try again or check the company data.")

#         # Main column: report content
#         with col_main:
#             st.subheader(f"🏢 {report_data.get('company_name')}")
#             # Company summary (if provided)
#             summary = report_data.get('company_summary') or report_data.get('summary')
#             if summary and summary != "Not Provided":
#                 st.markdown("### 📝 Summary")
#                 st.write(summary)

#             st.write(f"**Phone:** {report_data.get('phone')} | **Address:** {report_data.get('address')}")
            
#             st.markdown("### 📦 Products/Services")
#             st.write(", ".join(report_data.get('products_services', [])))
            
#             st.markdown("### ⚠️ Pain Points")
#             for p in report_data.get('pain_points', []):
#                 st.write(f"- {p}")
                
#             st.markdown("### ⚔️ Competitors")
#             for c in report_data.get('competitors', []):
#                 st.write(f"- [{c.get('name')}]({c.get('website')})")
        
#         # 5. Discord Integration
#         if discord_token and discord_channel:
#             st.info("Sending report to Discord...")
#             success = send_to_discord(pdf_bytes, filename, app_name, app_email, report_data.get('company_name'), target_url, discord_token, discord_channel)
#             if success:
#                 st.success("Sent to Discord successfully!")
#             else:
#                 st.error("Failed to send to Discord. Check your Bot Token/Channel ID.")
#     except Exception as e:
#         st.error(f"An unexpected error occurred: {str(e)}")




import os
from pathlib import Path
import streamlit as st
from urllib.parse import urlparse

# Import modular functions
from utils.search import get_official_website
from utils.scraper import intelligent_crawl
from utils.ai_agent import analyze_with_openrouter
from utils.pdf_gen import generate_pdf_report
from utils.discord_bot import send_to_discord

# Page UI Config
st.set_page_config(page_title="Company Research AI", layout="wide")

# Sidebar for Settings
st.sidebar.title("⚙️ Configuration")
config_path = Path(".env")

if "openrouter_key" not in st.session_state:
    st.session_state.openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
if "serper_key" not in st.session_state:
    st.session_state.serper_key = os.getenv("SERPER_API_KEY", "")
if "discord_token" not in st.session_state:
    st.session_state.discord_token = ""
if "discord_channel" not in st.session_state:
    st.session_state.discord_channel = ""
if "app_name" not in st.session_state:
    st.session_state.app_name = ""
if "app_email" not in st.session_state:
    st.session_state.app_email = ""

openrouter_key = st.sidebar.text_input("OpenRouter API Key", type="password", key="openrouter_key")
serper_key = st.sidebar.text_input("Serper API Key", type="password", key="serper_key")
selected_model = st.sidebar.selectbox("AI Model", ["google/gemini-2.5-flash", "meta-llama/llama-3-70b-instruct"])

if st.sidebar.button("Save API keys for next time"):
    lines = []
    if openrouter_key:
        lines.append(f"OPENROUTER_API_KEY={openrouter_key}")
    if serper_key:
        lines.append(f"SERPER_API_KEY={serper_key}")
    config_path.write_text("\n".join(lines))
    st.sidebar.success("API keys saved to .env")

st.sidebar.markdown("---")
st.sidebar.subheader("Discord Integration (Bonus)")
discord_token = st.sidebar.text_input("Bot Token", type="password", key="discord_token")
discord_channel = st.sidebar.text_input("Channel ID", key="discord_channel")
app_name = st.sidebar.text_input("Your Name", key="app_name")
app_email = st.sidebar.text_input("Your Email", key="app_email")

# Main Interface
st.title("AI-Powered Company Research Assistant")
st.markdown("Enter a company name (e.g., Stripe) or a website URL to generate an automated research report.")

query = st.text_input("Enter company name or URL...", key="user_query")
analyze_btn = st.button("🔍 Analyze Company")

if analyze_btn and query:
    if not openrouter_key or not serper_key:
        st.error("❌ Please enter OpenRouter and Serper API keys in the sidebar first!")
        st.stop()

    with st.spinner("Analyzing Company Data... Please wait."):
        try:
            # 1. Resolve URL
            is_url = urlparse(query).scheme in ('http', 'https')
            target_url = query if is_url else get_official_website(query, serper_key)
            
            if not target_url:
                st.error("❌ Failed to find website. Check company name or try a direct URL.")
                st.stop()
                
            # 2. Crawl Website
            raw_text = intelligent_crawl(target_url)
            
            if not raw_text or len(raw_text.strip()) < 50:
                st.error("⚠️ Could not extract meaningful content from the website.")
                st.stop()
            
            # 3. AI Analysis
            report_data = analyze_with_openrouter(raw_text, target_url, openrouter_key, selected_model)
            
            if not report_data:
                st.error("❌ AI analysis failed. Check your OpenRouter API key or try again.")
                st.stop()

            # 4. Generate PDF (with error handling that doesn't crash the app)
            pdf_bytes = None
            try:
                pdf_bytes = generate_pdf_report(report_data, target_url)
            except Exception as pdf_err:
                print(f"[ERROR] PDF Generation failed: {type(pdf_err).__name__}: {str(pdf_err)}")

            filename = f"{report_data.get('company_name', 'Report')}.pdf"

            st.write(f"**🌐 Target Website:** {target_url}")
            st.markdown("---")
            
            # TOP-RIGHT DOWNLOAD BUTTON LAYOUT
            header_col, btn_col = st.columns([7, 3])
            
            with header_col:
                st.subheader(f"🏢 {report_data.get('company_name')}")
                
            with btn_col:
                if pdf_bytes and len(pdf_bytes) > 0:
                    st.download_button(
                        label="📥 Download PDF", 
                        data=pdf_bytes, 
                        file_name=filename, 
                        mime="application/pdf",
                        use_container_width=True
                    )
                else:
                    st.info("📄 Info ready below (PDF generation unavailable)")

            # Company summary
            summary = report_data.get('company_summary') or report_data.get('summary')
            if summary and summary != "Not Provided":
                st.markdown("### 📝 Summary")
                st.write(summary)

            st.write(f"**Phone:** {report_data.get('phone')} | **Address:** {report_data.get('address')}")
            
            st.markdown("### 📦 Products/Services")
            st.write(", ".join(report_data.get('products_services', [])))
            
            st.markdown("### ⚠️ Pain Points")
            for p in report_data.get('pain_points', []):
                st.write(f"- {p}")
                
            st.markdown("### ⚔️ Competitors")
            for c in report_data.get('competitors', []):
                st.write(f"- [{c.get('name')}]({c.get('website')})")
            
            # 5. Discord Integration
            if discord_token and discord_channel and pdf_bytes and len(pdf_bytes) > 0:
                st.info("Sending report to Discord...")
                success = send_to_discord(pdf_bytes, filename, app_name, app_email, report_data.get('company_name'), target_url, discord_token, discord_channel)
                if success:
                    st.success("✅ Sent to Discord successfully!")
                else:
                    st.error("❌ Failed to send to Discord. Check your Bot Token/Channel ID.")
                    
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")