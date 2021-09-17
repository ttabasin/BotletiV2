import discord
import time
import config
from discord.ext import commands
import youtube_dl
import os

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
        # time.sleep(1)
    for channel in reversed(chanels):
        await member.move_to(channel)
        # time.sleep(1)


@bot.command(aliases=["p"])
async def play(ctx, url: str):
    songThere = os.path.isfile("song.webm")
    connected = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        if songThere:
            os.remove("song.webm")
    except PermissionError:
        return
    channel = ctx.message.author.voice.channel
    if not connected:
        await channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': '249/250/251',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    voice.play(discord.FFmpegOpusAudio("song.webm"))


@bot.command(aliases=["d"])
async def disconnect(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command(aliases=["r"])
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.event
async def on_message(message):
    frases = bot.get_channel(718568753268391943)
    if message.author == bot.user:
        return
    if message.channel.id == 453183946264674304:
        await frases.send(message.content)
    await bot.process_commands(message)

bot.run(config.token)
