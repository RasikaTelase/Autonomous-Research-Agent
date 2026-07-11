import requests

def send_to_discord(pdf_bytes, filename, app_name, app_email, comp_name, comp_url, bot_token, channel_id):
    if not bot_token or not channel_id: return False
    
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {"Authorization": f"Bot {bot_token}"}
    
    message_content = (
        f"**New Hackathon Submission**\n"
        f"**Name:** {app_name} | **Email:** {app_email}\n"
        f"**Company:** {comp_name} ({comp_url})"
    )
    
    payload = {"content": message_content}
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    
    try:
        res = requests.post(url, headers=headers, data=payload, files=files)
        return res.status_code in [200, 201]
    except:
        return False