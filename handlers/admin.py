from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID
from database import load_json, save_json

@app.on_message(filters.command("block") & filters.user(OWNER_ID))
    async def block_user(_, m: Message):
        if not m.reply_to_message:
            return await m.reply("Reply pesan user yang ingin diblokir.")
        user_id = m.reply_to_message.from_user.id
        data = load_json("blocked_user.json")
        if user_id not in data:
            data.append(user_id)
            save_json("blocked_user.json", data)
        await m.reply("✅ User diblokir.")

    @app.on_message(filters.command("unblock") & filters.user(OWNER_ID))
    async def unblock_user(_, m: Message):
        if not m.reply_to_message:
            return await m.reply("Reply pesan user yang ingin diunblok.")
        user_id = m.reply_to_message.from_user.id
        data = load_json("blocked_user.json")
        if user_id in data:
            data.remove(user_id)
            save_json("blocked_user.json", data)
        await m.reply("✅ User diunblok.")

    @app.on_message(filters.command("blacklist") & filters.user(OWNER_ID))
    async def add_blacklist(_, m: Message):
        if len(m.command) < 2:
            return await m.reply("Format: /blacklist kata")
        word = m.command[1].lower()
        data = load_json("blacklist.json")
        if word not in data:
            data.append(word)
            save_json("blacklist.json", data)
        await m.reply(f"✅ '{word}' ditambahkan ke blacklist.")

    @app.on_message(filters.command("whitelist") & filters.user(OWNER_ID))
    async def remove_blacklist(_, m: Message):
        if len(m.command) < 2:
            return await m.reply("Format: /whitelist kata")
        word = m.command[1].lower()
        data = load_json("blacklist.json")
        if word in data:
            data.remove(word)
            save_json("blacklist.json", data)
        await m.reply(f"✅ '{word}' dihapus dari blacklist.")
