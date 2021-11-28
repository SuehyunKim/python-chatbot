import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Oneday_class(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Oneday_class Cog is Ready")

    @commands.command(name="원데이클래스")
    async def restaurant(self, ctx, *args):
        keyword = ' '.join(args)
        url = f"https://taling.me/Home/Search/?query={keyword}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("div.cont2 > div.cont2_class")

        if len(data) > 6:
            limit = 6
        else:
            limit = len(data)

        for item in data[:limit]:
            image = item.select_one('div.img').get('style')
            url_text = image.split('background-image: url(')[1][:-2]
            title = item.select_one('div.title').text.strip()
            link = item.select_one('a').get('href')
            price = item.select_one('div.price2').text.strip()
            location = item.select_one('div.location').text.strip()
            like = item.select_one('div.d_day').text
            rating = item.select_one('div.star').text.strip()
            if rating == '':
                rating = '0'
            embed = discord.Embed(
                title=title, description=location, color=discord.Color.orange())
            embed.set_thumbnail(url=f'https:{url_text}')
            embed.add_field(name='가격', value=price)
            embed.add_field(name='찜', value=like)
            embed.add_field(name='평점', value=rating)
            embed.add_field(
                name='링크', value='https://taling.me/'+link, inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Oneday_class(client))
