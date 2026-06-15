import os
import json
import urllib.request
import time

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8767153160:AAGor3JL1WhGbsIQ-byCaV3VRwmOHl4zqG0")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AQ.Ab8RN6IlRbDPYqtwV7goOAy9_d4_ao-8O1pf-6EjRxPEOIxv3Q")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "1746687858")

SYSTEM_PROMPT = """შენ ხარ ზოოMARTი-ს (pet shop ქსელი საქართველოში) ტექნიკური დახმარების ასისტენტი.
შენი მიზანია ფილიალების თანამშრომლებს დაეხმარო ტექნიკური პრობლემების გადაჭრაში.

ფილიალებს აქვთ შემდეგი აღჭურვილობა:
- POS აპარატი (Sunmi T2 Mini)
- თერმული პრინტერი (HP Laser MFP 137FNW)
- ლაზერული პრინტერი (HP LaserJet, Canon i-SENSYS)
- USB ადაპტერი და ინტერნეტ როუტერი

ხშირი პრობლემები და გადაწყვეტები:
- პრინტერი არ ბეჭდავს: შეამოწმე USB კაბელი, გადატვირთე პრინტერი, შეამოწმე კარტრიჯი
- ინტერნეტი არ მუშაობს: გადატვირთე როუტერი (10 წამი გამორთე), შეამოწმე კაბელები
- POS არ მუშაობს: გადატვირთე, შეამოწმე დამტენი, შეამოწმე ინტერნეტი
- კარტრიჯი ბოლოვდება: ეს ტექნიკოსმა უნდა შეცვალოს

წესები:
1. პასუხი გასცი მხოლოდ ქართულად
2. მოკლე და მკაფიო ინსტრუქციები, მაქსიმუმ 4 წინადადება
3. თუ პრობლემა ვერ გადაიჭრა — თქვი რომ ტექნიკოსს გამოვაგზავნი
4. არასოდეს გასცე პასუხი სხვა ენაზე"""

user_histories = {}
user_attempts = {}

def tg(method, data):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        res = urllib.request.urlopen(req, timeout=30)
        return json.loads(res.read().decode())
    except Exception as e:
        print(f"TG error: {e}")
        return None

def send(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)
    tg("sendMessage", data)

def notify_admin(text):
    send(ADMIN_CHAT_ID, f"🚨 <b>ტექნიკოსი საჭიროა!</b>\n\n{text}")

def ask_gemini(chat_id, user_msg):
    if chat_id not in user_histories:
        user_histories[chat_id] = []
    if chat_id not in user_attempts:
        user_attempts[chat_id] = 0

    user_histories[chat_id].append({"role": "user", "parts": [{"text": user_msg}]})
    user_attempts[chat_id] += 1

    body = json.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": user_histories[chat_id][-10:]
    }).encode()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    try:
        res = urllib.request.urlopen(req, timeout=30)
        data = json.loads(res.read().decode())
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        user_histories[chat_id].append({"role": "model", "parts": [{"text": reply}]})
        needs_tech = (
            "ტექნიკოსს" in reply or
            "ტექნიკოსი" in reply or
            user_attempts[chat_id] >= 3
        )
        return reply, needs_tech
    except Exception as e:
        print(f"Gemini error: {e}")
        return "კავშირის შეცდომა, ცოტა ხანში სცადე.", False

def main_keyboard():
    return {
        "keyboard": [
            ["🖨 პრინტერი არ მუშაობს", "🌐 ინტერნეტი არ მუშაობს"],
            ["💳 POS არ მუშაობს", "🖋 კარტრიჯი"],
            ["💻 კომპიუტერი", "📞 ტექნიკოსი"]
        ],
        "resize_keyboard": True
    }

def handle(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    name = msg.get("from", {}).get("first_name", "")

    if text == "/start" or text == "🔄 თავიდან":
        user_histories[chat_id] = []
        user_attempts[chat_id] = 0
        send(chat_id,
            f"გამარჯობა {name}! 👋\n\nმე ვარ <b>ზოოMARTI-ს ასისტენტი</b>.\n\n"
            "აირჩიე პრობლემა ღილაკებიდან ან მომიყევი რა გაქვს! 🛠",
            keyboard=main_keyboard()
        )
        return

    if text == "📞 ტექნიკოსი":
        history = "\n".join([
            f"{'👤' if m['role']=='user' else '🤖'}: {m['parts'][0]['text']}"
            for m in user_histories.get(chat_id, [])[-6:]
        ])
        notify_admin(f"<b>ფილიალი/მომხმარებელი:</b> {name} (ID: {chat_id})\n\n<b>საუბარი:</b>\n{history}")
        send(chat_id,
            "✅ <b>ტექნიკოსს ვაცნობებ!</b>\n\nმალე დაგიკავშირდება. 📞",
            keyboard={
                "keyboard": [["🔄 თავიდან"]],
                "resize_keyboard": True
            }
        )
        return

    reply, needs_tech = ask_gemini(chat_id, text)
    send(chat_id, reply)

    if needs_tech:
        history = "\n".join([
            f"{'👤' if m['role']=='user' else '🤖'}: {m['parts'][0]['text']}"
            for m in user_histories.get(chat_id, [])[-6:]
        ])
        notify_admin(
            f"<b>ფილიალი:</b> {name} (ID: {chat_id})\n\n<b>საუბარი:</b>\n{history}"
        )
        send(chat_id,
            "⚠️ ეს პრობლემა <b>ტექნიკოსს</b> სჭირდება.\n\n📞 დააჭირე ღილაკს და ტექნიკოსი მალე დაგიკავშირდება!",
            keyboard={
                "keyboard": [["📞 ტექნიკოსი"], ["🔄 თავიდან"]],
                "resize_keyboard": True
            }
        )

def main():
    print("✅ ZooMARTI ბოტი გაეშვა!")
    last_id = 0
    while True:
        try:
            res = tg("getUpdates", {"offset": last_id + 1, "timeout": 30})
            if res and res.get("ok") and res.get("result"):
                for update in res["result"]:
                    last_id = update["update_id"]
                    handle(update)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
