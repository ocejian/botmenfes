from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from config import CHANNEL_ID, MODERATION, LOG_CHAT_ID
from database import load_json
import asyncio

cooldown_users = set()

def init(app):
    @app.on_message(filters.command("menfes") & filters.private)
    async def menfes_handler(_, message: Message):
        user_id = message.from_user.id
        user = message.from_user

        if user_id in load_json("blocked_user.json"):
            return await message.reply("⛔️ Kamu diblokir dari mengirim menfes.")

        if user_id in cooldown_users:
            return await message.reply("⌛ Tunggu beberapa saat sebelum kirim lagi.")

        if not message.reply_to_message and len(message.command) < 2:
            return await message.reply(
                "Kirim /menfes diikuti curhatan, atau reply ke media dengan /menfes <isi>"
            )

        # Ambil teks dari perintah atau caption reply
        text = ""
        if message.reply_to_message and len(message.command) >= 2:
            text = message.text.split(None, 1)[1]
        elif len(message.command) >= 2:
            text = message.text.split(None, 1)[1]

        # Anti badword
        blacklist = load_json("blacklist.json")
        if any(word.lower() in text.lower() for word in blacklist):
            return await message.reply("⚠️ Menfes mengandung kata yang dilarang.")

        menfes_text = f"💌 #Menfes :\n\n{text}" if text else "💌 #Menfes"

        cooldown_users.add(user_id)
        asyncio.get_event_loop().call_later(5, lambda: cooldown_users.remove(user_id))

        # Validasi peer ID (channel) untuk cegah crash
        try:
            await app.get_chat(CHANNEL_ID)
        except Exception as e:
            return await message.reply("❌ Gagal mengirim: bot belum join channel atau ID salah.")

        try:
            # Jika reply ke media
            if message.reply_to_message and any([
                message.reply_to_message.photo,
                message.reply_to_message.video,
                message.reply_to_message.document,
                message.reply_to_message.audio,
                message.reply_to_message.voice,
                message.reply_to_message.sticker,
            ]):
                media_msg = message.reply_to_message

                await media_msg.copy(
                    CHANNEL_ID,
                    caption=("📝 Review menfes:\n\n" if MODERATION else "") + menfes_text,
                    parse_mode=ParseMode.HTML,
                )
                await message.reply(
                    "✅ Menfes kamu dikirim untuk ditinjau admin." if MODERATION else
                    "✅ Menfes kamu berhasil dikirim!"
                )
            else:
                # Kirim teks biasa
                await app.send_message(
                    CHANNEL_ID,
                    ("📝 Review menfes:\n\n" if MODERATION else "") + menfes_text,
                    parse_mode=ParseMode.HTML
                )
                await message.reply(
                    "✅ Menfes kamu dikirim untuk ditinjau admin." if MODERATION else
                    "✅ Menfes kamu berhasil dikirim!"
                )
        except Exception as e:
            print(f"[ERROR]: {e}")
            return await message.reply("❌ Terjadi kesalahan saat mengirim menfes.")

        # Logging ke grup log
        log_text = (
            f"📥 <b>Log Menfes Masuk</b>\n"
            f"👤 <b>Nama:</b> {user.first_name}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else '-'}\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📝 <b>Isi:</b> {text or '(hanya media)'}"
        )
        try:
            await app.send_message(LOG_CHAT_ID, log_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"[LOG ERROR]: {e}")
