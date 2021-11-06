import logging
import discord
import asyncio
import youtube_dl
from youtube_search import YoutubeSearch
from discord.ext import commands

from mitra.config import DISCORD_TOKEN

logger = logging.getLogger(__name__)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
client = commands.Bot(command_prefix= '.')
pending_requests = []

def run(token):
    client.run(token)

async def play_next(ctx):
    if(ctx.voice_client != None):
        vc = ctx.voice_client
        if len(pending_requests) >= 1:
            obj = pending_requests[0]
            del pending_requests[0]
            vc.play(discord.FFmpegPCMAudio(obj['URL'], **FFMPEG_OPTIONS), after=lambda e:    play_next(ctx))
            asyncio.run_coroutine_threadsafe(ctx.send("Now playing...\n**"+ obj['title'] +"**\n" + obj['video']), client.loop)
        else:
            asyncio.run_coroutine_threadsafe(ctx.send("**No more songs in queue.**"), client.loop)

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('**See you later, 🐊!**')

@client.command(pass_context=True)
async def play(ctx, *, url):

    logger.info (url)

    channel = ctx.message.author.voice.channel
    if ctx.voice_client == None:
        await channel.connect()
    elif (ctx.voice_client != None and ctx.voice_client.channel != channel):
        await ctx.voice_client.channel.disconnect()
        await channel.connect()

    voice = ctx.voice_client
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    if 'https://www.youtu' not in url:
        result = YoutubeSearch(url, max_results=1).to_dict()
        url = 'https://www.youtube.com' + result[0]['url_suffix']

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        obj = {}
        URL = info['formats'][0]['url']
        obj['URL'] = URL
        obj['video'] = url
        obj['title'] = info['title']
    if not voice.is_playing():
        voice.play(discord.FFmpegPCMAudio(obj['URL'], **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
        await ctx.send("Now playing...\n**"+ obj['title'] +"**\n" + obj['video'])
    else:
        pending_requests.append(obj)
        await ctx.send('Song **' + obj['title'] +'** queued...')

@client.command(pass_context=True)
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.send('\n**Paused...**\n')

@client.command(pass_context=True)
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send('\n**Resumed...**\n')

@client.command(pass_context=True)
async def skip(ctx):
    ctx.voice_client.stop()
    await ctx.send('\n**Skipping...**\n')

@client.command(pass_context=True)
async def commands(ctx):
    await ctx.send("\nplay -> play a music or add it to pending requests\npause-> pause the current music\nresume -> resume the current music\nskip -> skip the current music\nlist->list the pending requests\nleave -> leave voice channel\n")

@client.command(pass_context=True)
async def list(ctx):
    result = ''
    for e in pending_requests:
        result += '\n' + e['title']
    await ctx.send('\n**Pending:**\n' + result + '\n')

