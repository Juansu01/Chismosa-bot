import youtube_dl
import discord
import asyncio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format':"bestaudio"}

async def check_queue(queues, ctx, id):
  if queues[id] != []:
    song = queues[id].pop(0)
    vc = ctx.guild.voice_client
    print(song)
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(song, download=False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      await ctx.send("Playing :woman_tipping_hand::notes: : {}".format(song))
      vc.play(source, after=lambda x=None: asyncio.run(check_queue(queues, ctx, ctx.message.guild.id)))

async def play_song(queues, song, ctx, vc):
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(song, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    await ctx.send("Playing :woman_tipping_hand::notes: : {}".format(song))
    vc.play(source, after=lambda x=None: asyncio.run(check_queue(queues, ctx, ctx.message.guild.id)))
