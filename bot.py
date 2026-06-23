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

შეამოწმე:
• ქაღალდი დევს თუ არა პრინტერში
• ქაღალდი სწორად არის ჩადებული და გვერდითი დამჭერები მიბჯენილია თუ არა
• შიგნით გაჭედილი ფურცელი ხომ არ არის
• ამოიღე კარტრიჯი და თავიდან ჩადე
• გახსენი და დახურე წინა/ზედა სახურავი
• გამორთე პრინტერი 30 წამით და ხელახლა ჩართე
• პრინტერიდან მომავალი USB კაბელი რითაც შეერთებულია მონიტორში გამოაერთე და შეაერთე თავიდან
• დენის კაბელი გამორთე და სხვა ცარიელ ადგილას გადააერთე
• გადატვირთე პრინტერი — გამორთე და 30 წამში ჩართე
• კომპიუტერი გადატვირთე ამ ყველაფრის მერე ბოლოს

❓ მოაგვარე?""",

    "სკანერი": """📷 სკანერის პრობლემა:

შეამოწმე:
• გამოაერთე USB და თავიდან შეაერთე
• თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "ბარათის წამკითხველი": """💳 ბარათის წამკითხველი:

შეამოწმე:
• გამოაერთე USB და თავიდან შეაერთე
• თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "კარტრიჯი": "KARTRIDJI_SPECIAL",

    "ინტერნეტი": """🌐 ინტერნეტის პრობლემა:

შეამოწმე:
• ცადე თუ უკავშირდები ზოომარტის wifi-ს ტელეფონზე
• როუტერი გადატვირთე (გამოაძრე შავი კაბელი 30 წამი დაელოდე და ჩართე თავიდან)
• შეამოწმე (თეთრი) ინტერნეტის კაბელი მონიტორის ქვეშ გამოაძრე და შეაერთე თავიდან (შეერთების დროს მწვანედ და ყვითლად უნდა ანათებდეს)

❓ მოაგვარე?""",

    "ჩეკის პრინტერი": """📇 დეტალური პრინტერის პრობლემა:

შეამოწმე:
• პრინტერი გამორთე და ჩართე ახლიდან
• შეამოწმე უკან კაბელი — გამოაძრე და შეაერთე თავიდან
• შეამოწმე დენი — გამოაძრე და ჩართე თავიდან
• თერმული ქაღალდი შეამოწმე — ჩადე სწორად და გაასუფთავე შეიძლება მტვერი ედოს
• შეამოწმე USB კაბელი — გამოაძრე და შეაერთე თავიდან

❓ მოაგვარე?""",

    "pos": """🖥 POS-ის პრობლემა:

შეამოწმე:
• მონიტორის ქვეშ POS-ის კაბელი ხომ არ არის გამომძვრალი (გამოაერთე და შეაერთე)
• თუ შუქი ჩაქვრა და ავარიულად გაითიშა კომპიუტერი დენის წყაროდან გამოაერთე და სხვაგან შეაერთე
• შეამოწმე POS-ის კაბელის ბლოკი კაბელი ხომ არ არის გამომძვრალი
• თუ POS-ზე გამოაქ განსხვავებული გამოსახულება და არ ირთვება დაუკავშირდი ტექნიკოს

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

    "მაუსი": """🖱 მაუსი:

შეამოწმე:
• გამოაერთე USB და თავიდან შეაერთე
• თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

❓ მოაგვარე?""",

    "კლავიატურა": """⌨️ კლავიატურა:

შეამოწმე:
• გამოაერთე USB და თავიდან შეაერთე
• თუ კიდევ არ მუშაობს გადააერთე სხვა USB პორტში

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
            ["🖨 პრინტერი", "🌐 ინტერნეტი"],
            ["🖥 POS", "🖋 კარტრიჯის დატუმბვა"],
            ["📷 სკანერი", "💳 ბარათის წამკითხველი"],
            ["📇 ჩეკის პრინტერი", "🖱 მაუსი"],
            ["⌨️ კლავიატურა", "📞 ტექნიკოსი"]
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

FIREBASE_PROJECT = "zoomart-92bc1"
FIREBASE_API_KEY = "AIzaSyB-_jS9QeaNycYLp-km7ZbDJgQ8d__jjiM"

def add_firebase_ticket(branch, problem, description=""):
    """Firebase REST API-ით ticket-ის დამატება zm_tickets კოლექციაში"""
    import time as _time
    url = (f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT}"
           f"/databases/(default)/documents/zm_tickets?key={FIREBASE_API_KEY}")
    now = datetime.now()
    payload = {
        "fields": {
            "branch":      {"stringValue": branch},
            "problem":     {"stringValue": problem},
            "description": {"stringValue": description},
            "status":      {"stringValue": "new"},
            "source":      {"stringValue": "telegram_bot"},
            "created_at":  {"integerValue": str(int(_time.time() * 1000))},
            "timestamp":   {"stringValue": now.strftime("%d/%m/%Y %H:%M")},
        }
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"Firebase error: {e}")
        return False

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
        return ANSWERS["კარტრიჯი"], "კარტრიჯის დატუმბვა"
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
    if "მაუს" in t:
        return ANSWERS["მაუსი"], "მაუსი"
    if "კლავიატურ" in t:
        return ANSWERS["კლავიატურა"], "კლავიატურა"
    return None, None


STAFF_DATA = {"აქსისი": {"manager": "ლაშა", "staff": [{"name": "ელენე ბლიაძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "მონიკა ყალიჩავა", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "მარიამ მოსახლიშვილი", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "საბა ზაზაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ნიკოლოზ ქემაშვილი", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "ბაგები": {"manager": "ლაშა", "staff": [{"name": "მარიამ დეკანოიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ლუკა ჭიალაშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "დოლიძე": {"manager": "ლაშა", "staff": [{"name": "ლიკა ჩადუნელი", "schedule": ["FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ნათია ხაჩიძე", "schedule": ["H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "ვაკე": {"manager": "ლაშა", "staff": [{"name": "ბექა ქურდაძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "მარიამ მენაღარიშვილი", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ეკა ფიფია", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ანა დევნოზაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "ვაჟა": {"manager": "ლაშა", "staff": [{"name": "მარიამ ზაალიშვილი", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ნინო ფარქოსაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ლევან ბარამიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "კარტოზია": {"manager": "ლაშა", "staff": [{"name": "მარიამ ქურდაძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "თემური კაპანაძე", "schedule": ["FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ნიკა ყაჭაშვილი", "schedule": ["FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ნია ხონელიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "თამარა ხუციშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ლისი 1": {"manager": "ლაშა", "staff": [{"name": "გვანცა ჯიმშიტაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "თამარ მაისურაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ნუცუბიძე 1": {"manager": "ლაშა", "staff": [{"name": "ნატო ჯაჯაინიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "თამარ ნამგალაური", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ნუცუბიძე 2": {"manager": "ლაშა", "staff": [{"name": "ილია დარჯანია", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ნინი აფციაური", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "ქუთათელაძე": {"manager": "ლაშა", "staff": [{"name": "მიხეილი ყველაშვილი", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "თინათინ ბოგვერაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ანი ხუჭუა", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ნინი ლაზარაევი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "ყიფშიძე": {"manager": "ლაშა", "staff": [{"name": "თაზო აბესაძე", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ქეთევან გელაშვილი", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "ჯიქია": {"manager": "ლაშა", "staff": [{"name": "ანა ჭალიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ნინი ხაჩიძე", "schedule": ["OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ნინო ქობალია", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "აგლაძე": {"manager": "აკაკი", "staff": [{"name": "ნინი სოზიაშვილი", "schedule": ["FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF"]}, {"name": "კესო გამახარია", "schedule": ["H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "OFF", "OFF"]}]}, "ავჭალა": {"manager": "აკაკი", "staff": [{"name": "გვანცა ზაქრაძე", "schedule": ["OFF", "H.D", "H.D", "H.D", "H.D", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ელენე ჯამელაშვილი", "schedule": ["FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ბელიაშვილი": {"manager": "აკაკი", "staff": [{"name": "ნანა ღაჭავა", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ელენე ბობოხიძე", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "გლდანი": {"manager": "აკაკი", "staff": [{"name": "მარიამ კაიშაური", "schedule": ["OFF", "OFF", "P.L", "P.L", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "P.L", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "სოფო წიკლაური", "schedule": ["FULL", "FULL", "FULL", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "გუდვილი": {"manager": "აკაკი", "staff": [{"name": "ელენე ფიფია", "schedule": ["P.L", "P.L", "P.L", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "თათია ელიავა", "schedule": ["FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "სალომე გოგალაძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ნატალი ბაშარული", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "დადიანი": {"manager": "აკაკი", "staff": [{"name": "ნინი მარგველაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "H.D", "H.D", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "სოფო სუხიტაშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "დიდი დიღომი": {"manager": "აკაკი", "staff": [{"name": "გიორგი გოგილაშვილი", "schedule": ["FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ნია ჩიხლაძე", "schedule": ["OFF", "OFF", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "თავდადებული": {"manager": "აკაკი", "staff": [{"name": "გვანცა ბულაური", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "მარიამ პოპიაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "U.L", "P.L", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "თემქა": {"manager": "აკაკი", "staff": [{"name": "საბა დულუზაური", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "თეკლა ციცქიშვილი", "schedule": ["FULL", "OFF", "OFF", "U.L", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ივერთუბანი": {"manager": "აკაკი", "staff": [{"name": "სალომე ელიკაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ბესო ჭუმბურიძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ლისი 2": {"manager": "აკაკი", "staff": [{"name": "თათული რუსაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "მარიამ ფოლადაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ლიზი ბურძენიძე", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "დიღმის მასივი": {"manager": "აკაკი", "staff": [{"name": "თინათინ ბადალაშვილი", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "P.L", "P.L"]}, {"name": "სალომე ჯოხთაბერიძე", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "ანი ჩოხელი", "schedule": ["OFF", "FULL", "OFF", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "საგურამო": {"manager": "აკაკი", "staff": [{"name": "ანეტა ფუტკარაძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "FULL", "FULL", "P.L", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "თამარი თელია", "schedule": ["FULL", "FULL", "OFF", "OFF", "P.L", "P.L", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "სანზონა": {"manager": "აკაკი", "staff": [{"name": "მარიამ იურისონოვი", "schedule": ["FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "სოფელი დიღომი": {"manager": "აკაკი", "staff": [{"name": "თათა მგელაძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "FULL", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "ანა ქობულაშვილი", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "OFF", "OFF", "OFF", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "OFF", "OFF", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "ვაზისუბანი": {"manager": "ნიკა", "staff": [{"name": "მარი ჩერნიკოვი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF"]}, {"name": "ნათელა თხილაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "P.L", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF"]}, {"name": "გიორგი ფხოველიშვილი", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "ვარკეთილი": {"manager": "ნიკა", "staff": [{"name": "მეგი სამადაშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "თაკო გაფრინდაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "იოსებიძე": {"manager": "ნიკა", "staff": [{"name": "ნუცა ყურაშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "FULL", "FULL", "FULL", "FULL", "OFF", "OFF", "U.L", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF"]}, {"name": "თეკლე გრიგალაშვილი", "schedule": ["OFF", "FULL", "FULL", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "H.D", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "ისანი": {"manager": "ნიკა", "staff": [{"name": "ნათია აბაშიძე", "schedule": ["OFF", "H.D", "H.D", "H.D", "H.D", "H.D", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF"]}, {"name": "თაკო გოგიბერიძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}]}, "კრწანისი": {"manager": "ნიკა", "staff": [{"name": "მათე გობეჯიშვილი", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "გურამ მარგველაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "მოზაიკა": {"manager": "ნიკა", "staff": [{"name": "ანი კობახიძე", "schedule": ["OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L"]}, {"name": "დავით ჭიკაიძე", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL"]}]}, "ონიაშვილი": {"manager": "ნიკა", "staff": [{"name": "ქეთი ნიკოლაშვილი", "schedule": ["OFF", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "ნუცი გელანტია", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "ორთაჭალა": {"manager": "ნიკა", "staff": [{"name": "თამუნა შენგელია", "schedule": ["FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL"]}, {"name": "მზექალა გიგაური", "schedule": ["FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}, {"name": "დავით ჭანტურია", "schedule": ["P.L", "P.L", "P.L", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "სამგორი": {"manager": "ნიკა", "staff": [{"name": "სოფო ზარდიაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ლიკა გირგვლიანი", "schedule": ["OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "სოლოლაკი": {"manager": "ნიკა", "staff": [{"name": "ნესტანი სხულუხია", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ვერიკო ლომიძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}, "შინდისი": {"manager": "ნიკა", "staff": [{"name": "ნინო მელაძე", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "მარიამ დარახველიძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}]}, "წყნეთი": {"manager": "ნიკა", "staff": [{"name": "თამთა პეტრიაშვილი", "schedule": ["OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "OFF", "OFF", "FULL", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL"]}]}, "ბათუმი": {"manager": "ბექა", "staff": [{"name": "გიორგი კოპლატაძე", "schedule": ["FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "დაჩი არძენაძე", "schedule": ["OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}, {"name": "მარიამ ნაკაშიძე", "schedule": ["P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "P.L", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF"]}]}, "ბათუმი 2": {"manager": "ბექა", "staff": [{"name": "ვაკო კვირკველია", "schedule": ["OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL"]}, {"name": "ნინო შენგელია", "schedule": ["FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF", "OFF", "FULL", "FULL", "OFF"]}]}}

def get_ganrigi_today():
    from datetime import datetime
    today = datetime.now()
    day = today.day - 1
    date_str = today.strftime("%d/%m/%Y")
    managers = {"ლაშა": [], "აკაკი": [], "ნიკა": [], "ბექა": []}
    for branch, bdata in STAFF_DATA.items():
        mgr = bdata["manager"]
        working, leave = [], []
        for s in bdata["staff"]:
            status = s["schedule"][day] if day < len(s["schedule"]) else "OFF"
            name = s["name"].strip()
            if status == "FULL":
                working.append(name)
            elif status not in ["OFF", ""]:
                leave.append(f"{name}({status})")
        line = f"  📍 {branch}"
        if working:
            line += f"\n     ✅ {', '.join(working)}"
        if leave:
            line += f"\n     ⚠️ {', '.join(leave)}"
        managers[mgr].append(line)
    colors = {"ლაშა": "🔵", "აკაკი": "🟢", "ნიკა": "🔴", "ბექა": "🟣"}
    text = f"📅 <b>განრიგი — {date_str}</b>\n\n"
    for mgr, branches in managers.items():
        text += f"{colors[mgr]} <b>{mgr}:</b>\n" + "\n".join(branches) + "\n\n"
    return text

def handle(update):
    if "message" not in update:
        return
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")
    name = msg.get("from", {}).get("first_name", "უცნობი")
    state = user_states.get(chat_id, {})

    # Admin commands
    if str(chat_id) == ADMIN_CHAT_ID:
        if text == "/stats":
            send(chat_id, get_stats_text())
            return
        if text == "/ganrigi":
            send(chat_id, get_ganrigi_today())
            return
        if text == "/help":
            send(chat_id,
                "📋 <b>ბრძანებები:</b>\n\n"
                "/ganrigi — დღევანდელი განრიგი\n"
                "/stats — სტატისტიკა\n"
                "/help — დახმარება"
            )
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
    if answer == "KARTRIDJI_SPECIAL":
        # კარტრიჯის დატუმბვა — ticket საიტზე + ადმინს შეტყობინება
        user_states[chat_id]["problem"] = "კარტრიჯის დატუმბვა"
        update_stats(branch, "კარტრიჯის დატუმბვა")
        add_firebase_ticket(branch, "კარტრიჯის დატუმბვა")
        notify_admin(name, chat_id, branch, "კარტრიჯის დატუმბვა")
        send(chat_id,
            f"🖋 <b>კარტრიჯის დატუმბვა</b>\n\n"
            f"შეტყობინება გაიგზავნა ტექნიკოსთან! ✅\n"
            f"ფილიალი: <b>{branch}</b>\n\n"
            f"ტექნიკოსი მოვა კარტრიჯის დასატუმბად.",
            keyboard={"keyboard": [["🔄 თავიდან"]], "resize_keyboard": True}
        )
    elif answer:
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
