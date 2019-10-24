from datetime import datetime
import asyncio, discord, urllib

from bs4 import BeautifulSoup as bs

async def ctx_print(_str, ctx=None):
    if ctx is not None:
        await ctx.send(_str)
    print(_str)

async def gofundme(url, ctx=None):
    #await ctx_print(f"gofundme: {datetime.now().isoformat()}", ctx)
    html = bs(urllib.request.urlopen(url), features="html.parser")
    donations = []
    clean = []
    name = html.find('h1').text
    progress = ''.join([x.text for x in html.find_all('h2',{'class':'m-progress-meter-heading'})])
    percent = list(progress.split(' ')[i].strip('$') for i in [0, 3])
    percentage = float('%.1f' %(int(percent[0].replace(',','')) / int(percent[1].replace(',','')) * 100))
    author = html.find('div', {'class': 'm-campaign-byline-description'}).text
    for ultag in html.find_all('ul', {'class': 'o-campaign-sidebar-donations'}):
        for litag in ultag.find_all('li'):
            donations.append(litag.text)
    for x in [don.split('\xa0') for don in donations]:
        if len(x) == 3:
            clean.append({"name": x[0], "donation": x[1] + ' ' + x[2]})
    embed = discord.Embed(title=author, color=1359922)
    embed.url = url
    embed.description = "${} / ${}\n**This fundraiser is {}% there!**\n\nRecent contributors".format(percent[0],percent[1],percentage)
    embed.set_image(url="https://cdn.discordapp.com/attachments/589204340019953666/636768886720561182/1FkYANkCKFd4UEsR7cIWKrw.png")
    embed.set_author(name=name, url=url)
    for x in clean[0:6]:
        embed.add_field(name=x["name"], value=x["donation"], inline=True)
    embed.add_field(inline=False, name="Checked at", value=f"{datetime.now().strftime('%H:%M:%S %a %d %b %Y')}")
    await ctx.send(embed=embed)

if __name__ == '__main__':
    asyncio.run(gofundme("https://www.gofundme.com/f/help-ben-finish-college"))
