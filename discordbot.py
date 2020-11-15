from discord.ext import commands
import os
import traceback
import random
import math
import typing

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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
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
    """NdN形式でダイスを振ります。"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    li = []
    for r in range(rolls):
        li.append(random.randint(1, limit))
    result = ','.join(map(str, li))
    await ctx.send(dice + ' -> [' + result + '] -> ' + str(sum(li)))
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

    # 山札を超える場合の処理
    if card > (52 + joker) * deck:
        await ctx.send('ドロー枚数が多すぎます。山札の枚数以下で指定してください。')
        return
    # 負数とか指定された場合の処理
    if card <= 0 or joker < 0 or deck <= 0:
        await ctx.send('間違った値が入力されています。/n[ドロー枚数][山数]は1以上、[JOKER枚数]は0以上で入力してください。')
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
