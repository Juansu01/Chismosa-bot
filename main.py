import discord
import nacl
import os
from discord.ext import commands
from datetime import date
from dotenv import load_dotenv
import re
from utils import remove_tag, get_chisme, get_quote, update_chismes, delete_chisme
import asyncio
from discord.ext import tasks
from replit import db
from keep_alive import keep_alive
import random
from discord.utils import get
import youtube_dl
import pafy


activity = discord.Activity(type=discord.ActivityType.listening, name="BLACKPINK")
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='Chismosa ', intents=intents, activity=activity)
load_dotenv('.env')
my_secret = os.environ['key']
client.remove_command('help')


chisme_permissions = ["Shubham#2936", "JuanC#1899"]

async def search_song(amount, song, get_url=False):
   info = await client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))

   if len(info["entries"]) == 0: return None
   return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

def trigger_function():
  asyncio.run(role_routine())
def get_all_members():
    guild = client.get_guild(862542952937029632)
    memberList = guild.members
    return memberList

def get_member_days(member):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    mem_join = member.joined_at
    member_join_date = mem_join.strftime("%d/%m/%Y")
    date0 = d1
    date1 = member_join_date
    day0 = int(date0[:2])
    morep0 = date0.replace("/", "")
    month0 = int(morep0[2:-4])
    year0 = int(date0[6:])
    day1 = int(date1[:2])
    morep1 = date1.replace("/", "")
    month1 = int(morep1[2:-4])
    year1 = int(date1[6:])
    date0 = date(year0, month0, day0)
    date1 = date(year1, month1, day1)
    delta = date0 - date1
    return delta.days

async def role_routine():
    role_list = ["Sister.💁‍♀️", "Sister Menor.🙆‍♀️", "Hermana del Medio.💇‍♀️", "Sister Mayor.🙇‍♀️"]
    channel = client.get_channel(862591362369191966)
    member_list = get_all_members()
    change_list = [[], [], [], []]
    for member in member_list:
        print("Checking: {}".format(member))
        days = get_member_days(member)
        roles = member.roles
        role = discord.utils.get(member.guild.roles, name="Spambot 🤖")
        role2 = discord.utils.get(member.guild.roles, name="Music Bot 🎶")
        if role in roles or role2 in roles:
            continue
        if days >= 30 and days < 90:
            new_role = discord.utils.get(member.guild.roles, name="Sister")
            old_role = discord.utils.get(member.guild.roles, name="Hermanastra")
            if new_role not in roles:
                print("Granting: {} role: Sister".format(member))
                change_list[0].append("{} is now a Sister! 💁‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 90 and days < 180:
            new_role = discord.utils.get(member.guild.roles, name="Sister Menor")
            old_role = discord.utils.get(member.guild.roles, name="Sister")
            if new_role not in roles:
                print("Granting: {} role: Sister Menor".format(member))
                change_list[1].append("{} is now a Sister Menor! 🙆‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 180 and days < 300:
            new_role = discord.utils.get(member.guild.roles, name="Hermana del Medio")
            old_role = discord.utils.get(member.guild.roles, name="Sister Menor")
            if new_role not in roles:
                print("Granting: {} role: Hermana del Medio".format(member))
                change_list[2].append("{} is now a Hermana del Medio! 💇‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 300:
            new_role = discord.utils.get(member.guild.roles, name="Sister Mayor")
            old_role = discord.utils.get(member.guild.roles, name="Hermana del Medio")
            if new_role not in roles:
                print("Granting: {} role: Sister Mayor".format(member))
                change_list[3].append("{} is now a Sister Mayor! 🙇‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
    
    for i, lis in enumerate(change_list):
      if len(lis) == 1:
        await channel.send(lis[0])
      elif len(lis) > 1:
        names = []
        for memb in lis:
          names.append(memb.split(' is')[0])
        names = ", ".join(names)
        role_name, emoji = role_list[i].split(".")
        await channel.send(f"{names} are now {role_name}!!!{emoji}")

    channel = client.get_channel(862542970099204098)
    await channel.send(random.choice(db["chismes"]))

@client.event
async def on_member_join(member):
    new_role = discord.utils.get(member.guild.roles, name="Hermanastra")
    await member.add_roles(new_role)

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "Chismosa help":
        embed = discord.Embed(title="Help with La Chismosa", description="List of Chismosa commands:")
        embed.add_field(name="Chismosa I'm depressed", value="Use this command to get an inspiring message from Jaime Carlos.")
        embed.add_field(name="Chisme", value="Get a chisme from La Chismosa.")
        embed.add_field(name="Days All", value="Displays a list of all members showing the days they have been on the server.")
        embed.add_field(name="Days <username>", value="La Chismosa will tell you the days this user has.")
        embed.add_field(name="My Days", value="La Chismosa will tell you your days.")
        embed.add_field(name="Members Count", value="Counts current members, including bots, 'cus bots are also sisterss.")
        embed.add_field(name="New Chisme <chisme>", value="Add a new chisme.")
        embed.add_field(name="Del Chisme <number>", value="Deletes a chisme, number is the positon of the chisme in the current chisme list.")
        embed.add_field(name="List Chismes", value="Shows all the chismes that La Chismosa is currently holding.")
        embed.add_field(name="Patch notes", value="La Chismosa will send you a message with her latest change.")
        embed.add_field(name="Chismosa play <song>", value="La Chismosa will search for the song and play it.")
        embed.add_field(name="Chismosa pause", value="La Chismosa will pause the song she is currently playing.")
        embed.add_field(name="Chismosa resume", value="La Chismosa will resume the song she was previously playing.")
        embed.add_field(name="Chismosa leave", value="La Chismosa will leave the voice channel.")
        await message.channel.send(content=None, embed=embed)

    if message.content == "do routine":
        if str(message.author) == "JuanC#1899":
          print("im here")
          await role_routine()

    if message.content == "Members Count":
        mem_list = get_all_members()
        for member in mem_list:
            print("Member: {} Days in server: {}".format(member, get_member_days(member)))

    if message.content == "List Chismes":
      chisme_list = list(db["chismes"])
      tuple_list = []
      for (i, item) in enumerate(chisme_list , start=1):
          tuple_list.append("({}) {}".format(i, item))
      for i in range(0, len(tuple_list), 3):
        await message.channel.send("\n".join(tuple_list[i:i + 3]))


    if re.match(re.compile("(Chismosa|chismosa) (I’m|I'm) (depressed)", re.I), message.content):
        quote = get_quote()
        await message.channel.send(quote)

    if re.match(re.compile("(hola|hi|hello|hey) (sister|hermana)", re.I), message.content):
        await message.channel.send("Oula jermana, ya compraste tu paleta de James Charles hoy?:sunglasses:")

    if message.content.lower() == 'chisme':
        try:
            await message.channel.send(random.choice(db["chismes"]))
        except:
            await message.channel.send("We don't have any chismes yet")

    if re.match(re.compile("chismosa (te|té)", re.I), message.content):
        await message.channel.send("Derrama el té sister!!!:tea:")
    
    if re.match(re.compile("days all", re.I), message.content):
        members = get_all_members()
        names = []
        member_dict = {}
        for member in members:
            member_dict[remove_tag(str(member))] = get_member_days(member)
        sorted_member_dict = sorted(member_dict.items(), key=lambda x: x[1], reverse=True)
        for item in sorted_member_dict:  
            names.append("@{}: {} days".format(item[0], item[1]))
        await message.channel.send("\n".join(names))

    if re.match("days [a-z0-9_]+", message.content.lower()):
        members = get_all_members()
        username = message.content.split()[1]
        print(username)
        for member in members:
            if remove_tag(str(member)).lower() == username.lower():
                print(member, username)
                await message.channel.send("@{} has been in the server for {} days!".format(remove_tag(str(member)), get_member_days(member)))

    if re.match(re.compile("my days", re.I), message.content):
        await message.channel.send("@{} has been in the server for {} days!".format(remove_tag(str(message.author)), get_member_days(message.author)))

    if re.match(re.compile("chismosa no hablo ingl(é|e)s", re.I), message.content):
        await message.channel.send("Omg, tienes que descargar Duolingou :mobile_phone:")

    if re.search(re.compile("(p+u+t+a+|p+u+t+o+|f+u+c+k+|f+a+g+o*t*|s+h+i+t+|b+i+t+c+h+|c+u+n+t+)", re.I), message.content):
        await message.channel.send("Watch your language sister!:nail_care:")

    if re.search(re.compile("s+h+o+(pp)+i+n+g+", re.I), message.content):
        await message.channel.send("Omg did someone say shopping!:shopping_bags:")

    if re.match(re.compile("s+e+n+d+ n+u+d+e+s+", re.I), message.content):
        await message.channel.send("At least take me to dinner first!:flushed:")
    
    if re.search(re.compile("(l+i+k+e+|l+o+v+e+)", re.I), message.content):
        n = random.randint(0, 1)
        if n == 0:
          await message.channel.send("i… LOVE :woman_gesturing_ok:")
        else:
          await message.channel.send("I literally LOVE :woman_gesturing_ok:")

    if message.content == "Count our sisters":
        members = get_all_members()
        count = len(members)
        await message.channel.send("We currently have {} sisters :woman_technologist: ".format(count))

    if message.content.startswith("New Chisme"):
        if str(message.author) not in chisme_permissions:
            await message.channel.send("Gurl, you're liek, not allowed to do that :face_with_hand_over_mouth:")
            return
        chisme = str(message.content).replace("New Chisme ", "")
        update_chismes(chisme)
        await message.channel.send("Ummhgg, qué buen chisme hermana, tengo que guardarlo :woman_tipping_hand:")

    if message.content.startswith("Del Chisme"):
        if str(message.author) not in chisme_permissions:
              await message.channel.send("Gurl, you're liek, not allowed to do that :face_with_hand_over_mouth:")
              return
        if 'chismes' in db.keys():
            index = int(message.content.split('Del Chisme ',1)[1])
            index = index - 1
            print(index)
            res = delete_chisme(index)
            if res == True:
                await message.channel.send("Ugh I hated that Chisme, it's gone now :face_gun_smiling:")
            else:
                await message.channel.send("Hermanaa, we don't have that many chismes :pinching_hand:")
        
    if "men" in str(message.content.lower()):
        if "women" in str(message.content.lower()) or "Women" in str(message.content):
            return
        emoji = get(client.emojis, name='face_lip_bite')
        await message.add_reaction(emoji)

    if message.content.startswith("Vamos lá?"):
        await message.channel.send("Está bem, você não sai daí :nail_care::flag_br:")

    if message.content.startswith("Patch notes"):
        embed = discord.Embed(title="Chismosa Patch Notes v1.6", description="Hiii sisters!!! This new chismosa patch brings a brand new feature, la chismosa can now play music, use the command \"Chismosa help\" if you want to know how to use this new feature.")
        await message.channel.send(content=None, embed=embed)

    if re.match(re.compile("c+h+i+s+m+o+s+a+ +i+ +l+i+k+e+ +m+e+n+", re.I), message.content):
      await message.channel.send("Bien ahí, sigue así, mi nena :woman_tipping_hand:")

    await client.process_commands(message)

@client.event
async def on_ready():
    print("Our bot is logged in as {0.user}".format(client))
    channel = client.get_channel(862591362369191966)
    embed = discord.Embed(title="Chismosa Patch Notes v1.6", description="Hiii sisters!!! This new chismosa patch brings a brand new feature, la chismosa can now play music, use the command \"Chismosa help\" if you want to know how to use this new feature.")
    await channel.send(content=None, embed=embed)
    

@client.command(pass_context = True)
async def play(ctx, url):
  if ctx.voice_client:
    ctx.voice_client.stop()
  url = ctx.message.content[14:]
  if ctx.author.voice is None:
    await ctx.send("Gurl, join a voice channel pls.")
  channel = ctx.author.voice.channel
  if ctx.voice_client is None:
    await channel.connect()
  else:
    await ctx.voice_client.move_to(channel)

  result = await search_song(1, url, get_url=True)
  song = result[0]
  print(song)

  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  YDL_OPTIONS = {'format':"bestaudio"}

  vc = ctx.voice_client

  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(song, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    await ctx.send("Playing :woman_tipping_hand::notes: : {}".format(song))
    vc.play(source)

@client.command(pass_context = True)
async def resume(ctx):
    await ctx.guild.voice_client.resume()

@client.command(pass_context = True)
async def pause(ctx):
    await ctx.guild.voice_client.pause()

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client is None:
      await ctx.send("I'm not even connected to a voice channel, *liek* wtfff :rolling_eyes:")
    else:
      await ctx.send("Bye girl :face_gun_smiling:")
      await ctx.guild.voice_client.disconnect()

@tasks.loop(hours=24)
async def called_once_a_day():
    await role_routine()

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")
called_once_a_day.start()

keep_alive()
client.run(my_secret)
