import youtube_dl
import discord
import asyncio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format':"bestaudio"}


async def search_song(client, amount, song, get_url=False):
   info = await client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))

   if len(info["entries"]) == 0: return None
   return [entry["webpage_url"] for entry in info["entries"]] if get_url else info


def check_queue(queues, ctx, id):
  if queues:
    vc = ctx.voice_client
    song = queues.pop(0)
    asyncio.run(play_song(queues, song, ctx, vc))


async def play_song(queues, song, ctx, vc):
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(song, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    await ctx.send("Playing :woman_tipping_hand::notes: : {}".format(song))
    vc.play(source, after=lambda x=None: check_queue(queues, ctx, ctx.message.guild.id))
