from discord.ext import commands
import os
import traceback
import random
import math

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

# 起動時に動作する処理
@bot.event
async def on_ready():
    # デッキ数・ジョーカー枚数の初期設定
    deck = 1 #デッキ数
    joker = 2 #ジョーカー枚数
    status = 'Deck' + str(deck) + ", Joker" + str(joker)
    # botのステータスを設定
    await client.change_presence(activity=discord.Game(name=status, type=1))
    print('正常に起動しました。')

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    # ランダムカード関数を実行
    if message.content == '/random':
        deck = 1 #デッキ数
        joker = 2 #ジョーカー枚数
        print('ランダムカード関数を実行します。デッキ数=', deck ,' Joker枚数=', joker)
        
        def RandomCard(deck, joker):
            randomCard = random.randrange(52 * deck + joker) + 1
            print('Original Card No.', randomCard)
            #Jokerの処理
            if 52 * deck < randomCard <= 52 * deck + joker:
                return "Joker"
            #スートの決定
            if randomCard % 4 == 0:
                cardSuite = "スペード"
                emojiSuite = ":spades:"
            elif randomCard % 4 == 1:
                cardSuite = "ハート"
                emojiSuite = ":hearts:"
            elif randomCard % 4 == 2:
                cardSuite = "ダイヤ"
                emojiSuite = ":diamonds:"
            elif randomCard % 4 == 3:
                cardSuite = "クラブ"
                emojiSuite = ":clubs:"
            #数字の決定
            if math.ceil(randomCard % 52 / 4) == 1:
                cardNumber = "A"
                emojiNumber = ":a:"
            elif math.ceil(randomCard % 52 / 4) == 2:
                cardNumber = "2"
                emojiNumber = ":two:"
            elif math.ceil(randomCard % 52 / 4) == 3:
                cardNumber = "3"
                emojiNumber = ":three:"
            elif math.ceil(randomCard % 52 / 4) == 4:
                cardNumber = "4"
                emojiNumber = ":four:"
            elif math.ceil(randomCard % 52 / 4) == 5:
                cardNumber = "5"
                emojiNumber = ":five:"
            elif math.ceil(randomCard % 52 / 4) == 6:
                cardNumber = "6"
                emojiNumber = ":six:"
            elif math.ceil(randomCard % 52 / 4) == 7:
                cardNumber = "7"
                emojiNumber = ":seven:"
            elif math.ceil(randomCard % 52 / 4) == 8:
                cardNumber = "8"
                emojiNumber = ":eight:"
            elif math.ceil(randomCard % 52 / 4) == 9:
                cardNumber = "9"
                emojiNumber = ":nine:"
            elif math.ceil(randomCard % 52 / 4) == 10:
                cardNumber = "10"
                emojiNumber = ":ten:"
            elif math.ceil(randomCard % 52 / 4) == 11:
                cardNumber = "J"
                emojiNumber = ":regional_indicator_j:"
            elif math.ceil(randomCard % 52 / 4) == 12:
                cardNumber ="Q"
                emojiNumber = ":regional_indicator_q:"
            elif math.ceil(randomCard % 52 / 4) == 13:
                cardNumber = "K"
                emojiNumber = ":regional_indicator_k:"
            return cardSuite + "の" + cardNumber + emojiSuite + emojiNumber

        result = RandomCard(deck, joker)
        await message.channel.send(result)
        print('実行結果: ', result)
    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# Botの起動とDiscordサーバーへの接続
bot.run(token)
