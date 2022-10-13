import discord
import random

from discord.ext import commands

bot = commands.Bot(command_prefix = 'f!')

#region Token
token = 'NzgzMTA5NTU3NTc5ODA4NzY5.X8V9mw.Z6irJD7lf_Zh6a4qdag0paWk-Rg'
#endregion

bot_version = 'stable 0.0.3d'


#----------------------------------------------------------#
#------------------------V EVENTS V------------------------#
#----------------------------------------------------------#

# When bot is redy, send message in cmd
@bot.event          
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=discord.Activity(name="f!help", type=1)) #custom status (types: 1 - Playing, 2 - Słucha)

# When user join or left server, send a message in cmd
@bot.event
async def on_member_join(member):
    print(f'{member}has joined a server.')

@bot.event
async def on_member_left(member):
    print(f'{member}has left a server.')

# When command has an error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send('Zla skladnia komendy, sprobuj ponownie.')


#----------------------------------------------------------#
#-----------------------V COMMANDS V-----------------------#
#----------------------------------------------------------#

#region Hello Command
# Command that replies when user say hello to bot
@bot.command(brief='Say hellow to Muto :3')
async def hello(message):
    await message.channel.send("Hello {}".format(message.author.mention))
#endregion

# Version
@bot.command()
async def version(cxt):
    await cxt.send(f"**Obecna wersja:** *{bot_version}*")

# Help
bot.remove_command('help') # Removes default help command 

@bot.command()
async def help(ctx):

    f = open("source_files\command_list\list_of_commands.txt","r")
    list_of_commands = f.read()

    embed=discord.Embed(title="Lista dostępnych komend:", description=list_of_commands, colour=discord.Color.green())
    msg = await ctx.send(embed=embed) # Get bot's message

    await ctx.message.delete() # Delete user's message
    await asyncio.sleep(5)

    await msg.delete() # Delete bot's message

# Changelog
@bot.command()
async def changelog(ctx, haslo=None):

    f = open("changelog.txt","r")
    changelog_read = f.read()

    if(haslo=="bobr"):
        changelog=changelog_read
    else:
        changelog="Ha! Nie znasz hasła :P"

    embed=discord.Embed(title="Lista zmian w wersjach Muto:", description=changelog, colour=discord.Color.green())
    msg = await ctx.send(embed=embed) # Get bot's message

    await ctx.message.delete() # Delete user's message
    await asyncio.sleep(5)

    await msg.delete() # Delete bot's message

#-----------------------V Management V-----------------------#
#region

# Clear Messages
@bot.command()
@commands.has_permissions(manage_messages=True, administrator=True)
async def clear(cxt, amout=5):
    await cxt.channel.purge(limit=amout)
    await cxt.send(f"*Wyczyszczono*  **{amout}** *wiadomości* :recycle:", delete_after=5.0)

# Kick
@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(cxt, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    
    kick_msg = f"{member.mention} *został wykpany przez* {cxt.author.mention}"

    embedKick = discord.Embed(description=kick_msg, color=0x00ff00)
    embedKick.add_field(name="Powód:" ,value=reason, inline=False)
    await cxt.channel.send(embed=embedKick)

# Ban
@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(cxt, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    
    ban_msg = f"{member.mention} *dostał młotkiem od* {cxt.author.mention} *aż zagrzmiało!*"

    embedBan = discord.Embed(description=ban_msg, color=0x00ff00)
    embedBan.add_field(name="Powód:" ,value=reason, inline=False)
    await cxt.channel.send(embed=embedBan)

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

            #unban_msg = f"*The sins of* {user.mention} *has been forgived*"

            #embedUnBan = discord.Embed(description=ban_msg, color=0x00ff00)
            #await cxt.channel.send(embed=embedUnBan)

            return

#endregion
#-----------------------V Fun Commands V-----------------------#
#region

# Hugs, Pats, Boops, Kisses #
#region

# Hug Command
@bot.command()
async def hug(cxt, member : discord.Member):
    hugs = [f"{cxt.author.mention} *hugs* {member.mention}",
            f"{cxt.author.mention} *cuddles to* {member.mention}",
            f"{cxt.author.mention} *comes closely to* {member.mention} *and gives him/her hug*",
            f"{member.mention} *got a big hug from* {cxt.author.mention}"]

    hug_msg = f'{random.choice(hugs)}'

    embedHug = discord.Embed(description=hug_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedHug)

# Pat Command
@bot.command()
async def pat(cxt, member : discord.Member):
    pats = [f"{cxt.author.mention} *pats* {member.mention}",
            f"{cxt.author.mention} *comes to* {member.mention} *and pat him/her*",
            f"{member.mention} *has been patted by* {cxt.author.mention}"]

    pat_msg = f'{random.choice(pats)}'

    embedPat = discord.Embed(description=pat_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedPat)

# Boop Command
@bot.command()
async def boop(cxt, member : discord.Member):
    boops = [f"{cxt.author.mention} *boops* {member.mention}",
            f"{cxt.author.mention} *looked into* {member.mention} *eyes and boop him/her*",
            f"{member.mention} *got a boop from* {cxt.author.mention}"]
    
    boop_msg = f'{random.choice(boops)}'

    embedBoop = discord.Embed(description=boop_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedBoop)

# Kiss Command
@bot.command()
async def kiss(cxt, member : discord.Member):
    kisses = [f"{cxt.author.mention} *kiss* {member.mention}",
            f"{cxt.author.mention} *smooch* {member.mention}",
            f"{cxt.author.mention} *comes closely to* {member.mention} *snouts and gives him/her kiss*",
            f"{member.mention} *got a big kiss from* {cxt.author.mention}"]
    
    kiss_msg = f'{random.choice(kisses)}'

    embedKiss = discord.Embed(description=kiss_msg, color=0x00ff00)
    await cxt.channel.send(embed=embedKiss)

#endregion

#endregion
#-----------------------V Minigames V-----------------------#
#region

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


# Dice Rolls

@bot.command()
async def d4(cxt):
    d4rolls = ["1","2","3","4"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d4rolls)} na kostce D4! :game_die:')

@bot.command()
async def d6(cxt):
    d6rolls = ["1","2","3","4","5","6"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d6rolls)} na kostce D6! :game_die:')

@bot.command()
async def d8(cxt):
    d8rolls = ["1","2","3","4","5","6","7","8"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d8rolls)} na kostce D7! :game_die:')

@bot.command()
async def d10(cxt):
    d10rolls = ["1","2","3","4","5","6","7","8","9","10"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d10rolls)} na kostce D10! :game_die:')

@bot.command(aliases=['d100','d00'])
async def _d100(cxt):
    d100rolls = ["10","20","30","40","50","60","70","80","90","00"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d100rolls)} na kostce D100! :game_die:')

@bot.command()
async def d12(cxt):
    d12rolls = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d12rolls)} na kostce D12! :game_die:')

@bot.command()
async def d20(cxt):
    d20rolls = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
    await cxt.send(f'Wyrzuciłeś {random.choice(d20rolls)} na kostce D20! :game_die:')

#endregion
#-----------------------V Useless Commands V-----------------------#

# Ping
# Command that shows ping between bot and discord server
@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping is: {round(bot.latency * 1000)}ms :arrows_counterclockwise:')

bot.run(token)