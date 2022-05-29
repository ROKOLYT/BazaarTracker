import discord
from discord.ext import commands
import asyncio
import sys
from handlingData import handleData
from menu import startBuild
import configparser
import random

active = False
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def startBot(client, bToken):
    try:
        client.run(bToken)
    except Exception as e:
        print('Error attempting to launch bot: ', e)
        print('you might find luck checking your info.ini file for any mistakes. ')
        e = input('Press enter to close')
        sys.exit()


def main():
    config = configparser.ConfigParser()
    config.read('info.ini')
    try:
        config['INFO']['BotToken'] = config['INFO']['BotToken']
    except KeyError:
        with open('info.ini', 'w') as cfgFile:
            config['INFO'] = {'bottoken': ''}
            config.write(cfgFile)
    if config['INFO']['BotToken'] == '':
        config['INFO']['BotToken'] = input('Please enter your bot token:')
    bToken = config['INFO']['BotToken']
    with open('info.ini', 'w') as cfg:
        config.write(cfg)
    client = commands.Bot(command_prefix='>')
    data = handleData('https://api.hypixel.net/skyblock/bazaar')

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Game('>'))
        print(f'Bot is Ready. Logged in as {client.user}')

    @client.command()
    async def info(ctx):
        global active
        active = True
        await startBuild(ctx, client, data)
        active = False

    def check(message):
        usr_number = int(message.content)
        return usr_number

    @client.command()
    async def roll(ctx, usr_number: int):
        num = random.randrange(1, 10)
        while True:
            if num == usr_number:
                await ctx.send(f'You won the number was indeed {num}')
                break
            else:
                await ctx.send(f'Keep on guessing')
                usr_number = await client.wait_for('message', timeout=20.0, check=check)
                usr_number = int(usr_number.content)
    startBot(client, bToken)


if __name__ == '__main__':
    main()
