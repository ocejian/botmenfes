from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from config import LOG_CHAT_ID  # jika butuh logging

# Fungsi init untuk di-load di bot.py
def init(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        user = message.from_user
        mention = user.mention
        user_info = f"👤 USER: {mention} | 🆔 {user.id} | @{user.username or '-'}"

        try:
            # Kirim foto/video dengan caption dan tombol
            await message.reply_photo(
                photo="https://files.catbox.moe/jh9dok.jpg",  # ganti sesuai kebutuhan (bisa video juga pakai reply_video)
                caption=f"👋 Halo {mention},\nSelamat datang di bot Menfes",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💌 Kirim Menfes", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("👤 Support", url="https://t.me/ofckelrapillas")]
                ])
            )

            # Opsional: Logging ke grup
            if LOG_CHAT_ID:
                await app.send_message(
                    LOG_CHANNEL,
                    f"#START\n\n{user_info}"
                )

        except Exception as e:
            await message.reply(f"⚠️ Terjadi error:\n`{e}`")
