import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from .module.youtube import getUrl


class Music(commands.Cog):
    def __init__(self, client):
        option = {
            'format': 'bestaudio/best',
            'noplaylist': True,
        }
        self.client = client
        self.DL = YoutubeDL(option)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is Ready")

    @commands.command(name='유튜브')
    async def _youtube(self, ctx, url):
        data = self.DL.extract_info(url, download=False)
        embed = discord.Embed(
            title=data['title'], url=url, color=discord.Color.purple())
        embed.set_author(name=data['uploader'])
        embed.add_field(name='조회수', value=data['view_count'], inline=True)
        embed.add_field(name='평점', value=data['average_rating'], inline=True)
        embed.add_field(name='좋아요 수', value=data['like_count'], inline=True)
        embed.set_image(url=data['thumbnail'])
        await ctx.send(embed=embed)

    @commands.command(name='음악재생', description='유튜브에서 키워드를 검색해 음악을 재생합니다.')
    async def play_music(self, ctx, *keywords):
        # 봇의 음성 채널 연결이 없으면
        if ctx.voice_client is None:
            # 명령어(ctx) 작성자(author)의 음성채널에 연결 상태(voice)
            if ctx.author.voice:
                # 봇을 명령어 작성자가 연결되어 있는 음성채널에 연결
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(title='오류 발생',
                                      description='음성 채널에 들어간 후 명령어를 사용 해 주세요.', color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError(
                    'Author not connected to a voice channel.')
        # 봇이 음성채널에 연결되어 있고, 재생중이라면
        elif ctx.voice_client.is_playing():
            # 현재 재생중인 음원을 종료
            ctx.voice_client.stop()

        keyword = ' '.join(keywords)
        # Youtube 검색 결과 url 얻어오기
        url = getUrl(keyword)
        # 영상 정보 제공
        await ctx.send(url)
        embed = discord.Embed(
            title='음악 재생', description='음악 재생을 준비하고 있어요. 잠시만 기다려 주세요!', color=discord.Color.red())
        await ctx.send(embed=embed)

        data = self.DL.extract_info(url, download=False)
        link = data['url']
        title = data['title']

        ffmpeg_options = {
            # 비디오를 사용하지 않는다
            'options': '-vn',
            # ffmpeg에서 연결이 끊기는 경우, 재연결을 시도
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }
        player = discord.FFmpegPCMAudio(
            link, **ffmpeg_options, executable='/Users/suehyun/Downloads/ffmpeg')
        ctx.voice_client.play(player)

        embed = discord.Embed(
            title='음악 재생', description=f'{title} 재생을 시작할게요!', color=discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name='음악종료', description='현재 재생 중인 음악을 종료합니다.')
    async def quit_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(
                title='', description='음악 재생을 종료합니다.', color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='일시정지', description='현재 재생 중인 음악을 일시정지합니다.')
    async def pause_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected() and voice.is_playing():
            voice.pause()
            embed = discord.Embed(
                title='', description='음악 재생을 일시정지합니다.', color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.command(name='다시시작', description='일시정지된 음악을 재생합니다.')
    async def resume_music(self, ctx):
        voice = ctx.voice_client
        if voice.is_connected and voice.is_paused():
            voice.resume()
            embed = discord.Embed(
                title='', description='멈춘 부분부터 음악을 재생합니다.', color=discord.Color.blue())
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Music(client))
