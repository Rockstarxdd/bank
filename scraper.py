# scraper.py
from pyrogram import Client, filters
from config import API_ID, API_HASH, GROUP_CHAT_ID
import os

app = Client("user_scraper_session", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.private & filters.command("scr"))
async def scrap(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /scr keyword\nExample: /scr bancorp")
        return

    keyword = " ".join(message.command[1:])
    await message.reply_text(f"Scraping messages with keyword: **{keyword}**\nPlease wait...")

    msgs = []
    async for msg in client.iter_history(GROUP_CHAT_ID):
        if msg.text and keyword.lower() in msg.text.lower():
            msgs.append(msg.text)

    if not msgs:
        await message.reply_text(f"No messages found for keyword: **{keyword}**")
        return

    filename = f"{keyword}_scraped.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(msgs))

    await message.reply_document(filename, caption=f"Results for '{keyword}'")
    os.remove(filename)

print("Running userbot...")
app.run()
