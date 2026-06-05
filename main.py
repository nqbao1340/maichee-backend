import os
import json
import resend
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()
resend.api_key = os.environ.get("RESEND_API_KEY", "")
print(f"API Key loaded: {resend.api_key[:10]}...")

def send_email(to_email, first_name):
    resend.Emails.send({
        "from": "Babychino <onboarding@resend.dev>",
        "to": to_email,
        "subject": f"Chào {first_name}! Cảm ơn bạn đã đăng ký 🎀",
        "html": f"""
        <h2>Heey {first_name}! 👋</h2>
        <p>Cảm ơn bạn đã đăng ký nhận bản tin Babychino!</p>
        <p>Bản tin PDF cá nhân hóa của bạn đang được chuẩn bị và sẽ sớm gửi đến.</p>
        <p><strong>Babychino 🤰</strong></p>
        """
    })

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("=== TALLY DATA ===")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    try:
        fields = {f["label"]: f["value"] for f in data["data"]["fields"]}
        first_name = fields.get("First name", "bạn")
        email = fields.get("Email", "")
        
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
