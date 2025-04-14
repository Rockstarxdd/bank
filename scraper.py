# scraper.py
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_CHAT_ID
import os

app = Client("scraper_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("scr"))
async def scrape_messages(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /scr keyword\nExample: /scr bancorp")
        return

    keyword = " ".join(message.command[1:])

    await message.reply_text(f"Scraping messages with keyword: **{keyword}**\nPlease wait...")

    scraped_msgs = []
    async for msg in client.iter_history(GROUP_CHAT_ID):
        if msg.text and keyword.lower() in msg.text.lower():
            scraped_msgs.append(msg.text)

    if not scraped_msgs:
        await message.reply_text(f"No messages found containing: **{keyword}**")
        return

    filename = f"{keyword}_scraped.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(scraped_msgs))

    await message.reply_document(filename, caption=f"Messages containing '{keyword}'")

    os.remove(filename)

print("Bot started successfully...")
app.run()
