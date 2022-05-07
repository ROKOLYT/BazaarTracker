import discord
from discord.ext import commands
import asyncio
import sys
from handlingData import handleData
from menu import startBuild
import configparser

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

    startBot(client, bToken)


if __name__ == '__main__':
    main()
