from pyrogram import Client, filters
import os
from config import Config
from yt_dlp import YoutubeDL

bot = Client("txtBot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("👋 Send /upload_txt and reply with a .txt file containing video links.")

@bot.on_message(filters.command("upload_txt"))
async def upload_from_txt(_, m):
    if not m.reply_to_message or not m.reply_to_message.document:
        return await m.reply("⚠️ Reply to a .txt file.")

    file_path = await m.reply_to_message.download()
    await m.reply("📥 File downloaded. Starting uploads...")

    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if ":" not in line:
            continue
        try:
            title, url = line.strip().split(":", 1)
            title, url = title.strip(), url.strip()
            await m.reply(f"⬇️ Downloading: **{title}**")

            ydl_opts = {
                'outtmpl': 'video.mp4',
                'format': 'best[height<=480]',
                'quiet': True
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            await m.reply_video("video.mp4", caption=f"🎬 {title}")
            os.remove("video.mp4")

        except Exception as e:
            await m.reply(f"❌ Failed: {title}\n{e}")

    os.remove(file_path)
    await m.reply("✅ All videos sent.")

bot.run()
