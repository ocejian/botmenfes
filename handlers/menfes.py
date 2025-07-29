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

        # Ambil teks dari command atau caption media jika reply
        text = ""
        if len(message.command) >= 2:
            text = message.text.split(None, 1)[1]
        elif message.reply_to_message and message.reply_to_message.caption:
            text = message.reply_to_message.caption

        if not text:
            return await message.reply("⚠️ Tidak ada isi menfes. Kirim /menfes <isi> atau reply media.")

        # Cek kata blacklist
        blacklist = load_json("blacklist.json")
        if any(word.lower() in text.lower() for word in blacklist):
            return await message.reply("⚠️ Menfes mengandung kata yang dilarang.")

        # Format menfes
        menfes_text = f"💌 #Menfes :\n\n{text}"

        # Tambahkan cooldown user
        cooldown_users.add(user_id)
        asyncio.get_event_loop().call_later(5, lambda: cooldown_users.remove(user_id))

        # Validasi channel
        try:
            await app.get_chat(CHANNEL_ID)
        except Exception:
            return await message.reply("❌ Bot belum join channel atau ID salah.")

        try:
            # Jika reply ke media, salin media ke channel
            if message.reply_to_message and any([
                message.reply_to_message.photo,
                message.reply_to_message.video,
                message.reply_to_message.document,
                message.reply_to_message.audio,
                message.reply_to_message.voice,
                message.reply_to_message.sticker,
            ]):
                await message.reply_to_message.copy(
                    CHANNEL_ID,
                    caption=("📝 Review menfes:\n\n" if MODERATION else "") + menfes_text,
                    parse_mode=ParseMode.HTML
                )
            else:
                # Jika hanya teks
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

        # Kirim ke log grup
        log_text = (
            f"📥 <b>Log Menfes Masuk</b>\n"
            f"👤 <b>Nama:</b> {user.first_name}\n"
            f"🔗 <b>Username:</b> @{user.username if user.username else '-'}\n"
            f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            f"📝 <b>Isi:</b> {text}"
        )
        try:
            await app.send_message(LOG_CHAT_ID, log_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"[LOG ERROR]: {e}")
