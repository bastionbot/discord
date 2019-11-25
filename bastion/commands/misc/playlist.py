import re, asyncio
from discord.utils import get_channel

def build_playlist():
    config = ConfigParser()
    config.read('/opt/discord/config.ini')
    channel = get_channel(id=config['channel']['muzak'])
    messages = await channel.history().flatten()
    links = ['youtube.com', 'youtu.be']
    videos = []
    for message in messages:
        if any links in message.content:
            videos.append(re.findall('(http[^\s]+)'', message.content))
    print(videos)
    return 'It\'s a work in progress.'
