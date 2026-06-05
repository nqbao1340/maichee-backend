import smtplib
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

def send_email(to_email, first_name):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    
    msg = MIMEMultipart()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = f"Chào {first_name}! Cảm ơn bạn đã đăng ký 🎀"
    
    body = f"""
Heey {first_name}! 👋

Cảm ơn bạn đã đăng ký nhận bản tin Babychino!

Babychino 🤰
    """
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("=== TALLY DATA ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("==================")
    
    try:
        fields = {f["label"]: f["value"] for f in data["data"]["fields"]}
        print("Fields:", fields)
        
        first_name = fields.get("First name", "bạn")
        email = fields.get("Bạn muốn nhận tài liệu vào email nào", "")
        
        print(f"Name: {first_name}, Email: {email}")
        
        if email:
            send_email(email, first_name)
            print("Email sent!")
            
        return JSONResponse({"status": "ok"})
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)

@app.get("/")
def health():
    return {"status": "Babychino backend is running!"}
