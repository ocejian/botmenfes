from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def init(app):  # Fungsi ini akan dipanggil di bot.py
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply(
            f"👋 Halo {message.from_user.mention},\nSelamat datang di bot Menfes!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💌 Kirim Menfes", switch_inline_query_current_chat="")],
                [InlineKeyboardButton("👤 Developer", url="https://t.me/ofckelrapillas")],
            ])
        )
