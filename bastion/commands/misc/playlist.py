import re, asyncio

async def build_playlist(self, ctx):
    chan = ctx.bot.config['channel']['muzak']
    print(chan)
    channel = ctx.bot.get_channel()
    print(channel)
    links = ['youtube.com', 'youtu.be']
    videos = []
    messages = await channel.history().flatten()
    for message in messages:
        if any(links in message.content):
            videos.append(re.findall('(http[^\s]+)', message.content))
    print(videos)
    return 'It\'s a work in progress.'
