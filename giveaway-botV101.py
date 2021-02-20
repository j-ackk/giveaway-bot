import discord
from discord.ext import commands
import asyncio
import random
import datetime
import os

# Prefix is set to g! for all commands
client = commands.Bot(command_prefix = 'g!')

@client.event
async def on_ready():
    # Prints a message when the bot is online and functioning
    await client.change_presence(status=discord.Status.online, activity = discord.Game(name=f'g!help for a list of commands! 🥳 🎉 Currently in {len(client.guilds)} servers! 🎉'))
    print('Ready to giveaway!')

@client.command()
async def version(ctx):
    # Version command that contains the current version number and recent changes made
    ver = discord.Embed(color = 0x7289da)
    ver.set_author(name = 'Update Notes', icon_url= '')
    ver.add_field(name = 'Version: 1.00', value = f'The bot was created on February 19th, 2021.\nThe following commands where added to the bot:\nhelpme\nversion\ngiveaway\nreroll.', inline= False)
    await ctx.send(embed = ver)

@client.command()
async def helpme(ctx):
    # Help command that lists the current available commands and describes what they do
    ghelp = discord.Embed(color = 0x7289da)
    ghelp.set_author(name = 'Commands/Help', icon_url = '')
    ghelp.add_field(name= 'helpme', value = 'This command took you here!', inline = False)
    ghelp.add_field(name= 'version', value = 'Displays the current version number and recent updates.', inline = False)
    ghelp.add_field(name= 'giveaway `seconds` `prize`', value = '__Can only be accessed by users with the "Giveaway Host" role.__\nStarts a giveaway for the server!', inline = False)
    ghelp.add_field(name= 'reroll `message id`', value = '__Can only be accessed by users with the "Giveaway Host" role.__\nThey must follow the command with the copied message id from the giveaway.', inline = False)
    ghelp.set_footer(text = 'Use the prefix "g!" before all commands!')
    await ctx.send(embed = ghelp)

@client.command()
@commands.has_role("Giveaway Host")
async def giveaway(ctx, mins:int, *, prize:str):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly
    # Giveaway embed message
    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'{prize} GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'{ctx.author.name} is hosting a giveaway!', value = f'React with 🎉 to enter! @everyone\n Ends in {mins/60} minutes!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)
    give.set_footer(text = f'Giveaway ends at {end} UTC!')
    my_message = await ctx.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(mins)

    new_message = await ctx.channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entries**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await ctx.send(embed = winning_announcement)

@client.command()
@commands.has_role("Giveaway Host")
async def reroll(ctx, id_ : int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await ctx.channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return
    
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'The giveaway was re-rolled by a host!', icon_url = 'https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name = f'🥳 New Winner:', value = f'{winner.mention}', inline = False)
    await ctx.send(embed = reroll_announcement)

# Bot token
client.run(os.environ.get('giveawaybot_pass'))