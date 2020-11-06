import discord
import time
import config
from discord.ext import commands


bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user) + " in:")
    print(bot.guilds)

@bot.command(aliases=["a"])
async def ascensor(ctx, member: discord.Member):
    guild: discord.Guild = ctx.guild
    chanels = guild.voice_channels
    for channel in chanels:
        await member.move_to(channel)
        time.sleep(1)
    for channel in reversed(chanels):
        await member.move_to(channel)
        time.sleep(1)

@bot.event
async def on_message(message):
    frases = bot.get_channel(718568753268391943)
    if message.author == bot.user:
        return
    if message.channel.id == 453183946264674304:
        await frases.send(message.content)
    await bot.process_commands(message)

bot.run(config.dicordApiKey)
