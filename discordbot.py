import discord
from discord.ext import commands
import os
import traceback
import random
import math
import typing
import re

bot = commands.Bot(command_prefix='/')
TOKEN = os.environ['DISCORD_BOT_TOKEN']

# コマンド設定
description = '''できること一覧。
コマンドは先頭に"/"をつけてください。'''
bot = commands.Bot(command_prefix='/', description=description)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

# 起動時に動作する処理
@bot.event
async def on_ready():
    # botのステータスを設定
    activity = discord.Game(name='人生')
    await bot.change_presence(activity=activity)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# ダイス処理関数
def diceroll(dice):
    # フォーマット整理：面数指定なしはD6とする
    pattern_NDblank = "D(?![1-9])"
    pattern_NDN = "[1-9][0-9]*D[1-9][0-9]*"
    dice = dice.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    dice = dice.strip().replace('　', ' ').replace(' ', '').upper()
    dice = re.sub(pattern_NDblank, 'D6', dice)
    diceset = re.findall(pattern_NDN, dice)
    dsumlist, dielist, result1, result2 = [], [], dice, dice

    for n in diceset:
        rolls, limit = map(int, n.split('D'))
        die = [random.randint(1, limit) for r in range(rolls)]
        dsum = sum(die)
        dsumlist.append(dsum)
        dielist.append(str(die).replace(' ',''))
    for m in range(len(diceset)):
        result1 = result1.replace(diceset[m], str(dsumlist[m]) + dielist[m], 1)
        result2 = result2.replace(diceset[m], str(dsumlist[m]), 1)
    total = eval(result2)
    return [dice, result1, result2, str(total)]

# ねこちゃんが返事をする
@bot.command()
async def neko(ctx):
    """ねこちゃんがランダムで返事をします。"""
    nekochan = ['にゃーん', '……んなぁご', 'ゴロゴロ', 'ふにゃあ', 'みゃみゃみゃ……', 'フシャーッ！', 'にゃにゃっ', 'GMから逃げるな']
    await ctx.send(random.choice(nekochan))
    print('command neko is send successfully.')
    print('------')

# ダイスを振る
@bot.command()
async def roll(ctx, dice : str):
    """入力されたダイスを振ります。`CoC`または`CoC6`と入力するとクトゥルフ6版、`CoC7`と入力するとクトゥルフ7版の探索者を自動生成します。"""
    PATTERN_rollset = '\[.+?\]'
    if dice == "CoC" or dice == "CoC6":
        throw = '3d+3d+3d+3d+3d+2d+2d+3d'
        try:
            dice_return = diceroll(throw)
        except Exception:
            await ctx.send('入力が間違っているかもしれません……')
            return
        rollset = re.findall(PATTERN_rollset, dice_return[1])
        status = ['STR', 'CON', 'POW', 'DEX', 'APP', 'SIZ', 'INT', 'EDU']
        dice_sum = dice_return[2].split('+')
        output_CoC = ''
        for x in range(len(status)):
            if status[x] in ['SIZ', 'INT']:
                output_CoC += status[x] + ' -> ' + rollset[x] + '   +6 -> ' + str(int(dice_sum[x])+6) + '\n'
            elif status[x] =='EDU':
                output_CoC += status[x] + ' -> ' + rollset[x] + ' +3 -> ' + str(int(dice_sum[x])+3) + '\n'
            else:
                output_CoC += status[x] + ' -> ' + rollset[x] + '    -> ' + str(int(dice_sum[x])) + '\n'
        output = 'クトゥルフ神話TRPG[6版]\n' + output_CoC + 'ダイス合計：' + str(dice_return[3])
    elif dice == 'CoC7':
        throw = '3d+3d+3d+3d+3d+2d+2d+2d+3d'
        try:
            dice_return = diceroll(throw)
        except Exception:
            await ctx.send('入力が間違っているかもしれません……')
            return
        rollset = re.findall(PATTERN_rollset, dice_return[1])
        status = ['STR', 'CON', 'POW', 'DEX', 'APP', 'SIZ', 'INT', 'EDU', 'LUK']
        dice_sum = dice_return[2].split('+')
        output_CoC = ''
        for x in range(len(status)):
            if status[x] in ['SIZ', 'INT', 'EDU']:
                output_CoC += status[x] + ' -> ' + rollset[x] + '   +6 ×5 -> ' + str(int(dice_sum[x])*5) + '\n'
            else:
                output_CoC += status[x] + ' -> ' + rollset[x] + '    ×5 -> ' + str(int(dice_sum[x])*5) + '\n'
        output = 'クトゥルフ神話TRPG[7版]\n' + output_CoC + 'ダイス合計：' + str(dice_return[3])
    else:
        try:
            dice_return = diceroll(dice)
        except Exception:
            await ctx.send('入力が間違っているかもしれません……')
            return
        output = dice_return[0] + '\n -> ' + dice_return[1] + '\n -> ' + dice_return[2] + '\n -> ' + dice_return[3]
        print(output)
    await ctx.send('```\n' + output + '```')
    print('command roll is send successfully.')
    print('------')

# choiceする
@bot.command()
async def choice(ctx, *choices : str):
    """スペース区切りの候補から1つをチョイスします。"""
    await ctx.send("choice[" + ', '.join(choices) + "] -> " + random.choice(choices))
    print('command choice is send successfully.')
    print('------')

# トランプを引く
@bot.command()
async def draw(ctx, card: typing.Optional[int] = 1, joker: typing.Optional[int] = 2, deck: typing.Optional[int] = 1):
    """トランプを引きます。スペース区切りで[ドロー枚数][JOKER枚数][山数]の指定が可能です。"""
    # 負数とか指定された場合の処理
    if card <= 0 or joker < 0 or deck <= 0:
        await ctx.send('間違った値が入力されています。\n[ドロー枚数][山数]は1以上、[JOKER枚数]は0以上で入力してください。')
        return
    # 山札を超える場合の処理
    if card > (52 + joker) * deck:
        await ctx.send('ドロー枚数が多すぎます。山札の枚数以下で指定してください。')
        return

    # シャッフルした山から指定枚数を抽出する
    wholeDeck = list(range((52 + joker) * deck))
    randomDeck = random.sample(wholeDeck, len(wholeDeck))

    for keyNo in randomDeck[0:card]:
        cardNo = keyNo % 13 + 1
        if keyNo % 13 + 1 == 1:
            cardNo = 'A'
        elif keyNo % 13 + 1 == 11:
            cardNo = 'J'
        elif keyNo % 13 + 1 == 12:
            cardNo = 'Q'
        elif keyNo % 13 + 1 == 13:
            cardNo = 'K'
        else:
            cardNo = str(keyNo % 13 + 1)
        if 52 * deck < keyNo <= (52 + joker) * deck:
            suite = "JOKER"
            cardNo = ""
        elif math.ceil(keyNo % 4) == 0:
            suite = "スペードの"
        elif math.ceil(keyNo % 4) == 1:
            suite = "ハートの"
        elif math.ceil(keyNo % 4) == 2:
            suite = "ダイヤの"
        else: # math.ceil(keyNo % 4) == 3:
            suite = "クラブの"
        await ctx.send(suite + cardNo)
    print('command draw is send successfully.')
    print('------')

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
