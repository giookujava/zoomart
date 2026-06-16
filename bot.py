import json
import urllib.request
import time
import os
from datetime import datetime

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8767153160:AAGor3JL1WhGbsIQ-byCaV3VRwmOHl4zqG0")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "1746687858")

BRANCHES = [
    "აქსისი", "ბაგები", "დოლიძე", "ვაკე", "ვაჟა", "კარტოზია",
    "ლისი 1", "ნუცუბიძე 1", "ნუცუბიძე 2", "ქუთათელაძე", "ყიფშიძე", "ჯიქია",
    "ავჭალა", "ვაზისუბანი", "ვარკეთილი", "ისანი", "კრწანისი", "მოზაიკა",
    "ორთაჭალა", "სოლოლაკი", "აგლაძე", "ბელიაშვილი", "გლდანი", "გუდვილი",
    "დადიანი", "დიდი დიღომი", "დიღმის მასივი", "თავდადებული", "თემქა",
    "ივერთუბანი", "ლისი 2", "საგურამო", "სანზონა", "სოფელი დიღომი",
    "შინდისი", "ბათუმი", "ბათუმი 2", "სამგორი", "იოსებიძე", "ონიაშვილი", "წყნეთი"
]

ANSWERS = {
    "პრინტერი": """🖨 პრინტერის პრობლემა:

1. შეამოწმე USB კაბელი — გამოაერთე და შეაერთე ახლიდან
2. გადატვირთე პრინტერი — გამორთე და 30 წამში ჩართე
3. შეამოწმე კარტრიჯი — გახსენი და ჩადე ახლიდან
4. კომპიუტერი გადატვირთე

❓ მოაგვარე?""",

    "სკანერი": """📷 სკანერის პრობლემა:

1. გამოაერთე USB და თავიდან შეაერთე
2. თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "ბარათის წამკითხველი": """💳 ბარათის წამკითხველის პრობლემა:

1. გამოაერთე USB და თავიდან შეაერთე
2. თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "კარტრიჯი": """🖋 კარტრიჯის პრობლემა:

თუ ბეჭდვა გამქრალია ან ღია ფერისაა:
1. გახსენი პრინტერი
2. კარტრიჯი ამოიღე
3. ქაღალდის პირსახოცით გაწმინდე
4. ჩადე ახლიდან

⚠️ თუ კარტრიჯი ბოლოვდება — ტექნიკოსი უნდა შეცვალოს.

❓ მოაგვარე?""",

    "ინტერნეტი": """🌐 ინტერნეტის პრობლემა:

1. როუტერი გამორთე (შავი ღილაკი)
2. 30 წამი დაელოდე
3. ჩართე ახლიდან
4. 1 წუთი დაელოდე

თუ მაინც არ მუშაობს:
5. შეამოწმე კაბელი — მონიტორის ქვეშ გამოაძრე და თავიდან შეაერთე
6. კომპიუტერი გადატვირთე

❓ მოაგვარე?""",

    "ჩეკის პრინტერი": """📇 ჩეკის პრინტერის პრობლემა:

1. პრინტერი გამორთე და ჩართე ახლიდან
2. შეამოწმე უკან კაბელი — გამოაძრე და შეაერთე თავიდან
3. შეამოწმე დენი — გამოაძრე და ჩართე თავიდან
4. თერმული ქაღალდი შეამოწმე — ჩადე სწორად
5. შეამოწმე USB კაბელი — გამოაძრე და შეაერთე თავიდან

❓ მოაგვარე?""",

    "pos": """💳 POS-ის პრობლემა:

1. POS გამორთე და ჩართე ახლიდან
2. შეამოწმე ინტერნეტი — Wi-Fi ან კაბელი
3. შეამოწმე დამტენი — ბატარეა ხომ არ გათავდა
4. თერმული ქაღალდი შეამოწმე — ჩადე სწორად

❓ მოაგვარე?""",

    "კომპიუტერი": """🖥️ კომპიუტერის პრობლემა:

1. გადატვირთე — Start → Restart
2. POS გამორთე და ჩართე ახლიდან
3. გამოაერთე დენიდან და სხვაგან შეაერთე
4. მონიტორის ქვეშ POS-ის კაბელი გამოაძრე და თავიდან შეაერთე

❓ მოაგვარე?""",

    "ეკრანი": """🖥 ეკრანის პრობლემა:

1. მონიტორის კაბელი შეამოწმე — კარგად არის შეერთებული?
2. მონიტორი გამორთე და ჩართე
3. კომპიუტერი გადატვირთე
4. სხვა კაბელი სცადე თუ გაქვს

❓ მოაგვარე?""",

    "wifi": """📶 WiFi-ის პრობლემა:

1. WiFi გამორთე და ჩართე
2. WiFi-ის პაროლი სწორია?
3. როუტერი გადატვირთე — გამორთე 30 წამი, ჩართე
4. სხვა მოწყობილობა WiFi-ს ხედავს?

❓ მოაგვარე?""",
}

# Statistics storage
stats = {
    "total": 0,
    "solved": 0,
    "escalated": 0,
    "by_branch": {},
    "by_problem": {},
    "today": {}
}

user_states = {}

def tg(method, data):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        res = urllib.request.urlopen(req, timeout=30)
        return json.loads(res.read().decode())
    except Exception as e:
        print(f"TG error: {e}")
        return None

def send(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if keyboard:
        data["reply_markup"] = json.dumps(keyboard, ensure_ascii=False)
    tg("sendMessage", data)

def branch_keyboard():
    keyboard = []
    row = []
    for i, b in enumerate(BRANCHES):
        row.append(b)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return {"keyboard": keyboard, "resize_keyboard": True}

def main_keyboard():
    return {
        "keyboard": [
            ["🖨 პრინტერი არ მუშაობს", "🌐 ინტერნეტი არ მუშაობს"],
            ["💳 POS არ მუშაობს", "🖋 კარტრიჯი"],
            ["📷 სკანერი", "💳 ბარათის წამკითხველი"],
            ["📇 ჩეკის პრინტერი", "💻 კომპიუტერი"],
            ["📞 ტექნიკოსი"]
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

def update_stats(branch, problem, solved=None, escalated=False):
    today = datetime.now().strftime("%Y-%m-%d")
    stats["total"] += 1
    if branch:
        stats["by_branch"][branch] = stats["by_branch"].get(branch, 0) + 1
    if problem:
        stats["by_problem"][problem] = stats["by_problem"].get(problem, 0) + 1
    if today not in stats["today"]:
        stats["today"][today] = {"total": 0, "solved": 0, "escalated": 0}
    stats["today"][today]["total"] += 1
    if solved:
        stats["solved"] += 1
        stats["today"][today]["solved"] += 1
    if escalated:
        stats["escalated"] += 1
        stats["today"][today]["escalated"] += 1

def get_stats_text():
    today = datetime.now().strftime("%Y-%m-%d")
    today_data = stats["today"].get(today, {"total": 0, "solved": 0, "escalated": 0})

    top_branches = sorted(stats["by_branch"].items(), key=lambda x: x[1], reverse=True)[:5]
    top_problems = sorted(stats["by_problem"].items(), key=lambda x: x[1], reverse=True)[:5]

    text = (f"📊 <b>სტატისტიკა</b>\n\n"
            f"<b>დღეს ({today}):</b>\n"
            f"• სულ მიმართვა: {today_data['total']}\n"
            f"• გადაიჭრა: {today_data['solved']}\n"
            f"• ტექნიკოსი: {today_data['escalated']}\n\n"
            f"<b>სულ ყველა დრო:</b>\n"
            f"• სულ: {stats['total']}\n"
            f"• გადაიჭრა: {stats['solved']}\n"
            f"• ტექნიკოსი: {stats['escalated']}\n\n")

    if top_branches:
        text += "<b>🏆 Top ფილიალები:</b>\n"
        for b, c in top_branches:
            text += f"• {b}: {c}\n"
        text += "\n"

    if top_problems:
        text += "<b>🔧 ხშირი პრობლემები:</b>\n"
        for p, c in top_problems:
            text += f"• {p}: {c}\n"

    return text

def notify_admin(name, chat_id, branch, problem):
    msg = (f"🚨 <b>ტექნიკოსი საჭიროა!</b>\n\n"
           f"<b>ფილიალი:</b> {branch}\n"
           f"<b>მომხმარებელი:</b> {name}\n"
           f"<b>პრობლემა:</b> {problem}")
    send(ADMIN_CHAT_ID, msg)

def find_answer(text):
    t = text.lower()
    if "სკანერ" in t:
        return ANSWERS["სკანერი"], "სკანერი"
    if "ბარათ" in t or "წამკითხველ" in t:
        return ANSWERS["ბარათის წამკითხველი"], "ბარათის წამკითხველი"
    if "ჩეკ" in t:
        return ANSWERS["ჩეკის პრინტერი"], "ჩეკის პრინტერი"
    if "პრინტერ" in t and "კარტრიჯ" not in t and "ჩეკ" not in t:
        return ANSWERS["პრინტერი"], "პრინტერი"
    if "კარტრიჯ" in t:
        return ANSWERS["კარტრიჯი"], "კარტრიჯი"
    if "ინტერნეტ" in t or "internet" in t:
        return ANSWERS["ინტერნეტი"], "ინტერნეტი"
    if "pos" in t or "ქასსა" in t:
        return ANSWERS["pos"], "POS"
    if "კომპიუტერ" in t or "computer" in t:
        return ANSWERS["კომპიუტერი"], "კომპიუტერი"
    if "ეკრან" in t or "მონიტორ" in t:
        return ANSWERS["ეკრანი"], "ეკრანი"
    if "wifi" in t or "wi-fi" in t or "ვაიფაი" in t:
        return ANSWERS["wifi"], "wifi"
    return None, None

def handle(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    name = msg.get("from", {}).get("first_name", "უცნობი")
    state = user_states.get(chat_id, {})

    # Admin stats command
    if text == "/stats" and str(chat_id) == ADMIN_CHAT_ID:
        send(chat_id, get_stats_text())
        return

    # Start
    if text in ["/start", "🔄 თავიდან"]:
        user_states[chat_id] = {"step": "branch"}
        send(chat_id,
            f"გამარჯობა {name}! 👋\n\n"
            "მე ვარ <b>ზოომარტის ასისტენტი</b>.\n\n"
            "პირველ რიგში — <b>აირჩიე შენი ფილიალი:</b>",
            keyboard=branch_keyboard()
        )
        return

    # Branch selection
    if state.get("step") == "branch":
        if text in BRANCHES:
            user_states[chat_id] = {"step": "problem", "branch": text}
            send(chat_id,
                f"✅ <b>{text}</b>\n\nახლა აირჩიე პრობლემა ან მომიყევი რა გაქვს! 🛠",
                keyboard=main_keyboard()
            )
        else:
            send(chat_id, "გთხოვ აირჩიე ფილიალი სიიდან! 👇", keyboard=branch_keyboard())
        return

    branch = state.get("branch", "უცნობი")

    # Technician
    if text == "📞 ტექნიკოსი":
        problem = state.get("problem", "უცნობი პრობლემა")
        notify_admin(name, chat_id, branch, problem)
        update_stats(branch, problem, escalated=True)
        send(chat_id,
            f"📞 <b>ტექნიკოსთან დასაკავშირებლად დააჭირე:</b>\n\n"
            f"<a href=\"https://t.me/g20goku\">👨‍🔧 ტექნიკოსი — @g20goku</a>\n\n"
            f"მიუთითე: <b>ფილიალი {branch}</b> და პრობლემა!",
            keyboard={"keyboard": [["🔄 თავიდან"]], "resize_keyboard": True}
        )
        return

    # Solved
    if text == "✅ კი, მოაგვარა!":
        update_stats(branch, state.get("problem"), solved=True)
        send(chat_id,
            "🎉 კარგია! გაგვიმარჯა!\n\nსხვა პრობლემა თუ გაქვს — მომწერე!",
            keyboard=main_keyboard()
        )
        return

    # Not solved
    if text == "❌ არა, ვერ მოაგვარა":
        problem = state.get("problem", "უცნობი პრობლემა")
        notify_admin(name, chat_id, branch, problem)
        update_stats(branch, problem, escalated=True)
        send(chat_id,
            f"⚠️ გასაგებია! პირდაპირ მიწერე ტექნიკოსს:\n\n"
            f"<a href=\"https://t.me/g20goku\">👨‍🔧 ტექნიკოსი — @g20goku</a>\n\n"
            f"მიუთითე: <b>ფილიალი {branch}</b> და პრობლემა!",
            keyboard={"keyboard": [["🔄 თავიდან"]], "resize_keyboard": True}
        )
        return

    # Find answer
    answer, problem_type = find_answer(text)
    if answer:
        user_states[chat_id]["problem"] = problem_type
        update_stats(branch, problem_type)
        send(chat_id, answer, keyboard=yes_no_keyboard())
    else:
        user_states[chat_id]["problem"] = text
        update_stats(branch, text)
        send(chat_id,
            "🤔 ვერ ვიცანი პრობლემა.\n\nგთხოვ აირჩიე ღილაკებიდან:",
            keyboard=main_keyboard()
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
