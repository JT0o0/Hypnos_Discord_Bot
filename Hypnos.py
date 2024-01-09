import discord  #discord_api
from discord.ui import Button
from discord.ext import commands

import os
from discord.ui.item import Item  #for acess system storage
from dotenv import load_dotenv
import random as rd

import time # time
from datetime import datetime

import asyncio
import youtube_dl
import spotipy  #spotify_api
from spotipy.oauth2 import SpotifyOAuth  #spotify_api_Oauth

# play-yt cmd
# from help_cog import help_cog
# from music_cog import music_cog

import RPG as rpg

import requests
from bs4 import BeautifulSoup as BS

load_dotenv() #load token
bot_token = os.getenv("BOT_TOKEN")
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify應用程序的客戶端ID和客戶端密鑰
SPOTIFY_CLIENT_ID = spotify_client_id
SPOTIFY_CLIENT_SECRET = spotify_client_secret
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # 在Spotify開發者控制台中設置的重定向URI

#bot_permission
intents = discord.Intents.all()  
intents.voice_states = True
bot = discord.Bot(intents=intents)

# bot.add_cog(help_cog(bot))
# bot.add_cog(music_cog(bot))

voice_clients = {}
ytdl_opts = {'format' : 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(ytdl_opts)

scope = 'user-read-currently-playing user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope)
    )

#------------------------------------------------------------#

http_code = [
    100, 101, 102, 103, 
    200, 201, 202, 203, 204, 206, 207, 
    300, 301, 302, 303, 304, 305, 307, 308, 
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451, 497, 498, 499, 
    500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 530, 599
    ]

@bot.event  #啟動
async def on_ready():
    print(f'Logged in as {bot.user}\nHello, World!')


slcmd = bot.slash_command
btstyle = discord.ButtonStyle
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

#----------------------------TEST-----------------------------# 
@slcmd(name = 'button_test')
async def button_t(bt):
    button1 = Button(label='click me!', style=btstyle.green, emoji='<:Happymention:971746595341209661>')
    button2 = Button(emoji='<:AC:971746595383156777>')
    button3 = Button(label='Danger', style=btstyle.danger)
    button4 = Button(label='Go to Youtube', url='https://www.youtube.com/', style=btstyle.link)
    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    await bt.respond('this is the button testing', view=view)

@slcmd(name = 'latency', description = 'Check the bot\'s latency')
async def ping(ping):
    await ping.respond(f'My ping is `{round((bot.latency)*1000)} ms`.')

@slcmd(name = 'get_id', description = 'get id-s')
async def gid(gid):
    s_ID = gid.guild.id
    c_ID = gid.channel.id
    usr_ID = gid.author.id
    await gid.respond(f'```Server ID: {s_ID}\nChannel ID: {c_ID}\nYour ID: {usr_ID}```')

@slcmd(name = 'hello', description = 'Say hello to you')
async def hello(hello):
    await hello.respond(f'Hello, {hello.author.mention}')

@slcmd(name = "haii", description = "hello but button")
async def hai(hai):
    view = hii()
    await hai.respond("Click it!", view = view)

#----------------------------TEST-----------------------------# 

@slcmd(name = 'divinate', description = '幫你算命 (幹話產生器)')
async def divi(divi):
    view = divin()
    await divi.respond(view = view)

@slcmd(name = 'httpcat', description = 'HTTP-code cats!!! :D')
async def cat(cat):
    httpcats = http_code[rd.randint(0, 70)]
    await cat.respond(f'https://http.cat/{httpcats}')

@slcmd(name = 'getwaifu', description = 'Get random waifu pictures')
async def getwaifu(getwaifu, type: str, category: str):
    r = requests.get(f'https://api.waifu.pics/{type}/{category}')
    res = r.json()
    em = discord.Embed()
    em.set_image(url = res['url'])
    await getwaifu.respond(embed = em)

is_used = True
# add a memo
@slcmd(name = 'write_memo', description = 'Remember, and ready to go')
async def wmem(wmem, tit:str, des:str, mention:str, remind_time:str):
    user = wmem.author
    c_time = time.localtime()
    s_id = wmem.guild.id
    year = c_time.tm_year
    now_day = c_time.tm_yday
    now_sec = c_time.tm_hour*3600 + c_time.tm_min*60 + c_time.tm_sec

    if is_used == False:
        os.makedirs(f'memo/{s_id}')
    
    memo_dir = f"memo/{s_id}/{wmem.author.id}_{year}_{now_day}_{now_sec}.memo"
    with open(memo_dir, 'a', encoding="utf-8") as memo:
        memo.write(f'{tit}\n{des}\n{mention}\n{remind_time}')
    
    embed = discord.Embed(
        title = f'{tit}',
        description = f'{des}',
        colour = 0x00b0f4,
        timestamp = datetime.now()
    )

    embed.add_field(name = "Mention", value = f"{user.mention}", inline=True)
    embed.add_field(name = "Remind Time", value = f"{remind_time}", inline=True)


    embed.set_author(name = 'Memo')
    embed.set_footer(
        text = f'{user.name}',
        icon_url = f'{user.avatar}'
    )

    await wmem.respond(f'紀錄成功!\n**Success to wrtie memo!**')
    await wmem.send(embed=embed)
    await wmem.send(f'File directory:\n```./{memo_dir}```')

@slcmd(name = 'read_memo', description = 'Read the memos in this server.')
async def rmem(rmem):
    await rmem.respond("This feature is still in development!!!")

@slcmd(name = 'random_nhentai', description = 'hmm')
async def rdnh(rdnh):
    await rdnh.respond('[BEWARE](https://nhentai.net/random/)')

@slcmd(name = 'russian_roulette', description = 'Play with your life.')
async def rr(rr):
    global bullet_place
    global roll_cnt
    global pull_cnt
    global shoot_place
    global shot
    bullet_place = 0 # initalize the first place
    roll_cnt = 0
    pull_cnt = 0
    shoot_place = 0
    shot = False

    view = Russian_roulette()
    embed = discord.Embed(
        title = "Russian Roulette",
        description = 'Welcome to Russian Roulette.',
        color = 0x7289da
    )
    embed.add_field(name = 'How 2 Play?', value = 'Click the buttons down below to play.', inline = False)
    await rr.respond(embed = embed, view = view)

# ------------------------------------------------------------ #

class hii(discord.ui.View):
    ui = discord.ui
    style = discord.ButtonStyle

    @ui.button(label = "Click me!!!", style=style.green)
    async def ok(self, button, ok):
        user = ok.user
        msg = f"Hello! {user.mention}"
        await ok.response.send_message(msg)

class divin(discord.ui.View):
    ui = discord.ui
    style = discord.ButtonStyle

    @ui.button(label = "算命 Divinate", style=style.primary)
    async def div(self, button, div):
        user = div.user

        embed = discord.Embed(
            title = "Divination",
            description = f"**{divination()}**",
            color = 0x7289da,
            timestamp = datetime.now()
        )

        embed.set_footer(
            text = f'{user.name}',
            icon_url = f'{user.avatar}'
        )
        await div.response.edit_message(embed = embed)

chamber = [1, 2, 3, 4, 5, 6]
bullet_place = 0 # initalize the first place
roll_cnt = 0
pull_cnt = 0
shoot_place = 0
shot = False
# roll, shoot, end the game
class Russian_roulette(discord.ui.View):
    ui = discord.ui
    style = discord.ButtonStyle
    
    # Roll the cylinder
    @ui.button(label="Roll", style=style.primary)    
    async def roll(self, button, roll):
        user = roll.user
        global roll_cnt
        global bullet_place
        bullet_place = rd.randint(1, 6)
        roll_cnt += 1
        
        embed = discord.Embed(
            title = 'Rolled',
            description = f'The cylinder had been rolled **{roll_cnt}** times.',
            color = 0x00ff00,
            timestamp = datetime.now()
        )
        embed.set_author(name = 'Russian Roulette')
        embed.set_footer(
            text = f'{user.name}',
            icon_url = f'{user.avatar}'
        )
        await roll.response.edit_message(embed = embed)
    
    @ui.button(label = 'Shoot', style = style.danger)
    async def shoot(self, button, shoot):
        user = shoot.user
        global pull_cnt
        global shoot_place
        global shot
        pull_cnt += 1
        shoot_place += 1

        if shoot_place == 6:
            shoot_place = 0

        if bullet_place == chamber[shoot_place-1]:
            shot = True
        else:
            shot = False

        if shot: # == True
            embed = discord.Embed(
                title = f'{user.name} has pulled the trigger',
                description = f'**{user.name} just shot himself/herself.** Game ended.',
                color = 0xff0000,
                timestamp = datetime.now()
            )
            embed.set_author(name = 'Russian Roulette')
            embed.set_footer(
                text = f'{user.name}',
                icon_url = f'{user.avatar}'
            )

            embed.add_field(name = 'The cylinder had been rolled', value = f'**{roll_cnt}** times.', inline = True)
            embed.add_field(name = 'The trigger had been pulled', value = f'**{pull_cnt}** times.', inline = True)

            await shoot.response.edit_message(embed = embed)
            self.value = False
            self.stop()
        else: # == False
            embed = discord.Embed(
                title = f'{user.name} has pulled the trigger',
                description = f'**The bullet didn\'t shoot out.** The revolver had been pulled **{pull_cnt}** times. Game continue.',
                color = 0xffff00,
                timestamp = datetime.now()
            )
            embed.set_author(name = 'Russian Roulette')
            embed.set_footer(
                text = f'{user.name}',
                icon_url = f'{user.avatar}'
            )
            await shoot.response.edit_message(embed = embed)
    
    @ui.button(label = 'End the game', style = style.green)
    async def end(self, button, end):
        user = end.user
        embed = discord.Embed(
                title = f'{user.name} has ended the game.',
                color = 0xff0000,
                timestamp = datetime.now()
            )
        
        embed.set_author(name = 'Russian Roulette')
        embed.set_footer(
            text = f'{user.name}',
            icon_url = f'{user.avatar}'
        )
        embed.add_field(name = 'The cylinder has been rolled', value = f'**{roll_cnt}** times.', inline = True)
        embed.add_field(name = 'The trigger has been pulled', value = f'**{pull_cnt}** times.', inline = True)
        await end.response.edit_message(embed = embed)
        self.value = False
        self.stop()

class change_page(discord.ui.View):
    ui = discord.ui
    style = discord.ButtonStyle
    @ui.button(label = 'prev', style = style.blurple)
    async def prev(self, button, prev):
        embed = discord.Embed()
        
        await prev.response.edit_message(content = '')

def divination(): #算命code
    a=rd.choice(['在這行代碼被寫出來的同時,程序員正在喝咖啡', '刷出「你今天將會爆炸」的機率不到1%', 'hdichdi只是邊緣,才不是社恐', '算了,不想讓你知道','我的RPG模式code中,報錯數高達468個,卻可以正常運行','我的RPG模式code中,高達102059個字元,這僅僅只計算到現在這行','這次算命2.0版本讓程式碼變得更好閱讀,算了你看不到程式碼','這次算命2.0版本把你們最討厭的「打架時記得」系列移除了','1+1=2','33+77=110','你正在讀這行文字','「一大堆人」共有4位管理員','世界末日時會死','在「一大堆人」中,有位管理員吃飯常吃到油蔥根','在「一大堆人」早期,有一個人總是在晚上8點時大喊「大佬登場!」','冷的注音是ㄌㄥˇ','在「一大堆人」中,有位管理員很晚才睡','在「一大堆人」中,有位管理員是最強肝帝'])
    b=rd.choice(['沒寫數學功課,可能會被數學老師罵','很渴,就會想喝水','加入hdichdi所在的語音頻道,他將有高機率會退出','很餓,就會想吃東西','很強,代表你很厲害','刷出「ERROR」並不是程式真的出錯','立可帶用完了,就要換新的','沒交嘉義高中家政課的作業,會發生很可怕的事','讀完這則訊息,就會按下按鈕','讀完這則訊息\n就會讀這行\n再來是這行\n最後會按下按鈕','等5秒再按下按鈕,什麼事都不會發生','分不清\\跟/,我來告訴你,如果斜率>0就是/(正斜線)\n什麼?你不會斜率?你怎麼那個可憐'])
    c=rd.choice(['不要回頭!','散彈槍是最強的!\n by hdichdi','ERROR','我建議你別算命了','再按算命按鈕我就要收你錢了','為什麼不參加每月一次的語音頻道投票?','有時你會刷出一些彩蛋,彩蛋可能被加密過','非常遺憾,這行不是彩蛋','8493849 18.53.15.13.13.5.14.4 afh \n提示:「.」代表是同一個英文單字','不要翻倒水','這裡什麼都沒有','停止你的行為','AI不會毀滅世界','你需要冷靜','雖然這個指令是算命,但其實只是告訴你一堆廢話','遇到困難了嗎?我推薦你去洗個澡轉換心情'])
    d=rd.choice(['去看醫生','先去讀書','別算命了','快點去睡覺','去玩遊戲','去看動漫','去喝水','來玩我的RPG模式','按按鈕按慢一點,不然你可能會錯過一些神奇的東西','休息一下','吃點東西','去聽音樂'])
    e=rd.choice(['安靜!\n它來了','你竟然這樣對我!\n總有一天...\n你會有報應!','你期待看到什麼嗎?\n很遺憾,這裡什麼都沒有','不可以色色!','我要跟老師講!','如果同一個老師上你們兩種不同課,在其中一科要上不完時\n就會出現跟自己借課的情形','我可是偉大預言家','千山鳥飛絕\n凍死沒知覺','哈哈哈哈哈哈哈哈哈哈','我其實是真人,被困在這裡快救我出去!','我猜你早餐吃吐司','我才不相信什麼星座','我想跟你玩猜拳','我比那什麼chatGPT強一萬倍','風真是武士,才不是忍者!','你現在醒著,準吧?','有些地方藏了某個邊緣人的自介','這裡有時會出現一些中二台詞','相信命運\n從來都不是要你放棄等死','你的下一步會是按算命按鈕\n...又或者,你根本沒讀完這行','如果有屁孩出現在「一大堆人」,請盡速通知管理員'])
    f=rd.choice(['吃早餐','吃午餐','吃晚餐','上廁所','喝水','睡覺','用手機','過得更好','起床','吃到油蔥根','走路'])
    number = rd.randint(1,6)
    r =''
    if number == 1:
        r = f'你知道嗎?\n{a}'
    if number == 2:
        r = f'如果你{b}'
    if number == 3:
        r = f'{c}'
    if number == 4:
        r = f'我建議你{d}'
    if number == 5:
        r = f'{e}'
    if number == 6:
        r = f'你明天將會{f}'
    return r


bot.run(bot_token)   # type: ignore