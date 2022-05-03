import discord
import asyncio
import json
from itertools import islice


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


async def startBuild(ctx, client, data):
    def check(reaction, user):
        return str(reaction.emoji) in ['\N{black rightwards arrow}', '\N{leftwards black arrow}',
                                       '\N{white heavy check mark}'] and user != client.user

    @client.event
    async def on_message(message):
        if str(message.content).lower() != '>info' and message.author != client.user:
            await message.delete()
        try:
            msg = int(message.content)

            with open('numbers.json', 'r') as jsonFile:
                numbers = json.load(jsonFile)
            prices = data.returnPrices(numbers[str(msg)])
            embed = discord.Embed(color=0xdd0303)
            dataStr = f"**sell Price: {round(prices['sellPrice'], 3)}**\n**buy Price: {round(prices['buyPrice'], 3)}**"
            embed.add_field(name=prices['name'], value=dataStr, inline=True)
            await message.channel.send(embed=embed)
        except ValueError:
            pass
        await client.process_commands(message)

    await ctx.message.delete()
    cp = 1
    embeds = getEmbeds()
    messagen = await ctx.send(embed=embeds[cp - 1])
    await messagen.add_reaction('\N{white heavy check mark}')
    await messagen.add_reaction('\N{black rightwards arrow}')
    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await messagen.delete()
            await ctx.author.send("Finished.")
            break
        if str(reaction.emoji) == '\N{leftwards black arrow}':
            cp -= 1
            await messagen.clear_reaction(str(reaction.emoji))
            await messagen.edit(embed=embeds[cp - 1])
            if 1 < cp < 21:
                await messagen.add_reaction('\N{leftwards black arrow}')
                await messagen.add_reaction('\N{black rightwards arrow}')
            if cp == 1:
                await messagen.clear_reaction('\N{leftwards black arrow}')
        elif str(reaction.emoji) == '\N{black rightwards arrow}':
            cp += 1
            await messagen.clear_reaction(str(reaction.emoji))
            await messagen.edit(embed=embeds[cp-1])
            if 1 < cp < 21:
                await messagen.add_reaction('\N{leftwards black arrow}')
                await messagen.add_reaction('\N{black rightwards arrow}')
            if cp == 21:
                await messagen.clear_reaction('\N{black rightwards arrow}')
        elif str(reaction.emoji) == '\N{white heavy check mark}':
            await messagen.delete()
            break
        else:
            pass



def getEmbeds():
    ndict = {}
    newList = []
    with open('names.json', 'r') as namesJson:
        names = json.load(namesJson)
    myList = []
    for item in chunks({i: i for i in names}, 20):
        myList.append(item)
    for i in myList:
        for k in i:
            ndict[k] = names[k]
        newList.append(ndict)
        ndict = {}
    embed = []
    valueString = ''
    c = 1
    for i in range(len(newList)):
        embed.append(discord.Embed(color=0xdd0303))
        for k in newList[i]:
            valueString += f'{c} '
            valueString += newList[i][k]
            valueString += '\n'
            c += 1
        embed[i].add_field(name=f"Page {i+1}", value=valueString, inline=True)
        valueString = ''
    return embed



