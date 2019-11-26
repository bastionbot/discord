import re, asyncio
from configparser import ConfigParser

async def build_playlist(self, ctx):
    config = ConfigParser()
    config.read('/opt/discord/config.ini')
    channel = ctx.bot.get_channel(config['channel']['muzak'])
    links = ['youtube.com', 'youtu.be']
    videos = []
    messages = await channel.history().flatten():
    for message in messages:
        if any(links in message.content):
            videos.append(re.findall('(http[^\s]+)', message.content))
    print(videos)
    return 'It\'s a work in progress.'
