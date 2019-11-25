import re, asyncio
from discord.utils import get_channel

async def build_playlist():
    config = ConfigParser()
    config.read('/opt/discord/config.ini')
    channel = get_channel(id=config['channel']['muzak'])
    links = ['youtube.com', 'youtu.be']
    videos = []
    async for message in channel.history():
        if any(links in message.content):
            videos.append(re.findall('(http[^\s]+)'', message.content))
    print(videos)
    return 'It\'s a work in progress.'
