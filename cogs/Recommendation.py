import discord
from discord.ext import commands
import random
import json
from bs4 import BeautifulSoup
import requests


class Recommendation(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("./data/lunch.json", 'r', encoding='utf-8') as f:
            self.lunchDict = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Recommendation Cog is Ready")

    @commands.command(name='점심맛집추천', description='점심메뉴를 추천받은 뒤, 입력한 위치 근처의 맛집을 추천합니다.')
    async def recommend_restaurant(self, ctx):
        def checkMessage(message):
            return message.author == ctx.author and message.channel == ctx.channel
        while True:
            categories = list(self.lunchDict.keys())
            embed = discord.Embed(
                title='점심 맛집 추천', description=f'{categories} 중에서 하나를 입력해주세요!', color=discord.Color.blue())
            await ctx.send(embed=embed)

            message = await self.client.wait_for('message', check=checkMessage)
            category = message.content

            lunch = random.choice(self.lunchDict[category])
            embed = discord.Embed(
                title='점심추천', description=f'오늘 점심은 {lunch}이(가) 어떠세요? (좋아요/싫어요)', color=discord.Color.blue())
            await ctx.send(embed=embed)

            message = await self.client.wait_for('message', check=checkMessage)
            answer = message.content
            if '좋아요' in answer:
                embed = discord.Embed(
                    title='', description='현재 지역을 입력해주세요. {lunch} 맛집을 찾아드릴게요!', color=discord.Color.blue())
                await ctx.send(embed=embed)
                message = await self.client.wait_for('message', check=checkMessage)
                location = message.content
                keyword = f'{location} {lunch}'
                url = f'https://www.mangoplate.com/search/{keyword}'

                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                data = soup.select(
                    "li.server_render_search_result_item > div.list-restaurant-item")

                if len(data) > 5:
                    limit = 5
                else:
                    limit = len(data)

                for item in data[:limit]:
                    thumbnail = item.select_one('img').get('data-original')
                    link = item.select_one('a').get('href')
                    title = item.select_one('h2.title').text.replace('\n', '')
                    rating = item.select_one('strong.search_point').text
                    category = item.select_one('p.etc').text
                    view = item.select_one('span.view_count').text
                    review = item.select_one('span.review_count').text
                    if rating == '':
                        rating = '0'
                    embed = discord.Embed(
                        title=title, description=category, color=discord.Color.orange())
                    embed.set_thumbnail(url=thumbnail)
                    embed.add_field(name='평점', value=rating)
                    embed.add_field(name='조회수', value=view)
                    embed.add_field(name='리뷰수', value=review)
                    embed.add_field(
                        name='링크', value='https://www.mangoplate.com'+link, inline=False)
                    await ctx.send(embed=embed)
                break

            elif '싫어요' in answer:
                embed = discord.Embed(
                    title='', description=f'다른 음식을 추천 받으시겠어요?(y/n)', color=discord.Color.blue())
                await ctx.send(embed=embed)
                message = await self.client.wait_for('message', check=checkMessage)
                answer = message.content
                if answer == 'y':
                    continue
                elif answer == 'n':
                    embed = discord.Embed(
                        title='', desription='맛집 추천을 종료합니다.', color=discord.Color.blue())
                    await ctx.send(embed=embed)
                    break


def setup(client):
    client.add_cog(Recommendation(client))
