import smtplib
import os
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

Bản tin PDF cá nhân hóa của bạn đang được chuẩn bị và sẽ sớm gửi đến.

Babychino 🤰
    """
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    try:
        fields = {f["label"]: f["value"] for f in data["data"]["fields"]}
        first_name = fields.get("First name", "bạn")
        email = fields.get("Bạn muốn nhận tài liệu vào email nào", "")
        
        if email:
            send_email(email, first_name)
            
        return JSONResponse({"status": "ok"})
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=500)

@app.get("/")
def health():
    return {"status": "Babychino backend is running!"}
