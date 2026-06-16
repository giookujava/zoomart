import json
import urllib.request
import time
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8767153160:AAGor3JL1WhGbsIQ-byCaV3VRwmOHl4zqG0")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "1746687858")

ANSWERS = {
    "პრინტერი": """🖨 **პრინტერის პრობლემა:**

1. შეამოწმე USB კაბელი — გამოაერთე და შეაერთე ახლიდან
2. გადატვირთე პრინტერი — გამორთე და 30 წამში ჩართე
3. შეამოწმე კარტრიჯი — გახსენი და ჩადე ახლიდან
4. კომპიუტერი გადატვირთე

❓ მოაგვარე?""",

    "სკანერი": """📷 **სკანერის პრობლემა:**

1. გამოაერთე USB და თავიდან შეართე
2. თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

     "ბარათის წამკითხველი": """💳 **სკანერის პრობლემა:**

1. გამოაერთე USB და თავიდან შეართე
2. თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "ინტერნეტი": """🌐 **ინტერნეტის პრობლემა:**

1. როუტერი გამორთე (შავი ღილაკი)
2. 30 წამი დაელოდე
3. ჩართე ახლიდან
4. 1 წუთი დაელოდე სანამ ჩაირთვება

თუ მაინც არ მუშაობს:
5. შეამოწმე კაბელი — მონიტორის ქვეშ გამოაძრე ინტერნეტის თეთრი კაბელი და თავიდან შეაერთე
6. კომპიუტერი გადატვირთე

❓ მოაგვარე?""",

    "ჩეკის პრინტერი": """📇 **ჩეკის პრინტერის პრობლემა:**

1. დეტალური ჩეკის პრინტერი გამორთე და ჩართე ახლიდან
2. შეამოწმე უკან კაბელი გამოაძრე და შეაერთე თავიდან
3. შეამოწმე დენში გამოაძრე და ჩართე თავიდან
4. თერმული ქაღალდი შეამოწმე — ჩადე სწორად
5. შეამოწმე USB კაბელი - გამოაძრე და შეაერთე თავიდან

❓ მოაგვარე?""",

    "კომპიუტერი": """🖥️ **კომპიუტერის პრობლემა:**

1. გადატვირთე — Start → Restart
2. POS გამორთე და ჩართე ახლიდან
3. გამოაერთე დენიდან და სხვაგან შეაერთე
4. მონიტორის ქვეშ POS ის კაბელი გამოაძრე და თავიდან შეაერთე

❓ მოაგვარე?""",

    "ეკრანი": """🖥 **ეკრანის პრობლემა:**

1. მონიტორის კაბელი შეამოწმე — კომპიუტერთან კარგად არის შეერთებული?
2. მონიტორი გამორთე და ჩართე
3. კომპიუტერი გადატვირთე
4. სხვა კაბელი სცადე თუ გაქვს

❓ მოაგვარე?""",

    "wifi": """📶 **WiFi-ის პრობლემა:**

1. ტელეფონზე ან კომპიუტერზე WiFi გამორთე და ჩართე
2. WiFi-ის პაროლი სწორია?
3. როუტერი გადატვირთე — გამორთე 30 წამი, ჩართე
4. სხვა მოწყობილობა WiFi-ს ხედავს?

❓ მოაგვარე?""",
}

DEFAULT_ANSWER = """🤔 ვერ ვიცანი პრობლემა.

გთხოვ უფრო დეტალურად მომიყევი, ან:"""

user_states = {}

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

def main_keyboard():
    return {
        "keyboard": [
            ["🖨 პრინტერი არ მუშაობს", "🌐 ინტერნეტი არ მუშაობს"],
            ["💳 POS არ მუშაობს", "🖋 კარტრიჯი"],
            ["💻 კომპიუტერი", "📞 ტექნიკოსი"]
        ],
        "resize_keyboard": True
    }

def yes_no_keyboard():
    return {
        "keyboard": [
            ["✅ კი, მოაგვარა!", "❌ არა, ვერ მოაგვარა"],
            ["📞 ტექნიკოსი", "🔄 თავიდან"]
        ],
        "resize_keyboard": True
    }

def notify_admin(name, chat_id, problem):
    msg = (f"🚨 <b>ტექნიკოსი საჭიროა!</b>\n\n"
           f"<b>ფილიალი/მომხმარებელი:</b> {name}\n"
           f"<b>ID:</b> {chat_id}\n"
           f"<b>პრობლემა:</b> {problem}")
    send(ADMIN_CHAT_ID, msg)

def find_answer(text):
    text = text.lower()
    if "პრინტერ" in text and "კარტრიჯ" not in text:
        return ANSWERS["პრინტერი"], "პრინტერი"
    if "კარტრიჯ" in text:
        return ANSWERS["კარტრიჯი"], "კარტრიჯი"
    if "ინტერნეტ" in text or "internet" in text:
        return ANSWERS["ინტერნეტი"], "ინტერნეტი"
    if "pos" in text or "POS" in text or "ქასსა" in text:
        return ANSWERS["pos"], "POS"
    if "კომპიუტერ" in text or "computer" in text:
        return ANSWERS["კომპიუტერი"], "კომპიუტერი"
    if "ეკრან" in text or "მონიტორ" in text:
        return ANSWERS["ეკრანი"], "ეკრანი"
    if "wifi" in text or "wi-fi" in text or "ვაიფაი" in text:
        return ANSWERS["wifi"], "wifi"
    return None, None

def handle(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    name = msg.get("from", {}).get("first_name", "უცნობი")

    # Start
    if text in ["/start", "🔄 თავიდან"]:
        user_states[chat_id] = {}
        send(chat_id,
            f"გამარჯობა {name}! 👋\n\n"
            "მე ვარ <b>ზოოMARTI-ს ასისტენტი</b>.\n"
            "აირჩიე პრობლემა ან მომიყევი რა გაქვს! 🛠",
            keyboard=main_keyboard()
        )
        return

    # Technician request
    if text == "📞 ტექნიკოსი":
        problem = user_states.get(chat_id, {}).get("problem", "უცნობი პრობლემა")
        notify_admin(name, chat_id, problem)
        send(chat_id,
            "✅ <b>ტექნიკოსს ვაცნობებ!</b>\n\nმალე დაგიკავშირდება. 📞",
            keyboard={"keyboard": [["🔄 თავიდან"]], "resize_keyboard": True}
        )
        return

    # Problem solved
    if text == "✅ კი, მოაგვარა!":
        send(chat_id,
            "🎉 კარგია! გაგვიმარჯა!\n\nსხვა პრობლემა თუ გაქვს — მომწერე!",
            keyboard=main_keyboard()
        )
        return

    # Not solved
    if text == "❌ არა, ვერ მოაგვარა":
        problem = user_states.get(chat_id, {}).get("problem", "უცნობი პრობლემა")
        notify_admin(name, chat_id, problem)
        send(chat_id,
            "⚠️ გასაგებია! <b>ტექნიკოსს ვაცნობებ</b> — მალე დაგიკავშირდება! 📞",
            keyboard={"keyboard": [["🔄 თავიდან"]], "resize_keyboard": True}
        )
        return

    # Find answer
    answer, problem_type = find_answer(text)

    if answer:
        user_states[chat_id] = {"problem": problem_type}
        send(chat_id, answer, keyboard=yes_no_keyboard())
    else:
        user_states[chat_id] = {"problem": text}
        send(chat_id,
            DEFAULT_ANSWER,
            keyboard={
                "keyboard": [
                    ["🖨 პრინტერი არ მუშაობს", "🌐 ინტერნეტი არ მუშაობს"],
                    ["💳 POS არ მუშაობს", "🖋 კარტრიჯი"],
                    ["💻 კომპიუტერი", "📞 ტექნიკოსი"]
                ],
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
