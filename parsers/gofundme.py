from datetime import datetime
import asyncio, discord, urllib

from bs4 import BeautifulSoup as bs

async def ctx_print(_str, ctx=None):
    if ctx is not None:
        await ctx.send(_str)
    print(_str)

async def gofundme(url, ctx=None):
    #await ctx_print(f"gofundme: {datetime.now().isoformat()}", ctx)
    if url.split(' ')[-1].startswith('https://www.gofundme.com/f/'):
        html = bs(urllib.request.urlopen(url), features="html.parser")
    donations = []
    name = html.find('h1').text
    progress = ''.join([x.text for x in html.find_all('h2',{'class':'m-progress-meter-heading'})])
    percent = list(progress.split(' ')[i].strip('$') for i in [0, 3])
    percentage = float('%.1f' %(int(percent[0].replace(',','')) / int(percent[1].replace(',','')) * 100))
    author = html.find('div', {'class': 'm-campaign-byline-description'}).text
    for ultag in html.find_all('ul', {'class': 'o-campaign-sidebar-donations'}):
        for litag in ultag.find_all('li'):
            donations.append(litag.text)
    clean = {x[0]: x[1] + ' ' + x[2] for x in [don.split('\xa0') for don in donations] if len(x) ==3}
    embed = discord.Embed(title=author, color=1359922)
    embed.url = url
    embed.description = "${} / ${}\n**This fundraiser is {}% there!**\n\nRecent contributors".format(percent[0],percent[1],percentage)
    embed.thumbnail.url = "https://www.gofundme.com/static/media/DefaultAvatar.65712475de0674c9f775ae3b64e7c69f.svg"
    embed.set_author(name=name, url=url)
    for x in list(clean)[0:5]:
        embed.add_field(name=x, value=clean[x], inline=True)
    await ctx.send(embed=embed)

if __name__ == '__main__':
    asyncio.run(gofundme("https://www.gofundme.com/f/help-ben-finish-college"))
