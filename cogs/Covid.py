import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Covid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Covid Cog is Ready")

    @commands.command(name="서울코로나", description='서울시 코로나19 정보를 제공합니다.')
    async def covid(self, ctx):
        url = "https://www.seoul.go.kr/coronaV/coronaStatus.do"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.select("div.inner > div.status")

        for item in data:
            new = item.select_one('div.num10 > p.counter').text
            total = item.select_one('div.num1 > p.counter').text
            time = item.select_one('div.status-seoul > h4 > span').text
            on_cure = item.select_one('div.cell7 > div.num8 > p.counter').text
            discharged_new = item.select_one(
                'div.cell5 > div.num11 > p.counter').text
            discharged = item.select_one(
                'div.cell5 > div.num8 > p.counter').text
            deaths = item.select_one('div.num9 > p.counter').text
            embed = discord.Embed(
                title='서울시 코로나19 발생동향', color=discord.Color.dark_blue())
            embed.add_field(name='신규확진자', value=new)
            embed.add_field(name='확진자', value=total)
            embed.add_field(name='치료중', value=on_cure)
            embed.add_field(name='신규퇴원', value=discharged_new)
            embed.add_field(name='퇴원', value=discharged)
            embed.add_field(name='사망', value=deaths)
            embed.add_field(name='기준', value=time, inline=False)
            embed.add_field(
                name='더 많은 정보 확인하기', value="https://www.seoul.go.kr/coronaV/coronaStatus.do", inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Covid(client))
