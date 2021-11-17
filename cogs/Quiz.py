import asyncio
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
        await ctx.send(problem)

        def checkAnswer(message):
            if message.channel == ctx.channel and answer in message.content:
                return True
            else:
                return False
        try:
            await self.client.wait_for("message", timeout=10.0, check=checkAnswer)
            with open("./data/score.json", 'r', encoding='utf-8') as f:
                self.scoreDict = json.load(f)
            name = ctx.author.display_name
            if self.scoreDict.get(name) == None:
                self.scoreDict[name] = 1
            else:
                self.scoreDict[name] += 1
            with open('./data/score.json', 'w', encoding='utf-8') as f:
                json.dump(self.scoreDict, f, ensure_ascii=False)

            await ctx.send("정답이에요!")
        except asyncio.TimeoutError:
            await ctx.send("땡! 정답은 %s!" % answer)


def setup(client):
    client.add_cog(Quiz(client))
