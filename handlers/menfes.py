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
        else:
            text = ""

        # Anti badword
        blacklist = load_json("blacklist.json")
        if any(word.lower() in text.lower() for word in blacklist):
            return await message.reply("⚠️ Menfes mengandung kata yang dilarang.")

        menfes_text = f"💌 #Menfes:\n\n{text}" if text else "💌 #Pesan Menfes"

        cooldown_users.add(user_id)
        asyncio.get_event_loop().call_later(2, lambda: cooldown_users.remove(user_id))

        # Jika reply ke media
        if message.reply_to_message and (
            message.reply_to_message.photo
            or message.reply_to_message.video
            or message.reply_to_message.document
            or message.reply_to_message.audio
            or message.reply_to_message.voice
            or message.reply_to_message.sticker
        ):
            media_msg = message.reply_to_message

            if MODERATION:
                await media_msg.copy(
                    CHANNEL_ID,
                    caption=f"📝 Review menfes:\n\n{menfes_text}",
                    parse_mode=ParseMode.HTML,
                )
                await message.reply("✅ Menfes kamu dikirim untuk ditinjau admin.")
            else:
                await media_msg.copy(
                    CHANNEL_ID,
                    caption=menfes_text,
                    parse_mode=ParseMode.HTML,
                )
                await message.reply("✅ Menfes kamu berhasil dikirim!")
        else:
            # Hanya teks saja
            if MODERATION:
                await app.send_message(CHANNEL_ID, f"📝 Review menfes:\n\n{menfes_text}")
                await message.reply("✅ Menfes kamu dikirim untuk ditinjau admin.")
            else:
                await app.send_message(CHANNEL_ID, menfes_text, parse_mode=ParseMode.HTML)
                await message.reply("✅ Menfes kamu berhasil dikirim!")

        # Logging ke grup log
        log_text = (
            f"📥 <b>Log Menfes Masuk</b>\n"
            f"👤 <b>Nama:</b> {user.first_name}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else '-'}\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📝 <b>Isi:</b> {text or '(hanya media)'}"
        )
        await app.send_message(LOG_CHAT_ID, log_text, parse_mode=ParseMode.HTML)
