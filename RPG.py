import asyncio
import os
import random as rd
import time
import discord

intents = discord.Intents.all()  
client = discord.Client(intents=intents)

#----------------------------------------------------------------------------#

Select_role=0#來計算抽到的角色編號
total_people=0#用來計算總人數
people_left=0#用來計算剩下的左邊人數
people_right=0#用來計算剩下的右邊人數
left=False#判斷角色屬於左
right=False#判斷角色屬於右  #key是選左或右,值是該角色的編號(最後要把編號取代成角色的)
field_number={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#角色站位
Temporary_number=0#該回合的角色編號
field_Remaining_HP={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩血量(字典)
field_Remaining_SP={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩速度(字典)
field_Remaining_DEF={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩防禦(字典)
field_Remaining_Critical={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩爆擊率(字典)
field_Remaining_Miss={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩迴避率(字典)
field_Remaining_Resistance={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩異常狀態抵抗(字典)
turn_bar={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_回合條(字典)
who_can_action={'左1':False,'左2':False,'左3':False,'右1':False,'右2':False,'右3':False}#佔位_誰能行動(字典)
who_survive={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_是否存活(字典)
true_keys=0#清單,處存可行動的佔位
Whether_to_enable_1v1= False#是否開啟1v1

cause_damage=0#造成傷害
true_keys_length=0#可行動長度
count_one=0#計數一
count_two=0#計數二#存當前被打的角色佔位
count_three=['B766AD','9AFF02']#計數三#用於輸出戰鬥字幕

originally_HP=0#原始血量

player_name={'左1':' ','左2':' ','左3':' ','右1':' ','右2':' ','右3':' '}#玩家名稱(字典)
all_role_sp={1:150,2:80,3:200,4:160,5:90} #所有角色的速度
all_role_hp={1:2500,2:3000,3:300,4:1500,5:3400}#所有角色的HP  #{編號:數值}
all_role_def={1:10,2:30,3:0,4:100,5:60}#所有角色的防禦
all_role_Resistance={1:0,2:0,3:0,4:0,5:0}#所有角色的異常狀態抵抗(字典)
all_role_name={1:'邪惡的粉',2:'色狼',3:'輻佬貳',4:'移動式異世界傳送門',5:'熊老大'}#所有角色的名子(字典)
all_role_Critical={1:0,2:0,3:0,4:0,5:0}#所有角色的爆擊率(字典)
all_role_miss={1:0,2:0,3:80,4:0,5:0} #所有角色的迴避率(字典)

state_damageChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,傷害改變(字典)
state_damageVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,傷害變化(字典)
state_damageMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,傷害倍率(字典)

state_SPChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,速度改變(字典)
state_SPVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,速度變化(字典)
state_SPMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,速度倍率(字典)

state_DEFChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,防禦改變(字典)
state_DEFVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,防禦變化(字典)
state_DEFMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,防禦倍率(字典)

state_Exemption={'左1':[[1,999999,0,0,'不可解除']],'左2':[[1,999999,0,0,'不可解除']],'左3':[[1,999999,0,0,'不可解除']],'右1':[[1,999999,0,0,'不可解除']],'右2':[[1,999999,0,0,'不可解除']],'右3':[[1,999999,0,0,'不可解除']]}#異常狀態,傷害減免(字典)

#暈眩格式{'左1':[[0為不觸發暈眩debug用(1為有觸發),999999(餘剩回合),0,0,'不可解除']]}

state_Dizziness={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,暈眩(字典)
state_noheal={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,無法回血(字典)

state_sustained_damage={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,持續傷害(字典)
state_bleed={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,流血傷害(字典)

state_evilcurse={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,邪惡詛咒(字典)
state_evilstorm={'左1':[0,0],'左2':[0,0],'左3':[0,0],'右1':[0,0],'右2':[0,0],'右3':[0,0]}#異常狀態,邪惡風暴(字典)

state_squelch={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,反擊(字典)

state_Critical={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,爆擊率改變(字典)
state_miss={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,迴避率改變(字典)

bat={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}
bad_people_left=0
bad_people_right=0

p1=''
p2=''
p3=''

now=''

onevone_hp_left=0#1v1時左邊的HP
onevone_def_left=0#1v1時左邊的防禦
onevone_sp_left=0#1v1時左邊的速度
onevone_name_left=0#1v1時左邊的名子
onevone_hp_right=0#1v1時右邊的HP
onevone_def_right=0#1v1時右邊的防禦
onevone_sp_right=0#1v1時右邊的速度
onevone_name_right=0#1v1時右邊的名子

count=lambda a,b,c,d:(a+b)*(1+c+d)#a為初始值b為增加量c為永久改變量d為暫時改變量(a以外記得取max())

#----------------------------------------------------------------------------#

@client.event  #啟動
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global Whether_to_enable_1v1,Select_role,total_people,people_left,people_right,field_number,Temporary_number
    global field_Remaining_HP,field_Remaining_SP,field_Remaining_DEF,all_role_Resistance,all_role_name
    global all_role_Critical,all_role_miss,state_damageChange,state_damageVariety,state_damageMultiple
    global state_SPChange,state_SPVariety,state_SPMultiple,state_DEFChange,state_DEFVariety,state_DEFMultiple
    global state_Exemption,state_Dizziness,state_noheal,state_sustained_damage,state_bleed,state_evilcurse
    global state_evilstorm,state_squelch,state_Critical,state_miss,who_survive
    global p1,p2,p3,now,originally_HP,bad_people_left,bad_people_right

    channel = message.channel
    msg = message.content
    if message.author == client.user:
        return

#----------------------------------------------------------------------------#

    def say_3v3():
        global p1,p2,p3,now,originally_HP,field_Remaining_HP,field_number,all_role_name,player_name
        p3=p2
        p2=p1
        p1=now
        for i in range(1,4):
            if field_Remaining_HP[f"左{i}"]<=0:
                field_Remaining_HP[f"左{i}"]=0
            if field_Remaining_HP[f"右{i}"]<=0:
                field_Remaining_HP[f"右{i}"]=0
            if rd.randint(1,2)==1:
                a=discord.Embed(title="3v3", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}VS.  {player_name["右1"]}的{all_role_name[field_number["右1"]]} \n {player_name["左2"]}的{all_role_name[field_number["左2"]]}VS.{player_name["右2"]}的{all_role_name[field_number["右2"]]}\n {player_name["左3"]}的{all_role_name[field_number["左3"]]}VS.{player_name["右3"]}的{all_role_name[field_number["右3"]]}',color=0x8CEA00)#基本排版
                a.set_author(name=client.user)
                a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
                a.add_field(name=p3, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
                a.add_field(name=all_role_name[field_number["左2"]], value=field_Remaining_HP["左2"], inline=True)
                a.add_field(name=p2, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右2"]], value=field_Remaining_HP["右2"], inline=True)
                a.add_field(name=all_role_name[field_number["左3"]], value=field_Remaining_HP["左3"], inline=True)
                a.add_field(name=p1, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右3"]], value=field_Remaining_HP["右3"], inline=True)
                return a
            else:
                a=discord.Embed(title="3v3", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}VS.  {player_name["右1"]}的{all_role_name[field_number["右1"]]} \n {player_name["左2"]}的{all_role_name[field_number["左2"]]}VS.{player_name["右2"]}的{all_role_name[field_number["右2"]]}\n {player_name["左3"]}的{all_role_name[field_number["左3"]]}VS.{player_name["右3"]}的{all_role_name[field_number["右3"]]}',color=0xB766AD)#基本排版
                a.set_author(name=client.user)
                a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
                a.add_field(name=p3, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
                a.add_field(name=all_role_name[field_number["左2"]], value=field_Remaining_HP["左2"], inline=True)
                a.add_field(name=p2, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右2"]], value=field_Remaining_HP["右2"], inline=True)
                a.add_field(name=all_role_name[field_number["左3"]], value=field_Remaining_HP["左3"], inline=True)
                a.add_field(name=p1, value=">>><<<", inline=True)
                a.add_field(name=all_role_name[field_number["右3"]], value=field_Remaining_HP["右3"], inline=True)
                return a

#----------------------------------------------------------------------------#

    def say_2v2():
        global p1,p2,p3,now,originally_HP,field_Remaining_HP,field_number,all_role_name,player_name
        p3=p2
        p2=p1
        p1=now
        for i in range(1,4):
            if field_Remaining_HP[f"左{i}"]<=0:
                field_Remaining_HP[f"左{i}"]=0
            if field_Remaining_HP[f"右{i}"]<=0:
                field_Remaining_HP[f"右{i}"]=0
        if rd.randint(1,2)==1:
            a=discord.Embed(title="2v2", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}VS.  {player_name["右1"]}的{all_role_name[field_number["右1"]]} \n {player_name["左2"]}的{all_role_name[field_number["左2"]]}VS.{player_name["右2"]}的{all_role_name[field_number["右2"]]}',color=0x8CEA00)#基本排版
            a.set_author(name=client.user)
            a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
            a.add_field(name=p3, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
            a.add_field(name=all_role_name[field_number["左2"]], value=field_Remaining_HP["左2"], inline=True)
            a.add_field(name=p2, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右2"]], value=field_Remaining_HP["右2"], inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p1, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            return a
        else:
            a=discord.Embed(title="2v2", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}VS.  {player_name["右1"]}的{all_role_name[field_number["右1"]]} \n {player_name["左2"]}的{all_role_name[field_number["左2"]]}VS.{player_name["右2"]}的{all_role_name[field_number["右2"]]}',color=0xB766AD)#基本排版
            a.set_author(name=client.user)
            a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
            a.add_field(name=p3, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
            a.add_field(name=all_role_name[field_number["左2"]], value=field_Remaining_HP["左2"], inline=True)
            a.add_field(name=p2, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右2"]], value=field_Remaining_HP["右2"], inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p1, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            return a

#----------------------------------------------------------------------------#

    def say_1v1():
        global p1,p2,p3,now,originally_HP,field_Remaining_HP,field_number,all_role_name,player_name
        p3=p2
        p2=p1
        p1=now
        if field_Remaining_HP["左1"]<=0:
            field_Remaining_HP["左1"]=0
        if field_Remaining_HP["右1"]<=0:
            field_Remaining_HP["右1"]=0
        if rd.randint(1,2)==1:
            a=discord.Embed(title="1v1", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}V.S  {player_name["右1"]}的{all_role_name[field_number["右1"]]}',color=0x8CEA00)#基本排版
            a.set_author(name=client.user)
            a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
            a.add_field(name=p3, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p2, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p1, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            return a
        else:
            a=discord.Embed(title="1v1", description=f'{player_name["左1"]}的{all_role_name[field_number["左1"]]}V.S  {player_name["右1"]}的{all_role_name[field_number["右1"]]}',color=0xB766AD)#基本排版
            a.set_author(name=client.user)
            a.add_field(name=all_role_name[field_number["左1"]], value=field_Remaining_HP["左1"], inline=True)
            a.add_field(name=p3, value=">>><<<", inline=True)
            a.add_field(name=all_role_name[field_number["右1"]], value=field_Remaining_HP["右1"], inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p2, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            a.add_field(name=p1, value=">>><<<", inline=True)
            a.add_field(name="XXXX", value="xxxxx", inline=True)
            return a

#----------------------------------------------------------------------------#

    def allRemake():#(函數)重置數值
        global Whether_to_enable_1v1,Select_role,total_people,people_left,people_right,field_number,Temporary_number
        global field_Remaining_HP,field_Remaining_SP,field_Remaining_DEF,all_role_Resistance,all_role_name
        global all_role_Critical,all_role_miss,state_damageChange,state_damageVariety,state_damageMultiple
        global state_SPChange,state_SPVariety,state_SPMultiple,state_DEFChange,state_DEFVariety,state_DEFMultiple
        global state_Exemption,state_Dizziness,state_noheal,state_sustained_damage,state_bleed,state_evilcurse
        global state_evilstorm,state_squelch,state_Critical,state_miss,turn_bar
        global left,right,field_Remaining_Critical,field_Remaining_Miss,field_Remaining_Resistance
        global who_can_action,who_survive,true_keys,cause_damage,true_keys_length,count_one
        global count_two,player_name,all_role_sp,all_role_hp,all_role_def
        global p1,p2,p3,now,count_three,originally_HP,bad_people_left,bad_people_right
        Select_role=0#來計算抽到的角色編號
        total_people=0#用來計算總人數
        people_left=0#用來計算剩下的左邊人數
        people_right=0#用來計算剩下的右邊人數
        left=False#判斷角色屬於左
        right=False#判斷角色屬於右  #key是選左或右,值是該角色的編號(最後要把編號取代成角色的)
        field_number={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#角色站位
        Temporary_number=0#該回合的角色編號
        field_Remaining_HP={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩血量(字典)
        field_Remaining_SP={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩速度(字典)
        field_Remaining_DEF={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩防禦(字典)
        field_Remaining_Critical={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩爆擊率(字典)
        field_Remaining_Miss={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩迴避率(字典)
        field_Remaining_Resistance={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_餘剩異常狀態抵抗(字典)
        turn_bar={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_回合條(字典)
        who_can_action={'左1':False,'左2':False,'左3':False,'右1':False,'右2':False,'右3':False}#佔位_誰能行動(字典)
        who_survive={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#佔位_是否存活(字典)
        true_keys=0#清單,處存可行動的佔位
        Whether_to_enable_1v1= False#是否開啟1v1

        cause_damage=0#造成傷害
        true_keys_length=0#可行動長度
        count_one=0#計數一
        count_two=0#計數二#存當前被打的角色佔位
        count_three=['B766AD','9AFF02']#計數三#用於輸出戰鬥字幕
        originally_HP=0#原始血量

        player_name={'左1':' ','左2':' ','左3':' ','右1':' ','右2':' ','右3':' '}#玩家名稱(字典)
        all_role_sp={1:150,2:80,3:200,4:160,5:90} #所有角色的速度
        all_role_hp={1:2500,2:3000,3:300,4:1500,5:3400}#所有角色的HP  #{編號:數值}
        all_role_def={1:10,2:30,3:0,4:100,5:60}#所有角色的防禦
        all_role_Resistance={1:0,2:0,3:0,4:0,5:0}#所有角色的異常狀態抵抗(字典)
        all_role_name={1:'邪惡的粉',2:'色狼',3:'輻佬貳',4:'移動式異世界傳送門',5:'熊老大'}#所有角色的名子(字典)
        all_role_Critical={1:0,2:0,3:0,4:0,5:0}#所有角色的爆擊率(字典)
        all_role_miss={1:0,2:0,3:80,4:0,5:0} #所有角色的迴避率(字典)

        state_damageChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,傷害改變(字典)
        state_damageVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,傷害變化(字典)
        state_damageMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,傷害倍率(字典)

        state_SPChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,速度改變(字典)
        state_SPVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,速度變化(字典)
        state_SPMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,速度倍率(字典)

        state_DEFChange={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,防禦改變(字典)
        state_DEFVariety={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,防禦變化(字典)
        state_DEFMultiple={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,防禦倍率(字典)

        state_Exemption={'左1':[[1,999999,0,0,'不可解除']],'左2':[[1,999999,0,0,'不可解除']],'左3':[[1,999999,0,0,'不可解除']],'右1':[[1,999999,0,0,'不可解除']],'右2':[[1,999999,0,0,'不可解除']],'右3':[[1,999999,0,0,'不可解除']]}#異常狀態,傷害減免(字典)

        #暈眩格式{'左1':[[0為不觸發暈眩debug用(1為有觸發),999999(餘剩回合),0,0,'不可解除']]}

        state_Dizziness={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,暈眩(字典)
        state_noheal={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,無法回血(字典)

        state_sustained_damage={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,持續傷害(字典)
        state_bleed={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,流血傷害(字典)

        state_evilcurse={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}#異常狀態,邪惡詛咒(字典)
        state_evilstorm={'左1':[0,0],'左2':[0,0],'左3':[0,0],'右1':[0,0],'右2':[0,0],'右3':[0,0]}#異常狀態,邪惡風暴(字典)

        state_squelch={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,反擊(字典)

        state_Critical={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,爆擊率改變(字典)
        state_miss={'左1':[[0,999999,0,0,'不可解除']],'左2':[[0,999999,0,0,'不可解除']],'左3':[[0,999999,0,0,'不可解除']],'右1':[[0,999999,0,0,'不可解除']],'右2':[[0,999999,0,0,'不可解除']],'右3':[[0,999999,0,0,'不可解除']]}#異常狀態,迴避率改變(字典)


        bat={'左1':0,'左2':0,'左3':0,'右1':0,'右2':0,'右3':0}
        bad_people_left=0
        bad_people_right=0
        p1=''
        p2=''
        p3=''

        now=''

        return

#----------------------------------------------------------------------------#

    def embed_powder():#邪惡的粉基本數值#NO.1
        user = message.author
        username = user.name
        embed=discord.Embed(title="邪惡的粉",description="相當邪惡的粉，它是什麼？我不知道", color=0xEAC100)
        embed.set_author(name= username,icon_url=user.avatar)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1162951441070162060/1163102113262485585/Pngtreethe_shock_effect_of_white_5434333.png?ex=653e5a41&is=652be541&hm=4a4ccf6090f854efde6b0cb5d964913499c727c889badaac0f990947308e5fd8&")
        embed.add_field(name="HP", value="3000", inline=True)
        embed.add_field(name="DEF", value="10", inline=True)
        embed.add_field(name="Speed", value="150", inline=True)
        embed.add_field(name="1.直接飄到你手上 30%", value="對一名敵人造成30~60傷害", inline=False)
        embed.add_field(name="2.直接飄到你臉上30%", value="對一名敵人造成80~110傷害", inline=False)
        embed.add_field(name="3.直接飄到你身上20%", value="對一名敵人造成150傷害，並給與持續傷害10，效果三回合", inline=False)
        embed.add_field(name="4.你看不到我19%", value="對所有敵人造成150~200傷害", inline=False)
        embed.add_field(name="5.邪惡風暴1%", value="對所有敵人造成敵人最大生命值的7%持續傷害，效果10回合，效果持續時間無法恢復HP（對付公敵時則造成自身最大生命的20%）", inline=False)
        embed.add_field(name="被動技能：怎麼洗不掉！", value="自身攻擊皆可給與「邪惡詛咒」效果，當邪惡詛咒到達20層時，造成500傷害並解除20層邪惡詛咒，造成的傷害無法迴避，抵抗，減免", inline=False)
        embed.set_footer(text="還沒想好這裡要幹嘛")
        return embed

#----------------------------------------------------------------------------#

    def powder_damage():#邪惡的行動函數
        global powder_Skill,people_left,people_right,left,right#下面是取得全屬性
        global onevone_sp_left,onevone_sp_right,onevone_hp_left,onevone_hp_right,onevone_def_left,onevone_def_right
        global state_sustained_damage,state_bleed,state_evilstorm,count_one,true_keys,state_Critical,state_miss
        global state_damageChange,state_damageVariety,state_damageMultiple,state_Exemption,who_survive,all_role_hp
        global field_number,field_Remaining_HP,count_two,now
        print('邪惡的粉回合')
        print(f'請確認當前角色為{count_one}')
        a=[1,2,3,4,5]
        c=Chooseattack()#取得攻擊對象的左右  #得到的是佔位而非編號  #c是要攻擊的人
        print(f'攻擊對象為{c}')
        b=rd.choices(a,weights=(30,30,20,19,1))#選技能
        now+=(' '+str(b[0])+' 技能')
        print(f'用{b}技能')
        field_Remaining_HP[count_one]-=max(state_sustained_damage[count_one])[0]*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:
            who_survive[count_one]=0
            return 'die'
        field_Remaining_HP[count_one]-=bleed()*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:
            who_survive[count_one]=0
            return 'die'
        if state_evilstorm[count_one]==0:
            pass
        else:
            field_Remaining_HP[count_one]-=state_evilstorm[count_one][0]
            if field_Remaining_HP[count_one]<=0:#行動前被持傷打死
                who_survive[count_one]=0
                return 'die'
            else:
                state_evilstorm[count_one][1]-=1
                if state_evilstorm[count_one][1]==0:
                    state_evilstorm[count_one][0]=0
        if max(state_Dizziness[count_one])[0]==1:#被暈眩
            return 

        if b==[1]:#對一名敵人造成30~60傷害 
            harm=rd.randint(30,60)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])

            return {1:harm,2:c,3:100,4:'邪惡詛咒',5:'no',6:'no'}
        if b==[2]:#對一名敵人造成80~110傷害
            harm=rd.randint(80,110)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'邪惡詛咒',5:'no',6:'no'}
        if b==[3]:#對一名敵人造成150傷害，並給與持續傷害10，效果三回合
            harm=150
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'邪惡詛咒',5:['持續傷害',[[10,3,100,100,'可解除']]],6:'no'}
        if b==[4]:#對所有敵人造成150~200傷害
            harm=rd.randint(150,200)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:'all',3:100,4:'邪惡詛咒',5:'no',6:'no'}
        if b==[5]:#對所有敵人造成敵人最大生命值的7%持續傷害，效果10回合，效果持續時間無法恢復HP（對付公敵時則造成自身最大生命的20%）
            if c=='右1'or c=='右2'or c=='右3':
                for k in range(1,4):
                    if field_number[f'右{k}']==0:
                        break
                    state_evilstorm[f'右{k}']=[int(all_role_hp[field_number[f'右{k}']]*0.07),10]
            else:
                for k in range(1,4):
                    if field_number[f'左{k}']==0:
                        break
                state_evilstorm[f'左{k}']=[int(all_role_hp[field_number[f'左{k}']]*0.07),10]
            return {1:0,2:'all',3:100,4:'邪惡風暴',5:['無法回血',[[1,10,100,100,'不可解除']]],6:'no'}

#----------------------------------------------------------------------------#

    def powder_def():#邪惡的粉的防禦函數
        global field_Remaining_HP,field_Remaining_DEF,cause_damage,all_role_miss,state_miss,count_two,now
        global state_Exemption,state_DEFVariety,state_DEFChange,state_DEFMultiple,who_survive,field_number
        global originally_HP
        print('邪惡的粉防禦')
        print(f'count_two={count_two}')
        a=rd.randint(0,100)
        d=field_number[count_two]
        if cause_damage[3]=='無法迴避':
            pass
        elif a<=cause_damage[3]-all_role_miss[d]+max(state_miss[count_two])[0]:#迴避失敗
            pass
        else:#迴避成功
            now+='邪惡的粉靈巧的躲開了'
            print('迴避成功')
            return
        now+='對邪惡的粉造成 '
        ifhavestate() #被給予,非觸發

        b=count(field_Remaining_DEF[count_two],max(state_DEFVariety[count_two])[0],state_DEFChange[count_two],max(state_DEFMultiple[count_two])[0])
        if type(cause_damage[2])==list:
            pass
            if cause_damage[2][0]=='連擊':
                b=b*cause_damage[2][1]
        if cause_damage[1]-b<=0:#b為防禦
            return#無傷害
        else:
            field_Remaining_HP[count_two]-=(cause_damage[1]-b)*max(state_Exemption[count_two])[0]
            now+=str((cause_damage[1]-b)*max(state_Exemption[count_two])[0])
        if field_Remaining_HP[count_two]<=0:
            who_survive[count_two]=0
            print(f'{count_two}死了')
        
        return

#----------------------------------------------------------------------------#

    def embed_colorWolf():#色狼基本數值#NO.2
        user = message.author
        username = user.name
        embed=discord.Embed(title="色狼",description="一隻彩色的狼，不喜歡自己的名字被念出來", color=0xEAC100)
        embed.set_author(name= username,icon_url=user.avatar)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1162951441070162060/1171222432430956544/received_875662917515136.jpg?ex=655be4e4&is=65496fe4&hm=d07460b3b73d6d38bad34a5cd228e0a84add953e2411506b4c7dc1ef810f85e9&')
        embed.add_field(name="HP", value="3200 ", inline=True)
        embed.add_field(name="DEF", value="30", inline=True)
        embed.add_field(name="Speed", value="80", inline=True)
        embed.add_field(name="1.伸出狼爪30%", value="對一名敵人造成60~120傷害，有30%機率造成傷害為5的流血持續傷害，效果3回合", inline=False)
        embed.add_field(name="2.連抓20%", value="以命中率70%攻擊一名敵人5次，每次傷害50，若目標正在流血，則命中率為100%", inline=False)
        embed.add_field(name="3.夾著尾巴逃10%", value="迴避率上升25%，效果4回合", inline=False)
        embed.add_field(name="4.大快朵頤15%", value="對一名敵人造成300傷害，並恢復150HP", inline=False)
        embed.add_field(name="5.誰剛剛叫我名字！15%", value="對一名敵人造成300~400傷害，並造成傷害為5的流血持續傷害，效果3回合", inline=False)
        embed.add_field(name="6.給你點顏色瞧瞧9%", value="對隨機敵人以命中率為80%攻擊10次，每次80傷害", inline=False)
        embed.add_field(name="7.我乃曠野裡獨來獨往的一匹狼1%", value="挑釁全體敵人直到自身敗北，自身獲得全傷害減免50%(只觸發一次)，，並使自身的hp上限+2000，防禦、速度翻倍，之後恢復所有HP", inline=False)
        embed.add_field(name="被動技能：狼若回頭，不是報恩，必為報仇", value="色狼獲得50%的反擊率，反擊傷害為10，自身若被隊友治療，該隊友也可得到相同的恢復量", inline=False)
        embed.set_footer(text="還沒想好這裡要幹嘛")
        return embed

#----------------------------------------------------------------------------#

    def colorWolf_damage():#色狼傷害函數
        global state_bleed,field_Remaining_Miss,true_keys,count_one,field_Remaining_HP
        global all_role_def,all_role_hp,state_miss,state_sustained_damage,state_Exemption,now
        global who_survive,state_damageChange,field_Remaining_SP,field_Remaining_DEF,state_Dizziness
        global state_damageVariety,state_damageMultiple,Temporary_number
        print('色狼回合')
        print(f'請確認當前角色為{count_one}')
        field_Remaining_HP[count_one]-=max(state_sustained_damage[count_one])[0]*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#行動前被持傷打死
            who_survive[count_one]=0
            return 'die'
        field_Remaining_HP[count_one]-=bleed()*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#流血
            who_survive[count_one]=0
            return 'die'
        if state_evilstorm[count_one]==0:
            pass
        else:
            field_Remaining_HP[count_one]-=state_evilstorm[count_one][0]
            if field_Remaining_HP[count_one]<=0:#行動前被邪惡風暴打死
                who_survive[count_one]=0
                return 'die'
            else:
                state_evilstorm[count_one][1]-=1
                if state_evilstorm[count_one][1]==0:
                    state_evilstorm[count_one][0]=0
        if max(state_Dizziness[count_one])[0]==1:#被暈眩
            return 
        c=Chooseattack()
        print(f'攻擊對象為{c}')
        a=[1,2,3,4,5,6,7]
        b=rd.choices(a,weights=(30,20,10,15,15,9,1))#取得機率
        now+=(' '+str(b[0])+' 技能')
        print(f'用{b}技能')

        if b==[1]:#對一名敵人造成60~120傷害，有30%機率造成傷害為5的流血持續傷害，效果3回合
            harm=rd.randint(60,120)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:['流血',[[5,3,30,100,'可解除']]],5:'no',6:'no'}
        if b==[2]:#以命中率70%攻擊一名敵人5次，每次傷害50，若目標正在流血，則命中率為100%
            harm=50
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            if min(state_bleed[c])==[0,999999,0,0,'不可解除']:
                return {1:harm,2:['連擊',5,c],3:70,4:'no',5:'no',6:'no'}
            else:
                return {1:harm,2:['連擊',5,c],3:100,4:'no',5:'no',6:'no'}
        if b==[3]:#迴避率上升25%，效果4回合
            state_miss[count_one]+=[[25,4,100,100,'可解除']]
            return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[4]:#對一名敵人造成300傷害，並恢復150HP
            harm=300
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            if max(state_noheal[count_one])[0]!=0:
                pass#無法治療
            else:
                field_Remaining_HP[count_one]+=150
                if field_Remaining_HP[count_one]>=all_role_hp[Temporary_number]:
                    field_Remaining_HP[count_one]=all_role_hp[Temporary_number]
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[5]:#對一名敵人造成300~400傷害，並造成傷害為5的流血持續傷害，效果3回合
            harm=rd.randint(300,400)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:['流血',[[5,3,100,100,'可解除']]],5:'no',6:'no'}
        if b==[6]:#對隨機敵人以命中率為80%攻擊10次，每次80傷害
            harm=80
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:['隨機',10],3:80,4:'no',5:'no',6:'no'}
        if b==[7]:#挑釁全體敵人直到自身敗北，自身獲得全傷害減免50%(只觸發一次)，並使自身的hp上限+2000，防禦、速度翻倍，之後恢復所有HP
            all_role_hp[field_number[count_one]]+=2000
            field_Remaining_DEF[count_one]*=2
            field_Remaining_SP[count_one]*=2
            state_Exemption[count_one]+=[[0.5,99999999,100,100,'不可解除']]
            if max(state_noheal[count_one])[0]!=0:#有錯
                pass#無法治療
            else:
                field_Remaining_HP[count_one]=all_role_hp[field_number[count_one]]
            return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}

#----------------------------------------------------------------------------#

    def colorWolf_def():#色狼的防禦函數
        global field_Remaining_HP,field_Remaining_DEF,cause_damage,all_role_miss,state_miss,count_two
        global state_Exemption,state_DEFVariety,state_DEFChange,state_DEFMultiple,who_survive,field_number
        global true_keys,count_one,now,originally_HP
        print('色狼防禦')
        print(f'count_two={count_two}')
        a=rd.randint(0,100)
        d=field_number[count_two]
        if cause_damage[3]=='無法迴避':
            pass
        elif a<=cause_damage[3]-all_role_miss[d]+max(state_miss[count_two])[0]:#迴避失敗
            pass
        else:#迴避成功
            now+='色狼靈巧的躲開了'
            print('迴避成功')
            return
        now+='對色狼造成 '
        ifhavestate() #被給予,非觸發
        b=count(field_Remaining_DEF[count_two],max(state_DEFVariety[count_two])[0],state_DEFChange[count_two],max(state_DEFMultiple[count_two])[0])
        if type(cause_damage[2])==list:
            pass
            if cause_damage[2][0]=='連擊':
                b=b*cause_damage[2][1]
        if cause_damage[1]-b<=0:#b為防禦
            return#無傷害
        else:
            field_Remaining_HP[count_two]-=(cause_damage[1]-b)*max(state_Exemption[count_two])[0]
            now+=str((cause_damage[1]-b)*max(state_Exemption[count_two])[0])
            if field_Remaining_HP[count_two]<=0:
                who_survive[count_two]=0
                print(f'{count_two}死了')
            elif rd.randint(0,100)<=50:#成功反擊
                field_Remaining_HP[count_one]-=10*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:
            who_survive[count_one]=0
            print(f'{count_one}死了')
        return

#----------------------------------------------------------------------------#

    def embed_flower():#輻佬貳基本數值#NO.3
        user = message.author
        username = user.name
        embed=discord.Embed(title="輻佬貳",description="一朵強大的食人花，看似無威脅卻暗藏玄機", color=0xEAC100)
        embed.set_author(name= username,icon_url=user.avatar)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1162951441070162060/1171386174254882866/received_299531112953323.jpg?ex=655c7d63&is=654a0863&hm=3147c3cc21a16ac282713fece46d46dfe6f8be9b3c7d6e4254830fda347251f9&')
        embed.add_field(name="HP", value="300", inline=True)
        embed.add_field(name="DEF", value="0", inline=True)
        embed.add_field(name="Speed", value="200", inline=True)
        embed.add_field(name="1.毒彈25%", value="對一名敵人造成40~60傷害", inline=False)
        embed.add_field(name="2.一口吞下25%", value="對一名敵人造成150傷害，若目標Speed小於125，造成雙倍傷害", inline=False)
        embed.add_field(name="3.不要小看我25%", value="提升全體隊友爆擊率20%，效果2回合", inline=False)
        embed.add_field(name="4.恐怖到做惡夢24%", value="降低所有敵人速度20，效果2回合，之後，造成170~220傷害", inline=False)
        embed.add_field(name="5.我不吃殭屍1%", value="對一名敵人造成1200傷害，暈眩目標10回合，無法解除", inline=False)
        embed.add_field(name="被動技能：靈活", value="輻佬貳獲得80%迴避率，不會被改變", inline=False)
        embed.set_footer(text="還沒想好這裡要幹嘛")
        return embed

#----------------------------------------------------------------------------#

    def flower_damage():#輻佬貳的傷害函數
        global field_Remaining_SP,state_Critical,state_Dizziness
        global state_SPChange,state_SPVariety,state_SPMultiple,field_Remaining_HP
        global state_sustained_damage,state_Exemption,who_survive,true_keys,count_one,count_two,now
        global state_damageVariety,state_damageMultiple,state_damageChange
        print('輻佬貳回合')
        print(f'請確認當前角色為{count_one}')
        field_Remaining_HP[count_one]-=max(state_sustained_damage[count_one])[0]*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:
            who_survive[count_one]=0
            return 'die'
        field_Remaining_HP[count_one]-=bleed()*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:
            who_survive[count_one]=0
            return 'die'
        if state_evilstorm[count_one]==0:
            pass
        else:
            field_Remaining_HP[count_one]-=state_evilstorm[count_one][0]
            if field_Remaining_HP[count_one]<=0:#行動前被持傷打死
                who_survive[count_one]=0
                return 'die'
            else:
                state_evilstorm[count_one][1]-=1
                if state_evilstorm[count_one][1]==0:
                    state_evilstorm[count_one][0]=0
        if max(state_Dizziness[count_one])[0]==1:#被暈眩
            return
        c=Chooseattack()
        print(f'攻擊對象為{c}')
        a=[1,2,3,4,5]   
        b=rd.choices(a,weights=(25,25,25,24,1))#取得機率
        now+=(' '+str(b[0])+' 技能')
        print(f'用{b}技能')
        d=all_role_hp[field_number[count_one]]

        if b==[1]:#對一名敵人造成40~60傷害
            harm=rd.randint(40,60)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}

        if b==[2]:#對一名敵人造成150傷害，若目標Speed小於125，造成雙倍傷害
            pass
            if (field_Remaining_SP[c]+max(state_SPVariety[c])[0])*(state_SPChange[c]+max(state_SPMultiple[c])[0])<125:
                harm=300
            else:
                harm=150
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[3]:#提升全體隊友爆擊率20%，效果2回合  #全體隊友未處裡
            state_Critical[count_one]+=[[20,2,100,100,'可解除']]
            return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[4]:#降低所有敵人速度20，效果2回合，之後，造成170~220傷害
            harm=rd.randint(170,220)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:'all',3:100,4:['速度降低',[[-20,2,100,100,'可解除']]],5:'no',6:'no'}
        if b==[5]:#對一名敵人造成1200傷害，暈眩目標10回合，無法解除
            harm=1200
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:['暈眩',[[1,10,100,100,'不可解除']]],5:'no',6:'no'}

#----------------------------------------------------------------------------#

    def flower_def():#輻佬貳的防禦函數
        global field_Remaining_HP,field_Remaining_DEF,cause_damage,all_role_miss,state_miss,count_two
        global state_Exemption,state_DEFVariety,state_DEFChange,state_DEFMultiple,who_survive,field_number
        global true_keys,count_one,now,originally_HP
        print('輻佬貳防禦')
        print(f'count_two={count_two}')
        a=rd.randint(0,100)
        d=field_number[count_two]
        if cause_damage[3]=='無法迴避':
            pass
        elif a>=80:#迴避失敗
            pass
        else:#迴避成功
            now+='輻佬貳躲開了'
            print('迴避成功')
            return
        now+='對輻佬貳造成 '
        ifhavestate() #被給予,非觸發

        b=count(field_Remaining_DEF[count_two],max(state_DEFVariety[count_two])[0],state_DEFChange[count_two],max(state_DEFMultiple[count_two])[0])
        if type(cause_damage[2])==list:
            pass
            if cause_damage[2][0]=='連擊':
                b=b*cause_damage[2][1]
        if cause_damage[1]-b<=0:#b為防禦
            return#無傷害
        else:
            field_Remaining_HP[count_two]-=(cause_damage[1]-b)*max(state_Exemption[count_two])[0]
            now+=str((cause_damage[1]-b)*max(state_Exemption[count_two])[0])
        if field_Remaining_HP[count_two]<=0:
            who_survive[count_two]=0
            print(f'{count_two}死了')
        return

#----------------------------------------------------------------------------#

    def embed_car():#移動式異世界傳送門基本數值#NO.4
        user = message.author
        username = user.name
        embed=discord.Embed(title="移動式異世界傳送門",description="據說被卡車撞會被送去異世界", color=0xEAC100)
        embed.set_author(name= username,icon_url=user.avatar)
        embed.add_field(name="HP", value="1500 ", inline=True)
        embed.add_field(name="DEF", value="100", inline=True)
        embed.add_field(name="Speed", value="160", inline=True)
        embed.add_field(name="1.麥可！30%", value="對一名敵人造成80~140傷害", inline=False)
        embed.add_field(name="2.衝撞25%", value="對一名敵人造成160~250傷害", inline=False)
        embed.add_field(name="3.普通轉身20%", value="對一名敵人造成290~330傷害", inline=False)
        embed.add_field(name="4.高級轉身10%", value="對一名敵人造成400~520傷害，本次攻擊+20%爆擊率", inline=False)
        embed.add_field(name="5.油門踩滿14%", value="自身速度+140，持續2回合", inline=False)
        embed.add_field(name="6.強制轉身1%", value="對一名敵人造成6000傷害，無法迴避", inline=False)
        embed.add_field(name="被動技能：鋼鐵猛獸", value="行動一次後獲得傷害減免25%，自身不受減速效果影響", inline=False)
        embed.set_footer(text="還沒想好這裡要幹嘛")
        return embed

#----------------------------------------------------------------------------#

    def car_damage():#移動式異世界傳送門的傷害函數
        global state_bleed,field_Remaining_Miss,true_keys,count_one,field_Remaining_HP
        global all_role_def,all_role_hp,state_miss,state_sustained_damage,state_Exemption
        global who_survive,state_damageChange,field_Remaining_SP,field_Remaining_DEF
        global state_SPVariety,state_Critical,state_damageMultiple,state_damageVariety
        global state_Dizziness,now
        state_Exemption[count_one]+=[[0.25,999999,100,100,'不可解除']]
        field_Remaining_HP[count_one]-=max(state_sustained_damage[count_one])[0]*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#行動前被持傷打死
            who_survive[count_one]=0
            return 'die'
        field_Remaining_HP[count_one]-=bleed()*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#流血
            who_survive[count_one]=0
            return 'die'
        if state_evilstorm[count_one]==0:
            pass
        else:
            field_Remaining_HP[count_one]-=state_evilstorm[count_one][0]
            if field_Remaining_HP[count_one]<=0:#行動前被邪惡風暴打死
                who_survive[count_one]=0
                return 'die'
            else:
                state_evilstorm[count_one][1]-=1
                if state_evilstorm[count_one][1]==0:
                    state_evilstorm[count_one][0]=0
        if max(state_Dizziness[count_one])[0]==1:#被暈眩
            return 
        c=Chooseattack()
        a=[1,2,3,4,5,6]
        b=rd.choices(a,weights=(30,25,20,10,14,1))#取得機率
        now+=(' '+str(b[0])+' 技能')
        if b==[1]:#對一名敵人造成80~140傷害
            harm=rd.randint(80,140)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[2]:#對一名敵人造成160~250傷害
            harm=rd.randint(160,250)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[3]:#對一名敵人造成290~330傷害
            harm=rd.randint(290,330)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[4]:#對一名敵人造成400~520傷害，本次攻擊+20%爆擊率
            harm=rd.randint(400,520)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            state_Critical[count_one]+=[[20,1,100,100,'可解除']]
            return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[5]:#自身速度+140，持續2回合
            state_SPVariety[count_one]+=[[140,2,100,100,'可解除']]
            return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[6]:#對一名敵人造成6000傷害，無法迴避
            harm=6000
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:'無法迴避',4:'no',5:'no',6:'no'}

#----------------------------------------------------------------------------#

    def car_def():#移動式異世界傳送門的防禦函數
        global field_Remaining_HP,field_Remaining_DEF,cause_damage,all_role_miss,state_miss,count_two
        global state_Exemption,state_DEFVariety,state_DEFChange,state_DEFMultiple,who_survive,field_number
        global true_keys,count_one,now,originally_HP
        a=rd.randint(0,100)
        d=field_number[count_two]
        if cause_damage[3]=='無法迴避':
            pass
        elif a<=cause_damage[3]-all_role_miss[d]+max(state_miss[count_two])[0]:#迴避失敗
            pass
        else:#迴避成功
            now+='移動式異世界傳送門靈巧的躲開了'
            print('迴避成功')
            return
        now+='對移動式異世界傳送門造成 '
        ifhavestate() #被給予,非觸發
    
        b=count(field_Remaining_DEF[count_two],max(state_DEFVariety[count_two])[0],state_DEFChange[count_two],max(state_DEFMultiple[count_two])[0])
        if type(cause_damage[2])==list:
            pass
        if cause_damage[2][0]=='連擊':
            b=b*cause_damage[2][1]
        if cause_damage[1]-b<=0:#b為防禦
            return#無傷害
        else:
            field_Remaining_HP[count_two]-=(cause_damage[1]-b)*max(state_Exemption[count_two])[0]
            now+=str((cause_damage[1]-b)*max(state_Exemption[count_two])[0])
        if field_Remaining_HP[count_two]<=0:
            who_survive[count_two]=0
            print(f'{count_two}死了')
    
        return

#----------------------------------------------------------------------------#

    def embed_bearboss():#熊老大的基本embed#NO.5
        user = message.author
        username = user.name
        embed=discord.Embed(title="熊老大",description="心地善良,幫助資金困難者\n但千萬不能惹到他否則後果難堪，雖然是做黑幫的\n但跟89不一樣", color=0xEAC100)
        embed.set_author(name= username,icon_url=user.avatar)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1162951441070162060/1191605316605976656/3f29ec98-b792-49a7-8cfd-d2728da99dde.png?ex=65a60bee&is=659396ee&hm=9808b245f1ded2d8cacc84497eaac6b6528e82f61fc65c5cc81300a54d579935&')
        embed.add_field(name="HP", value="3400", inline=True)
        embed.add_field(name="DEF", value="60", inline=True)
        embed.add_field(name="Speed", value="100", inline=True)
        embed.add_field(name="1.重拳/全壘打25%", value="對一名敵人造成80~120傷害，若擁有球棒，擊暈目標1回合", inline=False)
        embed.add_field(name="2.請支援輸贏！25%", value="對一名敵人造成40傷害,每個黑幫小弟使傷害+20%", inline=False)
        embed.add_field(name="3.金錢支援10%", value="恢復隨機隊友30%的HP", inline=False)
        embed.add_field(name="4.武裝•球棒！15%", value="武器從空手變更為球棒，造成的傷害增加20%，若已擁有球棒，還可對全體敵人造成100傷害", inline=False)
        embed.add_field(name="5.不是8+9 24%", value="全體隊友DEF增加100%，持續2回合", inline=False)
        embed.add_field(name="6.別再出現到我面前1%", value="對一名敵人造成3500傷害，無法迴避", inline=False)
        embed.add_field(name="被動技能：黑幫", value="熊老大每次行動有50%可召喚一名黑幫小弟到場上觀摩，黑幫小弟不會被攻擊，黑幫小弟在回合結束後有30%支援，傷害量為15x黑幫小弟人數\n熊老大擁有球棒時免疫一次致命傷害，之後武器變回空手並恢復100HP", inline=False)
        embed.set_footer(text="特別感謝繪師提供靈感")
        return embed

#----------------------------------------------------------------------------#

    def bearboss_damage():#熊老大的傷害函數
        global state_bleed,field_Remaining_Miss,true_keys,count_one,field_Remaining_HP
        global all_role_def,all_role_hp,state_miss,state_sustained_damage,state_Exemption,now
        global who_survive,state_damageChange,field_Remaining_SP,field_Remaining_DEF,state_Dizziness
        global state_SPVariety,state_Critical,bat,state_DEFMultiple,Temporary_number
        global state_damageVariety,state_damageMultiple,bad_people_left,bad_people_right
        #需要計數來處理小弟
        if rd.randint(1,100)<=50:
            pass
        if count_one=='左1'or count_one=='左2'or count_one=='左3':
            bad_people_left+=1#還需要左右邊黑幫人數
        else:
            bad_people_right+=1
        field_Remaining_HP[count_one]-=max(state_sustained_damage[count_one])[0]*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#行動前被持傷打死
            who_survive[count_one]=0
            return 'die'
        field_Remaining_HP[count_one]-=bleed()*max(state_Exemption[count_one])[0]
        if field_Remaining_HP[count_one]<=0:#流血
            who_survive[count_one]=0
            return 'die'
        if state_evilstorm[count_one]==0:
            pass
        else:
            field_Remaining_HP[count_one]-=state_evilstorm[count_one][0]
            if field_Remaining_HP[count_one]<=0:#行動前被邪惡風暴打死
                who_survive[count_one]=0
                return 'die'
            else:
                state_evilstorm[count_one][1]-=1
                if state_evilstorm[count_one][1]==0:
                    state_evilstorm[count_one][0]=0
        if max(state_Dizziness[count_one])[0]==1:#被暈眩
            return 
        c=Chooseattack()
        a=[1,2,3,4,5,6]
        b=rd.choices(a,weights=(25,25,10,15,24,1))#取得機率
        now+=(' '+str(b[0])+' 技能')
        if b==[1]:#對一名敵人造成80~120傷害，若擁有球棒，擊暈目標1回合
            harm=rd.randint(80,120)
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            if bat[count_one]==1:#有bat
                return {1:harm,2:c,3:100,4:['暈眩',[[1,1,100,100,'可解除']]],5:'no',6:'no'}
            else:
                return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[2]:#對一名敵人造成40傷害x1.2xN，N的值為黑幫小弟人數
            pass#要加入左右黑幫人數判斷
            if count_one=='左1'or count_one=='左2'or count_one=='左3':
                pass
                if bad_people_left!=0:
                    harm=int(40*(1+bad_people_left*0.2))
                    harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
                    return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
                else:
                    harm=40
                    harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
                    return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
            elif count_one=='右1'or count_one=='右2'or count_one=='右3':
                pass
                if bad_people_right!=0:
                    harm=int(40*(1+bad_people_right*0.2))
                    harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
                    return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}
                else:
                    harm=40
                    harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
                    return {1:harm,2:c,3:100,4:'no',5:'no',6:'no'}

        if b==[3]:#恢復隨機隊友30%的HP
            pass
            if count_one=='左1'or count_one=='左2'or count_one=='左3':
                w=rd.choice(['左1', '左2', '左3'])
                field_Remaining_HP[w]+=int((field_Remaining_HP[w]*0.3))
                if field_Remaining_HP[w]>=all_role_hp[Temporary_number]:
                    field_Remaining_HP[w]=all_role_hp[Temporary_number]

        if b==[4]:#武器從空手變更為球棒，造成的傷害增加20%，若已擁有球棒，還可對全體敵人造成100傷害
            state_damageChange[count_one]+=0.2
            now='熊老大拿起了球棒'
            if bat[count_one]==1:
                harm=100
                harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
                return {1:harm,2:'all',3:100,4:'no',5:'no',6:'no'}
            else:
                bat[count_one]=1
                return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[5]:#全體隊友DEF增加100%，持續2回合
            pass
            if count_one=='左1'or count_one=='左2'or count_one=='左3':
                state_DEFMultiple['左1']+=[[1,2.100,100,'可解除']]
                state_DEFMultiple['左2']+=[[1,2.100,100,'可解除']]
                state_DEFMultiple['左3']+=[[1,2.100,100,'可解除']]
            else:
                state_DEFMultiple['右1']+=[[1,2.100,100,'可解除']]
                state_DEFMultiple['右2']+=[[1,2.100,100,'可解除']]
                state_DEFMultiple['右3']+=[[1,2.100,100,'可解除']]
            return {1:0,2:c,3:100,4:'no',5:'no',6:'no'}
        if b==[6]:#對一名敵人造成3500傷害，無法迴避
            harm=3500
            harm=count(harm,max(state_damageVariety[count_one])[0],state_damageChange[count_one],max(state_damageMultiple[count_one])[0])
            return {1:harm,2:c,3:'無法迴避',4:'no',5:'no',6:'no'}

#----------------------------------------------------------------------------#

    def bearboss_def():#熊老大的防禦函數
        global field_Remaining_HP,field_Remaining_DEF,cause_damage,all_role_miss,state_miss,count_two
        global state_Exemption,state_DEFVariety,state_DEFChange,state_DEFMultiple,who_survive,field_number
        global true_keys,count_one,now,originally_HP
        a=rd.randint(0,100)
        d=field_number[count_two]
        if cause_damage[3]=='無法迴避':
            pass
        elif a<=cause_damage[3]-all_role_miss[d]+max(state_miss[count_two])[0]:#迴避失敗
            pass
        else:#迴避成功
            now+='熊老大靈巧的躲開了'
            return
        now+='對熊老大造成 '
        ifhavestate() #被給予,非觸發
        
        b=count(field_Remaining_DEF[count_two],max(state_DEFVariety[count_two])[0],state_DEFChange[count_two],max(state_DEFMultiple[count_two])[0])
        if type(cause_damage[2])==list:
            pass
        if cause_damage[2][0]=='連擊':
            b=b*cause_damage[2][1]
        if cause_damage[1]-b<=0:#b為防禦
            return#無傷害
        else:
            field_Remaining_HP[count_two]-=(cause_damage[1]-b)*max(state_Exemption[count_two])[0]
            now+=str(int((cause_damage[1]-b)*max(state_Exemption[count_two])[0]))
        if field_Remaining_HP[count_two]<=0:#熊老大擁有球棒時免疫一次致命傷害，之後武器變回空手並恢復100HP
            pass
            if bat[count_two]==1:
                field_Remaining_HP[count_two]=100
                bat[count_two]=0
                now+=',熊老大用球棒擋住了致命傷害'
            else:
                who_survive[count_two]=0
                print(f'{count_two}死了')
    
        return

#----------------------------------------------------------------------------#

    def bleed():
        global state_bleed,true_keys,count_one,field_Remaining_HP
        print('流血計算')
        if len(state_bleed[count_one])==1:
            return 0
        else:
            for i in range(0,len(state_bleed[count_one])-1):
                a=state_bleed[count_one][0][0]
                state_bleed[count_one][0][0]+=state_bleed[count_one][i+1][0]
                b=state_bleed[count_one][0][0]
                state_bleed[count_one][0][0]=a
                return b

#----------------------------------------------------------------------------#

    def if_critical_hit():#直接回傳爆傷#(函數)是否爆擊
        global true_keys,count_one,field_Remaining_Critical,state_Critical
        a=field_Remaining_Critical[count_one]+max(state_Critical[count_one])[0]
        print('爆擊計算')
        if a>=rd.randint(0,100):#成功爆擊
            print('成功爆擊')
            return 2
        else:
            print('不爆擊')
            return 1

#----------------------------------------------------------------------------#

    def character():#(函數)機算抽到的角色編號
        global Select_role,field_number
        Select_role= rd.randint(1,5)
        if Select_role ==1:
            return embed_powder()
        if Select_role ==2:
            return embed_colorWolf()
        if Select_role ==3:
            return embed_flower()
        if Select_role ==4:
            return embed_car()
        if Select_role ==5:
            return embed_bearboss()

#----------------------------------------------------------------------------#

    def Remaining_rounds_reduced():#(函數)該角色的餘剩回合減少
        global true_keys,count_one,state_damageVariety,state_damageMultiple,state_SPVariety,state_SPMultiple
        global state_DEFMultiple,state_DEFVariety,state_Exemption,state_Dizziness,state_noheal
        global state_sustained_damage,state_bleed,state_evilcurse,state_evilstorm,state_squelch
        global state_Critical,state_miss
        print('該角色的餘剩回合減少')
        state=[state_damageVariety,state_damageMultiple,state_SPVariety,state_SPMultiple,state_DEFMultiple,state_DEFVariety,state_Exemption,state_Dizziness,state_noheal,state_sustained_damage,state_bleed,state_squelch,state_Critical,state_miss]

        for d in state:#有時sublist會變成int,原因不明
            to_remove = []
            for index, sublist in enumerate(d[count_one]):
                if len(sublist) > 1:
                    sublist[1] -= 1
                    if sublist[1] <= 0:
                            to_remove.append(index)
            to_remove.sort(reverse=True)  # 逆序排序索引，以避免刪除後影響之後的索引
            for index in to_remove:
                    del d[count_one][index]#上面這鬼東西可以把所有異常狀態的回合數減1並刪除所有回合為0的狀態

        return

#----------------------------------------------------------------------------#

    def who_attack():#(函數)判斷誰攻擊
        global Temporary_number,now
        print('判斷誰攻擊')
        if Temporary_number==1:
            now='邪惡的粉用'
            return powder_damage()
        if Temporary_number==2:
            now='色狼用'
            return colorWolf_damage()
        if Temporary_number==3:
            now='輻佬貳用'
            return flower_damage()
        if Temporary_number==4:
            now='移動式異世界傳送門用'
            return car_damage()
        if Temporary_number==5:
            now='熊老大用'
            return bearboss_damage()

#----------------------------------------------------------------------------#

    def what_type():#(函數)判斷攻擊型態#所有cause_damage可能的情況為'all','佔位',['隨機',攻擊次數],['連擊',攻擊次數,c],None
        global field_number,true_keys,count_one,cause_damage,count_two
        print('判斷攻擊型態')
        if cause_damage=='die':
            return
        if cause_damage==None:
            print('沒有造成傷害')
            return
        
        if type(cause_damage[2])==str:
            pass
            if cause_damage[2][0]=='連擊':                   #隨機攻擊格式為['隨機',攻擊次數]#連擊格式為['連擊',攻擊次數,c]
                cause_damage[1]=cause_damage[1]*cause_damage[2][1]#傷害乘攻擊次數
                who_def(cause_damage[2][2])
                return
            if cause_damage[2][0]=='隨機':
                for i in range(0,cause_damage[2][1]):
                    if count_one=='左1'or count_one=='左2'or count_one=='左3':
                        a=rd.choice(['右1', '右2', '右3'])
                        count_two=a
                        who_def(a)
                    else:
                        a=rd.choice(['左1', '左2', '左3'])
                        count_two=a
                        who_def(a)
                return
            if cause_damage[2]=='all':
                pass
                if count_one=='左1'or count_one=='左2'or count_one=='左3':#true_keys[count_one]是當前行動的角色
                    for a in range(1,4):
                        b=field_number[f'右{a}']
                        count_two=f'右{a}'
                        who_def(b)
                    return
                else:
                    for a in range(1,4):
                        b=field_number[f'左{a}']
                        count_two=f'左{a}'
                        who_def(b) 
                    return

            else:
                a=field_number[cause_damage[2]]
                count_two=cause_damage[2]
                who_def(a)
                return

#----------------------------------------------------------------------------#

    def who_def(a):#(函數)判斷誰防禦(a)
        global field_number,cause_damage
        print('判斷誰防禦')
        if type(a)==str:
            a=field_number[a]
        if a==1:
            return powder_def()
        if a==2:
            return colorWolf_def()
        if a==3:
            return flower_def()
        if a==4:
            return car_def()
        if a==5:
            return bearboss_def()

#----------------------------------------------------------------------------#

    def ifhavestate():#(函數)是否有異常狀態
        global cause_damage,all_role_Resistance
        print('檢查異常狀態')
        if cause_damage[4]==cause_damage[5]==cause_damage[6]=='no':#皆無給予異常狀態
            return
        elif cause_damage[4]!='no':#有異常狀態
            state_determination()

#----------------------------------------------------------------------------#
    def state_determination():#(函數)異常狀態判定
        global true_keys,count_one,state_damageVariety,state_damageMultiple,state_SPVariety,state_SPMultiple
        global state_DEFMultiple,state_DEFVariety,state_Exemption,state_Dizziness,state_noheal
        global state_sustained_damage,state_bleed,state_evilcurse,state_evilstorm,state_squelch
        global state_Critical,state_miss,all_role_Resistance,count_two,field_Remaining_HP,count_two
        print('判定異常狀態')
        if type(cause_damage[2])==list:#一定是連擊#['連擊',攻擊次數,'佔位']#連擊部分已完成,再來處理'all'
            for i in range(4,7):#不可能為邪惡詛咒
                if cause_damage[i][0]=='持續傷害':
                    b=rd.randint(1,100)
                    if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2][2]]:#抵抗失敗
                        state_sustained_damage[cause_damage[2][2]]+cause_damage[i][1]
                        continue
                    else:
                        continue
                if cause_damage[i][0]=='流血':
                    b=rd.randint(1,100)
                    if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2][2]]:#抵抗失敗
                        state_bleed[cause_damage[2][2]]+cause_damage[i][1]
                        continue
                    else:
                        continue
                if cause_damage[i][0]=='速度降低':
                    b=rd.randint(1,100)
                    if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2][2]]:#抵抗失敗
                        state_SPVariety[cause_damage[2][2]]+cause_damage[i][1]
                        continue
                    else:
                        continue
                if cause_damage[i][0]=='暈眩':
                    b=rd.randint(1,100)
                    if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2][2]]:#抵抗失敗
                        state_Dizziness[cause_damage[2][2]]+cause_damage[i][1]
                        continue
                    else:
                        continue
                if cause_damage[i][0]=='無法回血':
                    b=rd.randint(1,100)
                    if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2][2]]:#抵抗失敗
                        state_noheal[cause_damage[2][2]]+cause_damage[i][1]
                        continue
                    else:
                        continue
                return
        elif type(cause_damage[2])==str:##此時造成傷害[2]為'佔位'或'all'
            pass
            if cause_damage[2]=='all':#處理'all',剩下'佔位'
                for i in range(4,7):
                    if cause_damage[i]=='邪惡詛咒':#邪惡詛咒為特殊格式
                        state_evilcurse[count_two]+=1
                        if state_evilcurse[count_two]>=20:
                            print('詛咒發作')
                            state_evilcurse[count_two]-=20
                            field_Remaining_HP[count_two]-=500
                            if field_Remaining_HP[cause_damage[2]]<=0:
                                who_survive[cause_damage[2]]=0
                            continue
                        continue
                    if type(cause_damage[i][1])==list:
                        if cause_damage[i][0]=='持續傷害':
                            b=rd.randint(1,100)
                            if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[count_two]:#抵抗失敗
                                state_sustained_damage[count_two]+cause_damage[i][1]
                                continue
                            else:
                                continue
                        if cause_damage[i][0]=='流血':
                            b=rd.randint(1,100)
                            if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[count_two]:#抵抗失敗
                                state_bleed[count_two]+cause_damage[i][1]
                                continue
                            else:
                                continue
                        if cause_damage[i][0]=='速度降低':
                            b=rd.randint(1,100)
                            if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[count_two]:#抵抗失敗
                                state_SPVariety[count_two]+cause_damage[i][1]
                                continue
                            else:
                                continue
                        if cause_damage[i][0]=='暈眩':
                            b=rd.randint(1,100)
                            if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[count_two]:#抵抗失敗
                                state_Dizziness[count_two]+cause_damage[i][1]
                                continue
                            else:
                                continue
                        if cause_damage[i][0]=='無法回血':
                            b=rd.randint(1,100)
                            if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[count_two]:#抵抗失敗
                                state_noheal[count_two]+cause_damage[i][1]
                                continue
                            else:
                                continue
                return
        else:#必為'佔位'          
            for i in range(4,7):
                if cause_damage[i]=='邪惡詛咒':#邪惡詛咒為特殊格式
                    state_evilcurse[cause_damage[2]]+=1
                    if state_evilcurse[cause_damage[2]]>=20:
                        print('詛咒發作')
                        state_evilcurse[cause_damage[2]]-=20
                        field_Remaining_HP[cause_damage[2]]-=500
                        if field_Remaining_HP[cause_damage[2]]<=0:
                            who_survive[cause_damage[2]]=0
                        continue
                    continue
                if type(cause_damage[i][1])==list:
                    pass
                    if cause_damage[i][0]=='持續傷害':
                        b=rd.randint(1,100)
                        if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2]]:#抵抗失敗
                            state_sustained_damage[cause_damage[2]]+cause_damage[i][1]
                            continue
                        else:
                            continue
                    if cause_damage[i][0]=='流血':
                        b=rd.randint(1,100)
                        if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2]]:#抵抗失敗
                            state_bleed[cause_damage[2]]+cause_damage[i][1]
                            continue
                        else:
                            continue
                    if cause_damage[i][0]=='速度降低':
                        b=rd.randint(1,100)
                        if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2]]:#抵抗失敗
                            state_SPVariety[cause_damage[2]]+cause_damage[i][1]
                            continue
                        else:
                            continue
                    if cause_damage[i][0]=='暈眩':
                        b=rd.randint(1,100)
                        if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2]]:#抵抗失敗
                            state_Dizziness[cause_damage[2]]+cause_damage[i][1]
                            continue
                        else:
                            continue
                    if cause_damage[i][0]=='無法回血':
                        b=rd.randint(1,100)
                        if b<cause_damage[i][1][0][2]-field_Remaining_Resistance[cause_damage[2]]:#抵抗失敗
                            state_noheal[cause_damage[2]]+cause_damage[i][1]
                            continue
                        else:
                            continue
            return

#----------------------------------------------------------------------------#

    def Chooseattack():#(函數)選擇要攻擊誰  #這裡會陷入無盡迴圈
        global true_keys,true_keys_length,count_one,who_survive
        true_keys_length=len(true_keys)
        print('選擇要攻擊誰')
        print(f'count_one={count_one}')
        if count_one=='左1'or count_one=='左2'or count_one=='左3':#為左,要打右
            a=rd.choice(['右1', '右2', '右3'])
            while who_survive[a]==0:
                a=rd.choice(['右1', '右2', '右3'])
            return a
        else:#為右,要打左
            a=rd.choice(['左1', '左2', '左3'])
            while who_survive[a]==0:
                a=rd.choice(['左1', '左2', '左3'])
            return a

#----------------------------------------------------------------------------#
    def One_turn_of_action():#(函數)一回合的行動#終極函數
        global who_can_action,Temporary_number,field_number,true_keys,cause_damage,count_one,state_Dizziness
        count_one=0
        print('回合開始')
        speed_calculation()#(函數)速度計算

        true_keys = [key for key, value in who_can_action.items() if value]#找出哪些能動
        #true_keys儲存的是位置!
        a=list(true_keys)
        print(f'true_keys={true_keys}')
        for i in a:#取得同一回合能動的佔位
            count_one=i#現在計數一直接等於當前佔位
            Temporary_number=field_number[i]      #站位(字典) [a[i]] 為取得的角色編號  #目前已取得角色編號
            print(f'Temporary_number={Temporary_number}')
            cause_damage=who_attack()

            print(f'cause_damage為{cause_damage}')
            if cause_damage=='die':
                return

            if type(cause_damage)==dict:
                cause_damage[1]*=if_critical_hit()

            what_type()
            Remaining_rounds_reduced()
            if bad_people_left>=1:
                pass
                if rd.randint(1,100)<=30:#打右邊
                    w=rd.choice(['右1', '右2', '右3'])
                    field_Remaining_HP[w]-=(bad_people_left*15)
            if bad_people_right>=1:
                pass
                if rd.randint(1,100)<=30:#打左邊
                    w=rd.choice(['左1', '左2', '左3'])
                    field_Remaining_HP[w]-=(bad_people_right*15)

            
            
            if who_survive['左1']==0 and who_survive['左2']==0 and who_survive['左3']==0:
                break
            if who_survive['右1']==0 and who_survive['右2']==0 and who_survive['右3']==0:
                break
            for q in range(1,4):
                field_Remaining_HP[f'左{q}']=int(field_Remaining_HP[f'左{q}'])
                field_Remaining_HP[f'右{q}']=int(field_Remaining_HP[f'右{q}'])

        count_one=0
        true_keys=0
        who_can_action={'左1':False,'左2':False,'左3':False,'右1':False,'右2':False,'右3':False}
        print('回合結束')
        print(f'剩餘hp{field_Remaining_HP}')
        return

#----------------------------------------------------------------------------#

    def speed_calculation():#(函數)速度計算
        global field_Remaining_SP,turn_bar,who_can_action,who_survive,state_SPChange
        global state_SPVariety,state_SPMultiple
        a=0

        while 1:
            print(turn_bar)
            for i in range(1,4):#所有角色的速度增加#(佔位速度+速度變化)*(速度倍率+速度改變+1)
                turn_bar[f'左{i}']+=(field_Remaining_SP[f'左{i}']+max(state_SPVariety[f'左{i}'])[0])*(1+max(state_SPMultiple[f'左{i}'])[0]+state_SPChange[f'左{i}'])
                turn_bar[f'右{i}']+=(field_Remaining_SP[f'右{i}']+max(state_SPVariety[f'右{i}'])[0])*(1+max(state_SPMultiple[f'右{i}'])[0]+state_SPChange[f'右{i}'])

            for j in range(1,4):#把死亡角色的回合條設為0#這裡有問題
                if who_survive[f'左{j}']==0:
                    turn_bar[f'左{j}']=0
                if who_survive[f'右{j}']==0:
                    turn_bar[f'右{j}']=0


            for key,value in turn_bar.items():#判斷是否有角色能行動
                if value >= 1000:
                    who_can_action[key]= True #找出哪些角色能行動
                    a+=1
                    turn_bar[key]-=1000

            if a>=1:
                return

#----------------------------------------------------------------------------#

    if msg=='圖鑑':
        a=discord.Embed(title="全角色圖鑑",description="目前只有五隻角色", color=0xEAC999)
        a.add_field(name="NO.1", value="邪惡的粉", inline=True)
        a.add_field(name="NO.2", value="色狼", inline=True)
        a.add_field(name="NO.3", value="輻佬貳", inline=True)
        a.add_field(name="NO.4", value="移動式異世界傳送門", inline=True)
        a.add_field(name="NO.5", value="熊老大", inline=True)
        await channel.send(embed=a)

#----------------------------------------------------------------------------#

    if msg.startswith('查看NO.1'):
        a=embed_powder()
        await channel.send(embed=a)
    if msg.startswith('查看NO.2'):
        a=embed_colorWolf()
        await channel.send(embed=a)
    if msg.startswith('查看NO.3'):
        a=embed_flower()
        await channel.send(embed=a)
    if msg.startswith('查看NO.4'):
        a=embed_car()
        await channel.send(embed=a)
    if msg.startswith('查看NO.5'):
        a=embed_bearboss()
        await channel.send(embed=a)

#----------------------------------------------------------------------------#
    if msg =='單挑阿':
        #global player_name,Whether_to_enable_1v1,total_people,people_left,people_right
        #global Select_role,total_people,all_role_name,field_number
        allRemake()
        Whether_to_enable_1v1=True
        user = message.author
        username_left = user.name
        player_name['左1']=user.name
        total_people=2
        embed=character()
        field_number['左1']=Select_role

        embed_message = await channel.send(embed=embed)

        total_people-=1
        await channel.send(f'{player_name["左1"]}發動了1v1戰鬥,想挑戰他的話請輸入:加入')
        await channel.send(f'{player_name["左1"]}的位置是左邊')
        await channel.send(f'剩下{total_people}個名額')

    if msg.startswith('加入')and Whether_to_enable_1v1:#1v1正式版
        user = message.author
        print('已截止,開始單挑')
        Whether_to_enable_1v1=False
        player_name['右1']=user.name
        embed=character()
        embed_message = await channel.send(embed=embed)
        field_number['右1']=Select_role
        await channel.send(f'{player_name["右1"]}的位置是右邊')
        await channel.send('已截止,開始單挑')


        embed2=discord.Embed(title="1v1", description=f'{player_name["左1"]}的 {all_role_name[field_number["左1"]]}VS.  {player_name["右1"]}的 {all_role_name[field_number["右1"]]}',color=0xff0000)#基本排版
        embed2.set_author(name=client.user)
        embed2.add_field(name=all_role_name[field_number["左1"]], value=all_role_hp[field_number["左1"]], inline=True)
        embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
        embed2.add_field(name=all_role_name[field_number["右1"]], value=all_role_hp[field_number["右1"]], inline=True)
        embed2.add_field(name="XXXX", value="xxxxx", inline=True)
        embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
        embed2.add_field(name="XXXX", value="xxxxx", inline=True)
        embed2.add_field(name="XXXX", value="xxxxx", inline=True)
        embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
        embed2.add_field(name="XXXX", value="xxxxx", inline=True)
        embed_message = await channel.send(embed=embed2)

        field_Remaining_SP['左1']=all_role_sp[field_number['左1']]
        field_Remaining_HP['左1']=all_role_hp[field_number['左1']]
        field_Remaining_DEF['左1']=all_role_def[field_number['左1']]
        field_Remaining_Critical['左1']=all_role_Critical[field_number['左1']]
        field_Remaining_Miss['左1']=all_role_miss[field_number['左1']]
        field_Remaining_Resistance['左1']=all_role_Resistance[field_number['左1']]

        field_Remaining_SP['右1']=all_role_sp[field_number['右1']]
        field_Remaining_HP['右1']=all_role_hp[field_number['右1']]
        field_Remaining_DEF['右1']=all_role_def[field_number['右1']]
        field_Remaining_Critical['右1']=all_role_Critical[field_number['右1']]
        field_Remaining_Miss['右1']=all_role_miss[field_number['右1']]
        field_Remaining_Resistance['右1']=all_role_Resistance[field_number['右1']]

        who_survive={'左1':1,'左2':0,'左3':0,'右1':1,'右2':0,'右3':0}

        while 1:
            time.sleep(1)
            originally_HP=field_Remaining_HP
            One_turn_of_action()
            #持續編輯embed
            a=say_1v1()
            await embed_message.edit(embed=a)

            if who_survive['左1']==0 and who_survive['左2']==0 and who_survive['左3']==0:
                z='右方'
                y='右1'
                break
            if who_survive['右1']==0 and who_survive['右2']==0 and who_survive['右3']==0:
                z='左方'
                y='左1'
                break

        a=discord.Embed(title=f"恭喜{z}的{player_name[y]}取得勝利")

        embed_message = await channel.send(embed=a)
        print('比賽結束')
        allRemake()#(函數)重置數值

#----------------------------------------------------------------------------#

    if msg == '發動2v2' and total_people==0:#2v2正式版
        allRemake()
        user = message.author
        people=4
        people_left=2
        people_right=2
        player_name['左1']=user.name
        total_people=4
        embed=character()
        field_number['左1']=Select_role
        embed_message = await channel.send(embed=embed)
        total_people-=1
        people_left-=1
        await channel.send(f'{player_name["左1"]}發動了2v2戰鬥,想挑戰他的話請輸入:加入2v2')
        await channel.send(f'{player_name["左1"]}的位置是左1')
        await channel.send(f'剩下{total_people}個名額')
    if msg.startswith('加入2v2')and total_people!=0:#順序為左1>右1>左2>右2
        user = message.author
        if total_people==3:
            player_name['右1']=user.name
            total_people-=1
            people_right-=1
            embed=character()
            field_number['右1']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["右1"]}的位置是右1')
            await channel.send(f'剩下{total_people}個名額')
        elif total_people==2:
            player_name['左2']=user.name
            total_people-=1
            people_left-=1
            embed=character()
            field_number['左2']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["左2"]}的位置是左2')
            await channel.send(f'剩下{total_people}個名額')
        else:
            player_name['右2']=user.name
            total_people=0
            people_right-=1
            embed=character()
            field_number['右2']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["右2"]}的位置是右2')
            await channel.send('2v2已截止')
            await channel.send(f'{player_name["左1"]} VS. {player_name["右1"]}\n{player_name["左2"]} VS. {player_name["右2"]}')
            embed2=discord.Embed(title="2v2", description=f'{player_name["左1"]} 的{all_role_name[field_number["左1"]]}V.S  {player_name["右1"]} 的{all_role_name[field_number["右1"]]}\n {player_name["左2"]} 的{all_role_name[field_number["左2"]]}V.S  {player_name["右2"]} 的{all_role_name[field_number["右2"]]}',color=0xff0000)#基本排版
            embed2.set_author(name=client.user)
            embed2.add_field(name=all_role_name[field_number["左1"]], value=all_role_hp[field_number["左1"]], inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name=all_role_name[field_number["右1"]], value=all_role_hp[field_number["右1"]], inline=True)
            embed2.add_field(name=all_role_name[field_number["左2"]], value=all_role_hp[field_number["左2"]], inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name=all_role_name[field_number["右2"]], value=all_role_hp[field_number["右2"]], inline=True)
            embed2.add_field(name="XXXX", value="xxxxx", inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name="XXXX", value="xxxxx", inline=True)
            embed_message = await channel.send(embed=embed2)

            for i in range(1,3): #以後不用改
                field_Remaining_SP[f'左{i}']=all_role_sp[field_number[f'左{i}']]
                field_Remaining_HP[f'左{i}']=all_role_hp[field_number[f'左{i}']]
                field_Remaining_DEF[f'左{i}']=all_role_def[field_number[f'左{i}']]
                field_Remaining_Critical[f'左{i}']=all_role_Critical[field_number[f'左{i}']]
                field_Remaining_Miss[f'左{i}']=all_role_miss[field_number[f'左{i}']]
                field_Remaining_Resistance[f'左{i}']=all_role_Resistance[field_number[f'左{i}']]
            for k in range(1,3):
                field_Remaining_SP[f'右{k}']=all_role_sp[field_number[f'右{k}']]
                field_Remaining_HP[f'右{k}']=all_role_hp[field_number[f'右{k}']]
                field_Remaining_DEF[f'右{k}']=all_role_def[field_number[f'右{k}']]
                field_Remaining_Critical[f'右{k}']=all_role_Critical[field_number[f'右{k}']]
                field_Remaining_Miss[f'右{k}']=all_role_miss[field_number[f'右{k}']]
                field_Remaining_Resistance[f'右{k}']=all_role_Resistance[field_number[f'右{k}']]
            z=''
            who_survive={'左1':1,'左2':1,'左3':0,'右1':1,'右2':1,'右3':0}
            while 1:
                time.sleep(1)
                originally_HP=field_Remaining_HP
                One_turn_of_action()
                a=say_2v2()
                await embed_message.edit(embed=a)
                if who_survive['左1']==0 and who_survive['左2']==0 and who_survive['左3']==0:
                    z='右方'
                    y='右1'
                    x='右2'
                    break
                if who_survive['右1']==0 and who_survive['右2']==0 and who_survive['右3']==0:
                    z='左方'
                    y='左1'
                    x='左2'
                    break
                
            a=discord.Embed(title=f"恭喜{z}的{player_name[y]}和{player_name[x]}取得勝利")

            embed_message = await channel.send(embed=a)

            allRemake()

#----------------------------------------------------------------------------#

    if msg=='群架'and total_people==0:
        allRemake()
        user = message.author
        people=6
        player_name['左1']=user.name
        total_people=6
        embed=character()
        field_number['左1']=Select_role
        embed_message = await channel.send(embed=embed)
        total_people-=1
        await channel.send(f'{player_name["左1"]}發動了3v3戰鬥,想挑戰他的話請輸入:加入3v3')
        await channel.send(f'{player_name["左1"]}的位置是左1')
        await channel.send(f'剩下{total_people}個名額')
    if msg==('加入3v3')and total_people!=0:#順序為左1>右1>左2>右2>左3>右3
        print('ok')
        user = message.author
        if total_people==5:
            player_name['右1']=user.name
            total_people-=1
            people_right-=1
            embed=character()
            field_number['右1']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["右1"]}的位置是右1')
            await channel.send(f'剩下{total_people}個名額')
        elif total_people==4:
            player_name['左2']=user.name
            total_people-=1
            people_left-=1
            embed=character()
            field_number['左2']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["左2"]}的位置是左2')
            await channel.send(f'剩下{total_people}個名額')
        elif total_people==3:
            player_name['右2']=user.name
            total_people-=1
            people_left-=1
            embed=character()
            field_number['右2']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["右2"]}的位置是右2')
            await channel.send(f'剩下{total_people}個名額')
        elif total_people==2:
            player_name['左3']=user.name
            total_people-=1
            people_left-=1
            embed=character()
            field_number['左3']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["左3"]}的位置是左3')
            await channel.send(f'剩下{total_people}個名額')
        else:
            player_name['右3']=user.name
            total_people-=1
            people_left-=1
            embed=character()
            field_number['右3']=Select_role
            embed_message = await channel.send(embed=embed)
            await channel.send(f'{player_name["右3"]}的位置是右3')
            await channel.send(f'剩下{total_people}個名額')
            await channel.send('3v3已截止')
            await channel.send(f'{player_name["左1"]} VS. {player_name["右1"]}\n{player_name["左2"]} VS. {player_name["右2"]}\n{player_name["左3"]} VS. {player_name["右3"]}')
            embed2=discord.Embed(title="3v3", description=f'{player_name["左1"]} 的{all_role_name[field_number["左1"]]}V.S  {player_name["右1"]} 的{all_role_name[field_number["右1"]]}\n {player_name["左2"]} 的{all_role_name[field_number["左2"]]}V.S  {player_name["右2"]} 的{all_role_name[field_number["右2"]]}\n {player_name["左3"]} 的{all_role_name[field_number["左3"]]}V.S  {player_name["右3"]} 的{all_role_name[field_number["右3"]]}',color=0xff0000)#基本排版
            embed2.set_author(name=client.user)
            embed2.add_field(name=all_role_name[field_number["左1"]], value=all_role_hp[field_number["左1"]], inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name=all_role_name[field_number["右1"]], value=all_role_hp[field_number["右1"]], inline=True)
            embed2.add_field(name=all_role_name[field_number["左2"]], value=all_role_hp[field_number["左2"]], inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name=all_role_name[field_number["右2"]], value=all_role_hp[field_number["右2"]], inline=True)
            embed2.add_field(name=all_role_name[field_number["左3"]], value=all_role_hp[field_number["左3"]], inline=True)
            embed2.add_field(name="戰鬥字幕", value=">>><<<", inline=True)
            embed2.add_field(name=all_role_name[field_number["右3"]], value=all_role_hp[field_number["右3"]], inline=True)
            embed_message = await channel.send(embed=embed2)
        for i in range(1,4): #以後不用改
            field_Remaining_SP[f'左{i}']=all_role_sp[field_number[f'左{i}']]
            field_Remaining_HP[f'左{i}']=all_role_hp[field_number[f'左{i}']]
            field_Remaining_DEF[f'左{i}']=all_role_def[field_number[f'左{i}']]
            field_Remaining_Critical[f'左{i}']=all_role_Critical[field_number[f'左{i}']]
            field_Remaining_Miss[f'左{i}']=all_role_miss[field_number[f'左{i}']]
            field_Remaining_Resistance[f'左{i}']=all_role_Resistance[field_number[f'左{i}']]
        for k in range(1,4):
            field_Remaining_SP[f'右{k}']=all_role_sp[field_number[f'右{k}']]
            field_Remaining_HP[f'右{k}']=all_role_hp[field_number[f'右{k}']]
            field_Remaining_DEF[f'右{k}']=all_role_def[field_number[f'右{k}']]
            field_Remaining_Critical[f'右{k}']=all_role_Critical[field_number[f'右{k}']]
            field_Remaining_Miss[f'右{k}']=all_role_miss[field_number[f'右{k}']]
            field_Remaining_Resistance[f'右{k}']=all_role_Resistance[field_number[f'右{k}']]
        z=''
        who_survive={'左1':1,'左2':1,'左3':1,'右1':1,'右2':1,'右3':1}
        while 1:
            time.sleep(1)
            originally_HP=field_Remaining_HP
            One_turn_of_action()
            a=say_3v3()
            await embed_message.edit(embed=a)
            if who_survive['左1']==0 and who_survive['左2']==0 and who_survive['左3']==0:
                z='右方'
                y='右1'
                x='右2'
                w='右3'
                break
            if who_survive['右1']==0 and who_survive['右2']==0 and who_survive['右3']==0:
                z='左方'
                y='左1'
                x='左2'
                w='左3'
                break
        
        a=discord.Embed(title=f"恭喜{z}的{player_name[y]}和{player_name[x]}及{player_name[w]}取得勝利")
        
        embed_message = await channel.send(embed=a)
        
        allRemake()