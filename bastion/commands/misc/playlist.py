import re, asyncio

async def build_playlist(self, ctx):
    channel = ctx.bot.get_channel(int(ctx.bot.config['channel']['muzak']))
    links = ['youtube.com', 'youtu.be']
    videos = []
    messages = await channel.history(limit=None).flatten()
    for message in messages:
        if any(link in message.content for link in links):
            videos.append(''.join(re.findall('(http[^\s]+)', message.content)))
    dedup = list(set(videos))
    return 'It\'s a work in progress. {0} links found.'.format(len(dedup))
