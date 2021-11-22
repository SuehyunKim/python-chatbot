import asyncio
from os import name
import discord
from discord.ext import commands
import csv
import random
import json


class Quiz(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.quizDict = {}
        with open("./data/quiz.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.quizDict[row[0]] = row[1]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quiz Cog is Ready")

    @commands.command(name="퀴즈")
    async def quiz(self, ctx):
        problemList = list(self.quizDict.keys())
        problem = random.choice(problemList)
        answer = self.quizDict[problem]
        embed = discord.Embed(
            title='퀴즈', description=problem, color=discord.Color.blue())
        await ctx.send(embed=embed)

        def checkAnswer(message):
            if message.channel == ctx.channel and answer in message.content:
                name = message.author.display_name
                with open("data/score.json", 'r', encoding='utf-8') as f:
                    scoreDict = json.load(f)
                if name in scoreDict.keys():
                    scoreDict[name] += 1
                else:
                    scoreDict[name] = 1
                with open("data/score.json", 'w', encoding='utf-8') as f:
                    json.dump(scoreDict, f, ensure_ascii=False)
                return True
            else:
                return False
        try:
            message = await self.client.wait_for(
                "message", timeout=10.0, check=checkAnswer)
            name = message.author.display_name
            embed = discord.Embed(
                title='', description=f'{name}님, 정답이에요!', color=discord.Color.green())
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='', description=f'땡! 정답은 {answer}!', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='퀴즈랭킹')
    async def quiz_rank(self, ctx, *, player=None):
        embed = discord.Embed(
            title='전체 퀴즈 랭킹', description='전체 퀴즈 랭킹입니다.\n한 문제를 맞출 때마다 1점이 증가해요!', color=discord.Color.blue())
        with open("data/score.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        sdata = sorted(data.items(), key=lambda x: x[1])
        sdata = list(reversed(sdata))
        people = []
        for i in range(len(sdata)):
            people.append(sdata[i][0])
        # 개인 퀴즈 랭킹
        if player != None:
            rank = people.index(player) + 1
            score = data.get(player)
            embed = discord.Embed(
                title='개인 퀴즈 랭킹', description='개인 퀴즈 랭킹입니다.', color=discord.Color.blue())
            embed.add_field(name=player,
                            value=f'{player}님은 {score}점으로 {rank}등입니다.', inline=False)
        # 전체 퀴즈 랭킹
        else:
            for i in range(len(sdata)):
                embed.add_field(name=f'{i+1}등. {sdata[i][0]}',
                                value=f'점수: {sdata[i][1]}점', inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Quiz(client))
