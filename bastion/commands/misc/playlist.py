import re, asyncio
from configparser import ConfigParser
from discord.ext import commands

async def build_playlist(self):
    config = ConfigParser()
    config.read('/opt/discord/config.ini')
    channel = commands.get_channel(channel_id=config['channel']['muzak'])
    links = ['youtube.com', 'youtu.be']
    videos = []
    async for message in channel.history():
        if any(links in message.content):
            videos.append(re.findall('(http[^\s]+)', message.content))
    print(videos)
    return 'It\'s a work in progress.'
