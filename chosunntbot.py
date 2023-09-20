import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import asyncio
import datetime

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
token = 'token'
channel_id = '' #enter your discord channel id
ntlist = []


@bot.event
async def on_ready():
    print('=' * 50)
    print('디스코드 봇 작동')
    print('=' * 50)
    channel = bot.get_channel(channel_id)
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        week = now.weekday()
        if hour >= 9 and hour < 18 and week < 5:
            url = 'https://www3.chosun.ac.kr/chosun/217/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY2hvc3VuJTJGMTE3JTJGYXJ0Y2xMaXN0LmRvJTNG'

            # 공지사항 페이지로 이동
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(2) > a:nth-child(1)").text.strip()
            file = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(6)").text.strip()
            # file = soup.select_one(".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(7) > td:nth-child(6)").text.strip()
            num = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(1)").text.strip()
            author = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(3)").text.strip()
            time = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(4)").text.strip()
            whref = soup.select_one(
                ".type-table > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(6) > td:nth-child(2) > a:nth-child(1)").get(
                'href')

            # 내부로 이동 후 공지사항 내부로 이동
            response = requests.get(f'https://www3.chosun.ac.kr{whref}')
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            # 파일 링크 가져오기
            file_href = soup.find_all('p', attrs={"class": "text"})

            # 제목 리스트에 제목 추가
            ntlist.append(title)

            if len(ntlist) == 1:

                # 디스코드 공지사항 임베드
                embed = discord.Embed(title='조선대학교 공지 알림', description=f'[ No. {num} ]',
                                      timestamp=datetime.datetime.now(), color=0x034EA2)
                embed.add_field(name=f'[ 제목 ] : {title}', value='', inline=False)
                embed.add_field(name=f'[ 작성자 ] : {author}', value='', inline=True)
                embed.add_field(name=f'[ 작성일 ] : {time}', value='', inline=True)
                embed.add_field(name='', value=f'[ 링크 ] : https://www3.chosun.ac.kr{whref}', inline=False)
                count = len(file_href)

                # 첨부파일이 있으면 실행, 아니면 실행하지 않음
                if file == '첨부파일':

                    for i in range(1, count):
                        embed.add_field(name='',
                                        value=f'[ 파일{i} ] : [{file_href[i].a.text.strip()}]( https://www3.chosun.ac.kr{file_href[i].a.get("href")} )',
                                        inline=False)

                    embed.set_footer(text=f'{file}',
                                     icon_url='https://www3.chosun.ac.kr/sites/chosun/images/resource/icon-board-file.png')

                await channel.send(embed=embed)

            elif len(ntlist) == 2:

                # 제목 리스트에서 제목이 중복되면 실행
                if ntlist[0] == ntlist[1]:

                    ntlist.remove(ntlist[0])
                    print('중복된 공지')
                # 제목 리스트에서 요소가 2개일 경우 두 내용이 다르면 실행
                elif ntlist[0] != ntlist[1]:

                    # 디스코드 공지사항 임베드
                    embed = discord.Embed(title='조선대학교 공지 알림', description=f'[ No. {num} ]',
                                          timestamp=datetime.datetime.now(), color=0x034EA2)
                    embed.add_field(name=f'[ 제목 ] : {title}', value='', inline=False)
                    embed.add_field(name=f'[ 작성자 ] : {author}', value='', inline=True)
                    embed.add_field(name=f'[ 작성일 ] : {time}', value='', inline=True)
                    embed.add_field(name='', value=f'[ 링크 ] : https://www3.chosun.ac.kr{whref}', inline=False)

                    # 첨부파일 개수
                    count = len(file_href)

                    # 첨부파일이 있으면 개수만큼 실행
                    if file == '첨부파일':

                        for i in range(1, count):
                            embed.add_field(name='',
                                            value=f'[ 파일 {i} ] : [{file_href[i].a.text.strip()}]( https://www3.chosun.ac.kr{file_href[i].a.get("href")} )',
                                            inline=False)

                        embed.set_footer(text=f'{file}',
                                         icon_url='https://www3.chosun.ac.kr/sites/chosun/images/resource/icon-board-file.png')

                    await channel.send(embed=embed)

                    # 제목 리스트에서 첫번쨰 요소 제거거
                    ntlist.remove(ntlist[0])

            # 1분간 대기
            await asyncio.sleep(300)

        else:

            # 1분간 대기
            await asyncio.sleep(300)


bot.run(token)
