from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID
import os
import asyncio

@app.on_message(filters.command("updatebot") & filters.user(OWNER_ID))
    async def update_bot(_, m: Message):
        msg = await m.reply("🔄 Mengupdate dari GitHub...")
        try:
            os.system("git stash")
            os.system("git pull origin main")
            await msg.edit("✅ Update selesai. Merestart bot...")
            await asyncio.sleep(2)
            os.execvp("python", ["python", "bot.py"])
        except Exception as e:
            await msg.edit(f"❌ Gagal update: {e}")
