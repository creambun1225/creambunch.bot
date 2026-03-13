import discord
from discord.ext import tasks
import feedparser
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1443792825711071292
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCFVRexFaAfmEKHzHhuWezrQ"

last_video = None

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global last_video

    print("Bot起動！")

    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        last_video = feed.entries[0].id

    check_youtube.start()

@tasks.loop(minutes=1)
async def check_youtube():
    global last_video

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        return

    video = feed.entries[0]

    if video.id != last_video:
        last_video = video.id

        title = video.title
        url = video.link

        channel = client.get_channel(CHANNEL_ID)

        await channel.send(
            f""" youtubeにクリームパンの動画がアップされたよ!!
みんな見てね!!

【{title}】

{url}"""
        )

client.run(TOKEN)