from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("start") & filters.private)
async def start_handler(_, message: Message):
    await message.reply(
        f"👋 Halo {message.from_user.mention},\nSelamat datang di bot Menfes!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📮 Kirim Menfes", switch_inline_query_current_chat="")],
            [InlineKeyboardButton("📌 Support", url="https://t.me/ofckelrapillas")],
        ])
    )
