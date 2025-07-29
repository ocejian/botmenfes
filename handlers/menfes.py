from pyrogram import filters
from pyrogram.types import Message
from config import CHANNEL_ID, MODERATION, LOG_CHAT_ID
from database import load_json, save_json
from main import app  # pastikan import app juga
from pyrogram.enums import ParseMode

cooldown_users = set()

@app.on_message(filters.command("menfes") & filters.private)
async def menfes_handler(_, message: Message):
    user_id = message.from_user.id
    user = message.from_user

    if user_id in load_json("blocked_user.json"):
        return await message.reply("⛔️ Kamu diblokir dari mengirim menfes.")

    if user_id in cooldown_users:
        return await message.reply("⌛ Tunggu beberapa saat sebelum kirim lagi.")

    if len(message.command) < 2:
        return await message.reply("Gunakan format: /menfes isi curhatan")

    text = message.text.split(None, 1)[1]

    # Anti badword
    blacklist = load_json("blacklist.json")
    if any(word.lower() in text.lower() for word in blacklist):
        return await message.reply("⚠️ Menfes mengandung kata yang dilarang.")

    menfes_text = f"💌 Pesan anonim:\n\n{text}"

    cooldown_users.add(user_id)
    app.loop.call_later(60, lambda: cooldown_users.remove(user_id))

    if MODERATION:
        await app.send_message(CHANNEL_ID, f"📝 Review menfes:\n\n{menfes_text}")
        await message.reply("✅ Menfes kamu dikirim untuk ditinjau admin.")
    else:
        await app.send_message(CHANNEL_ID, menfes_text, parse_mode=ParseMode.HTML)
        await message.reply("✅ Menfes kamu berhasil dikirim!")

    # Logging user info ke LOG_CHAT_ID
    log_text = (
        f"📥 <b>Log Menfes Masuk</b>\n"
        f"👤 <b>Nama:</b> {user.first_name}"
        f"\n🔗 <b>Username:</b> @{user.username if user.username else '-'}"
        f"\n🆔 <b>ID:</b> <code>{user.id}</code>"
        f"\n📝 <b>Isi:</b> {text}"
    )
    await app.send_message(LOG_CHAT_ID, log_text, parse_mode=ParseMode.HTML)
