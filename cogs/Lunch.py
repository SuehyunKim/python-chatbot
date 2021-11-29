
from discord.ext import commands
import json
import random


class Lunch(commands.Cog):
    def __init__(self, client):
        self.client = client
        # 데이터 불러오기
        with open("./data/lunch.json", 'r', encoding='utf-8') as f:
            self.lunchDict = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Lunch Cog is Ready")

    @commands.command(name="점심추천", description='[None,한식,중식,일식,양식] 점심 메뉴를 추천받습니다.')
    async def recommend_lunch(self, ctx, arg=None):
        if arg == None:
            # categories : ['한식', '일식', ..]
            categories = list(self.lunchDict.keys())
            category = random.choice(categories)  # category : ex) '한식'
            lunch = random.choice(self.lunchDict[category])  # lunch : ex) 떡볶이
            await ctx.send(f'오늘 점심은 {category}, 그 중에서 {lunch} 어떠세요?')
        else:
            category = arg
            lunch = random.choice(self.lunchDict[category])
            await ctx.send(f'오늘 점심은 {lunch} 어떠세요?')


def setup(client):
    client.add_cog(Lunch(client))
