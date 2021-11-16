from discord.ext import commands
import json
import random


class Homework(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("./data/lunch.json", 'r', encoding='utf-8') as f:
            self.lunchDict = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Homework Cog is Ready")

    @commands.command(name="이름")
    async def _user(self, ctx):
        user = ctx.author.display_name
        await ctx.send(f'Logged in as {user}')

    @commands.command(name="점심추천2")
    async def recommend_lunch_2(self, ctx, arg1, arg2):
        categories = [arg1, arg2]
        category = random.choice(categories)
        lunch = random.choice(self.lunchDict[category])
        await ctx.send(f'{arg1}이랑 {arg2}이면.. 오늘 점심은 {lunch} 어떠세요?')


def setup(client):
    client.add_cog(Homework(client))
