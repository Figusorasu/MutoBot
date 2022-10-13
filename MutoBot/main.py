import discord
import random
import os
import time
import socket

from discord.ext import commands, tasks
from datetime import datetime, date

bot = commands.Bot(command_prefix='f!')

# region Token
token = ''
# endregion

loaded_ping = 'Unloaded.'

bot_version = '0.0.3d'


# ------------------------V Bot Functions V------------------------#

# CMD Message when bot is active without timer
def cmdMessage():
    print(f'Muto is Ready :3')
    print(f'Logged in as: {bot.user.name} | ID: {bot.user.id}')
    print(f'Current Version: {bot_version} | discord.py version is {discord.__version__}')
    print("Activation time: ", getTime(), " ", getDate(), "\n")
    # print(f'\nActive extensions:\n')


# Work Time Timer
def workTime():
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    time.sleep(1)

    if hours == 24:
        hours = 0
        days = days + 1
    if minutes == 60:
        minutes = 0
        hours = hours + 1
    if seconds == 60:
        seconds = 0
        minutes = minutes + 1
    else:
        seconds = seconds + 1

    return f'\nBot is active for {days} days, {hours} hours, {minutes} minutes, {seconds} seconds'


# CMD Message when bot is active with timer
def cmdMessageTimer():
    while True:
        working_time = workTime()
        os.system('cls')
        print(f'Muto is Ready :3')
        print(f'Logged in as: {bot.user.name} | ID: {bot.user.id}')
        print(f'Current Version: {bot_version} | discord.py version is {discord.__version__}')
        print(f'{working_time}')
        print(f'\nActive extensions:\n')


# Get current time
def getTime():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return current_time


# Get current date
def getDate():
    today = date.today()
    return today


# Send log in CMD when someone use bot command
def sendLog(commandName, commandAuthor, p1="none", p2="none"):
    time = getTime()
    date = getDate()
    print(f"[{date} / {time}] {commandAuthor} used f!{commandName} command with parametres: {p1}  {p2}")


# ------------------------V COGS V------------------------#


# ------------------------V EVENTS V------------------------#


# When bot is ready, send message in cmd

@bot.event
async def on_ready():
    os.system('cls')
    cmdMessage()
    await bot.change_presence(activity=discord.Activity(name="f!help", type=1))  # custom status


# -----------------------V TASKS V-----------------------#


# -----------------------V COMMANDS V-----------------------#

# Command that replies when user say hello to bot
@bot.command()
async def hello(cxt):
    await cxt.send(f"Hello {cxt.author.mention} :wave:")

    command_name = "hello"
    sendLog(command_name, cxt.author)


# Help
bot.remove_command('help')  # Removes default help command


@bot.command()
async def help(ctx):
    f = open("source_files/command_list/help_command.txt", "r")
    help_commands = f.read()

    embed = discord.Embed(title="Lista dostępnych komend:", description=help_commands, colour=discord.Color.green())
    msg = await ctx.send(embed=embed)  # Get bot's message

    # await ctx.message.delete() # Delete user's message
    # await asyncio.sleep(5)

    # await msg.delete() # Delete bot's message

    command_name = "help"
    sendLog(command_name, cxt.author)


#                    V Management V
# region

# Clear Messages
@bot.command()
@commands.has_permissions(manage_messages=True, administrator=True)
async def clear(cxt, amout=5):
    await cxt.channel.purge(limit=amout + 1)
    await cxt.send(f"*Wyczyszczono*  **{amout}** *wiadomości* :recycle:", delete_after=5.0)

    command_name = "clear"
    sendLog(command_name, cxt.author, amout)


# Kick
@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(cxt, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

    kick_msg = f"{member.mention} *został wykpany przez* {cxt.author.mention}"

    embedKick = discord.Embed(description=kick_msg, color=0x00ff00)
    embedKick.add_field(name="Powód:", value=reason, inline=False)
    await cxt.channel.send(embed=embedKick)

    command_name = "kick"
    sendLog(command_name, cxt.author, member, reason)


# Ban
@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(cxt, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)

    ban_msg = f"{member.mention} *dostał młotkiem od* {cxt.author.mention} *aż zagrzmiało!*"

    embedBan = discord.Embed(description=ban_msg, color=0x00ff00)
    embedBan.add_field(name="Powód:", value=reason, inline=False)
    await cxt.channel.send(embed=embedBan)

    command_name = "ban"
    sendLog(command_name, cxt.author, member, reason)


# Unban
@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'*Winy* {user.mention} *zostały oczyszczone*')

            return

    command_name = "unban"
    sendLog(command_name, cxt.author, member, reason)


# endregion
#                        V Fun Commands V
# region

# SpamPing
@bot.command()
@commands.check(spam_channel)
async def spamping(cxt, member: discord.Member, howManyTimes=5):
    command_name = "spamping"
    sendLog(command_name, cxt.author, member, howManyTimes)

    x = 0
    while x < howManyTimes:
        await cxt.send(f"You've been gnommed! {member.mention}")
        x += 1
        time.sleep(1)

    command_name = "spamping"
    sendLog(command_name, cxt.author, member, howManyTimes)


# Hugs, Pats, Boops, Kisses #
# region

# Hug Command
@bot.command()
async def hug(cxt, member: discord.Member):
    command_name = "hug"
    sendLog(command_name, cxt.author, member)

    hugs = [f"{cxt.author.mention} *hugs* {member.mention}",
            f"{cxt.author.mention} *cuddles to* {member.mention}",
            f"{cxt.author.mention} *comes closely to* {member.mention} *and gives him/her hug*",
            f"{member.mention} *got a big hug from* {cxt.author.mention}"]

    hug_msg = f'{random.choice(hugs)}'

    embedHug = discord.Embed(description=hug_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedHug)


# Pat Command
@bot.command()
async def pat(cxt, member: discord.Member):
    command_name = "pat"
    sendLog(command_name, cxt.author, member)

    pats = [f"{cxt.author.mention} *pats* {member.mention}",
            f"{cxt.author.mention} *comes to* {member.mention} *and pat him/her*",
            f"{member.mention} *has been patted by* {cxt.author.mention}"]

    pat_msg = f'{random.choice(pats)}'

    embedPat = discord.Embed(description=pat_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedPat)


# Boop Command
@bot.command()
async def boop(cxt, member: discord.Member):
    command_name = "boop"
    sendLog(command_name, cxt.author, member)

    boops = [f"{cxt.author.mention} *boops* {member.mention}",
             f"{cxt.author.mention} *looked into* {member.mention} *eyes and boop him/her*",
             f"{member.mention} *got a boop from* {cxt.author.mention}"]

    boop_msg = f'{random.choice(boops)}'

    embedBoop = discord.Embed(description=boop_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedBoop)


# Kiss Command
@bot.command()
async def kiss(cxt, member: discord.Member):
    command_name = "kiss"
    sendLog(command_name, cxt.author, member)

    kisses = [f"{cxt.author.mention} *kiss* {member.mention}",
              f"{cxt.author.mention} *smooch* {member.mention}",
              f"{cxt.author.mention} *comes closely to* {member.mention} *snouts and gives him/her kiss*",
              f"{member.mention} *got a big kiss from* {cxt.author.mention}"]

    kiss_msg = f'{random.choice(kisses)}'

    embedKiss = discord.Embed(description=kiss_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedKiss)


# endregion

# endregion
#                        V Minigames V
# region

# 8ball Game
@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["To pewne.",
                 "Zdecydowanie tak.",
                 "Bez wątpienia.",
                 "Tak - zdecydowanie.",
                 "Możesz na tym polegać.",
                 "Tak, widzę to.",
                 "Najprawdopodobniej.",
                 "Dobra perspektywa.",
                 "Tak.",
                 "Znaki wskazują na tak.",
                 "Odpowiedź jest niewyraźna, spróbuj ponownie.",
                 "Zapytaj ponownie później.",
                 "Lepiej ci teraz nie mówić.",
                 "Ciężko powiedzieć.",
                 "Przemyśl to i zapytaj ponownie.",
                 "Nie licz na to.",
                 "Moja odpowiedź brzmi: nie",
                 "Moje źródła mówią nie.",
                 "Kiepska perspektywa.",
                 "Bardzo wątpliwe.",
                 "Nie.",
                 "Myślę, że to zły pomysł.",
                 "Może powinieneś wyjść na zewnątrz.",
                 "OMG, naprawdę? NIE!",
                 "Emm ... Myślę, że to trochę dziwne.",
                 "Nie jestem co do tego pewien."]

    await ctx.send(f'**Pytanie:** {question}\n**Odpowiedź:** {random.choice(responses)}')

    command_name = "8ball"
    sendLog(command_name, cxt.author, question)


# Dice Rolls

@bot.command()
async def d4(cxt):
    d4rolls = ["1", "2", "3", "4"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d4rolls)} na kostce D4! :game_die:')

    command_name = "d4"
    sendLog(command_name, cxt.author)


@bot.command()
async def d6(cxt):
    d6rolls = ["1", "2", "3", "4", "5", "6"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d6rolls)} na kostce D6! :game_die:')

    command_name = "d6"
    sendLog(command_name, cxt.author)


@bot.command()
async def d8(cxt):
    d8rolls = ["1", "2", "3", "4", "5", "6", "7", "8"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d8rolls)} na kostce D7! :game_die:')

    command_name = "d8"
    sendLog(command_name, cxt.author)


@bot.command()
async def d10(cxt):
    d10rolls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d10rolls)} na kostce D10! :game_die:')

    command_name = "d10"
    sendLog(command_name, cxt.author)


@bot.command(aliases=['d100', 'd00'])
async def _d100(cxt):
    d100rolls = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "00"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d100rolls)} na kostce D100! :game_die:')

    command_name = "d100"
    sendLog(command_name, cxt.author)


@bot.command()
async def d12(cxt):
    d12rolls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d12rolls)} na kostce D12! :game_die:')

    command_name = "12"
    sendLog(command_name, cxt.author)


@bot.command()
async def d20(cxt):
    d20rolls = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                "20"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d20rolls)} na kostce D20! :game_die:')

    command_name = "20"
    sendLog(command_name, cxt.author)


# endregion

bot.run(token)
