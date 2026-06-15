# ZooMARTI Telegram Bot

## გაშვება Railway-ზე:

### 1. GitHub-ზე ატვირთე
- შექმენი GitHub ანგარიში: github.com
- ახალი repo შექმენი სახელით "zoomarti-bot"
- ატვირთე ეს ფაილები

### 2. Railway-ზე დააყენე
- გახსენი railway.app
- "New Project" → "Deploy from GitHub"
- აირჩიე "zoomarti-bot" repo

### 3. Environment Variables დაამატე
Railway-ს Settings → Variables-ში დაამატე:
- TELEGRAM_TOKEN = 8767153160:AAGor3JL1WhGbsIQ-byCaV3VRwmOHl4zqG0
- ANTHROPIC_KEY = (შენი Anthropic API key)
- ADMIN_CHAT_ID = (შენი Telegram ID - /start დაწერე @userinfobot-ში)

### 4. Deploy!
Railway ავტომატურად გაუშვებს ბოტს.
