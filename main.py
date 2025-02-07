from telethon import TelegramClient, events
import openai
import asyncio
import datetime

# Get your API ID & HASH from my.telegram.org
API_ID = "24037900"
API_HASH = "765103bc54bf0e4d6a8322bc1ec6f3fe"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

client = TelegramClient("selfbot", API_ID, API_HASH)

AUTO_DELETE = False
AUTO_REPLY = False
LOGGING = False

openai.api_key = OPENAI_API_KEY

# AI Chatbot
@client.on(events.NewMessage(pattern="\.ai (.+)"))
async def ai_chat(event):
    query = event.pattern_match.group(1)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    await event.reply(response["choices"][0]["message"]["content"])

# Auto-Reply with AI
@client.on(events.NewMessage())
async def auto_reply(event):
    global AUTO_REPLY
    if AUTO_REPLY and event.is_private:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": event.text}]
        )
        await event.reply(response["choices"][0]["message"]["content"])

@client.on(events.NewMessage(pattern="\.autoreply on"))
async def enable_autoreply(event):
    global AUTO_REPLY
    AUTO_REPLY = True
    await event.reply("✅ Auto-Reply enabled!")

@client.on(events.NewMessage(pattern="\.autoreply off"))
async def disable_autoreply(event):
    global AUTO_REPLY
    AUTO_REPLY = False
    await event.reply("❌ Auto-Reply disabled!")

# Auto Delete Messages
@client.on(events.NewMessage())
async def auto_delete(event):
    global AUTO_DELETE
    if AUTO_DELETE:
        await asyncio.sleep(10)  # Deletes message after 10s
        await event.delete()

@client.on(events.NewMessage(pattern="\.autodelete on"))
async def enable_autodelete(event):
    global AUTO_DELETE
    AUTO_DELETE = True
    await event.reply("✅ Auto-Delete enabled!")

@client.on(events.NewMessage(pattern="\.autodelete off"))
async def disable_autodelete(event):
    global AUTO_DELETE
    AUTO_DELETE = False
    await event.reply("❌ Auto-Delete disabled!")

# Message Logging
@client.on(events.NewMessage())
async def log_message(event):
    global LOGGING
    if LOGGING:
        with open("chat_logs.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            file.write(f"{timestamp} {event.sender_id}: {event.text}\n")

@client.on(events.NewMessage(pattern="\.log on"))
async def enable_logging(event):
    global LOGGING
    LOGGING = True
    await event.reply("✅ Logging enabled!")

@client.on(events.NewMessage(pattern="\.log off"))
async def disable_logging(event):
    global LOGGING
    LOGGING = False
    await event.reply("❌ Logging disabled!")

# Start Selfbot
print("✅ Selfbot is running...")
client.start()
client.run_until_disconnected()
