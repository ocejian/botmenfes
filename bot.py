from pyrogram import Client
from handlers import start, menfes, admin, update
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("menfesbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

start.init(app)
menfes.init(app)
admin.init(app)
update.init(app)

print("[INFO] Bot Menfes berjalan kel💔")
app.run()
