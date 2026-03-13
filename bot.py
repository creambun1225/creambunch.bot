import discord
from discord.ext import tasks
import feedparser
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1443792825711071292
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCFVRexFaAfmEKHzHhuWezrQ"

# Webサーバー（Render用）
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_video = None

@client.event
async def on_ready():
    print("Bot起動！")
    check_youtube.start()

@tasks.loop(minutes=1)
async def check_youtube():
    global last_video

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        return

    video = feed.entries[0]

    if last_video is None:
        last_video = video.id
        return

    if video.id != last_video:
        last_video = video.id

        title = video.title
        url = video.link

        channel = client.get_channel(CHANNEL_ID)

        if channel:
            await channel.send(
                f"""youtubeにクリームパンの動画がアップされたよ!!
みんな見てね!!

【{title}】

{url}"""
            )

keep_alive()
client.run(TOKEN)