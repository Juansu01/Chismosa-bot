import discord
import nacl
import os
from dotenv import load_dotenv
from discord.ext import commands
import re
from funcs import *
import asyncio
from discord.ext import tasks
import random
from discord.utils import get
import youtube_dl
from music import play_song, check_queue, search_song
import openai
from musc import Music

music = Music()
activity = discord.Activity(type=discord.ActivityType.listening, name="BLACKPINK")
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='Chismosa ', intents=intents, activity=activity)
load_dotenv()
my_secret = os.getenv('key')
openai_token = os.getenv('openai_token')
client.remove_command('help')
chisme_permissions = ["Shubham#2936", "JuanC#1899"]
all_chismes = get_all_chismes()


def trigger_function():
      asyncio.run(role_routine(client))

@client.event
async def on_member_join(member):
    new_role = discord.utils.get(member.guild.roles, name="Hermanastra")
    await member.add_roles(new_role)

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    if message.content.startswith("test "):
          print("OMG IM HEREE")
          channel = client.get_channel(862591362369191966)
          await channel.send(message.content[5:])
    if message.content.startswith("Gos "):
        openai.api_key = openai_token
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=message.content[4:],
            temperature=0.1,
            max_tokens=1000,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=0
        )
        await message.channel.send(response.choices[0].text)
      
        
    if message.content == "Chismosa help":
        embed = discord.Embed(title="Help with La Chismosa", description="List of Chismosa commands:")
        embed.add_field(name="Chismosa I'm depressed", value="Use this command to get an inspiring message from Jaime Carlos.")
        embed.add_field(name="Chisme", value="Get a chisme from La Chismosa.")
        embed.add_field(name="Days All", value="Displays a list of all members showing the days they have been on the server.")
        embed.add_field(name="Days <username>", value="La Chismosa will tell you the days this user has.")
        embed.add_field(name="My Days", value="La Chismosa will tell you your days.")
        embed.add_field(name="Count our sisters", value="Counts current members")
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
            await role_routine(client)

    if message.content == "Members Count":
        mem_list = get_all_members(client)
        for member in mem_list:
            print("Member: {} Days in server: {}".format(member, get_member_days(member)))

    if message.content == "List Chismes":
        if str(message.author) not in chisme_permissions:
            await message.channel.send("Gurl, you're liek, not allowed to do that :face_with_hand_over_mouth:")
            return
        chisme_list = divide_chunks(get_all_chismes(), 3)
        for chismes in chisme_list:
            await message.channel.send("\n".join(chismes))


    if re.match(re.compile("(Chismosa|chismosa) (I’m|I'm) (depressed)", re.I), message.content):
        quote = get_quote()
        await message.channel.send(quote)

    if re.match(re.compile("(hola|hi|hello|hey) (sister|hermana)", re.I), message.content):
        await message.channel.send("Oula jermana, ya compraste tu paleta de James Charles hoy?:sunglasses:")

    if message.content.lower() == 'chisme':
        while True:
            chisme = get_random_chisme()
            if chisme:
                await message.channel.send(get_random_chisme())
                return

    if re.match(re.compile("chismosa (te|té)", re.I), message.content):
        await message.channel.send("Derrama el té sister!!!:tea:")
    
    if re.match(re.compile("days all", re.I), message.content):
        ctx = await client.get_context(message)
        members = get_all_members(client)
        names = []
        member_dict = {}
        for member in members:
            member_dict[remove_tag(str(member))] = get_member_days(member)
        sorted_member_dict = sorted(member_dict.items(), key=lambda x: x[1], reverse=True)
        for item in sorted_member_dict:  
            names.append("@{}: {} days".format(item[0], item[1]))
        await send_day_list(ctx, names)
       

    if re.match("days [a-z0-9_]+", message.content.lower()):
        members = get_all_members(client)
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
        members = get_all_members(client)
        count = len(members)
        for member in members:
            if member.bot:
                count -= 1
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
        index = int(message.content.split('Del Chisme ',1)[1])
        deleted = delete_chisme(index)
        if deleted:
            await message.channel.send("Ugh I hated that Chisme, it's gone now :face_gun_smiling:")
        else:
            await message.channel.send("Hermanaa, you just gave me a wrong id, estás bien?? :rolling_eyes: ")

        
    if "men" in str(message.content.lower()):
        if "women" in str(message.content.lower()) or "Women" in str(message.content):
            return
        emoji = get(client.emojis, name='face_lip_bite')
        await message.add_reaction(emoji)

    if message.content.startswith("Vamos lá?"):
        await message.channel.send("Está bem, você não sai daí :nail_care::flag_br:")

    if message.content.startswith("Send patch notes"):
        embed = discord.Embed(title="Chismosa Patch Notes v1.7", description="Umghhh, I just added some permissions to some commands xd, remember to use \"Chismosa help\" if you need help with the commands.")
        channel = client.get_channel(862591362369191966)
        await channel.send(content=None, embed=embed)

    if re.match(re.compile("c+h+i+s+m+o+s+a+ +i+ +l+i+k+e+ +m+e+n+", re.I), message.content):
        await message.channel.send("Bien ahí, sigue así, mi nena :woman_tipping_hand:")

    await client.process_commands(message)

@client.event
async def on_ready():
    print("Our bot is logged in as {0.user}".format(client))

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel(862591362369191966)
    voice_client = member.guild.voice_client
    if voice_client is None:
        return
    if len(voice_client.channel.members) == 1:
        player = music.get_player(guild_id=862542952937029632)
        if player:
            player.delete()
        await channel.send("Not you guys leaving me alone :sob::sob::sob:")
        await channel.send("Anyway, bye :rolling_eyes:")
        await voice_client.disconnect()
    

@client.command(pass_context = True)
async def play(ctx, name):
    if "youtube.com" in ctx.message.content or "youtu.be" in ctx.message.content:
        print("yt url")
        url = ctx.message.content[14:]
    else:
        print("Not a yt url")
        name = ctx.message.content[14:]
        result = await search_song(client, 1, name, True)
        url = result[0]
  
    if ctx.author.voice is None:
        await ctx.send("Gurl, join a voice channel pls.")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)
  
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing {song.name}")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Queued {song.name}")


@client.command(pass_context = True)
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
          ctx.guild.voice_client.resume()
          emoji = '\N{DANCER}'
          await ctx.message.add_reaction(emoji)
    else:
          await ctx.send("The song isn't paused sis :woman_tipping_hand:")

@client.command(pass_context = True)
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
          await ctx.send("Gurl, the song is *lik*, already paused :rolling_eyes:")
          return
    ctx.guild.voice_client.pause()
    emoji = '\N{RAISED HAND}'
    await ctx.message.add_reaction(emoji)

@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("I'm not even connected to a voice channel, *liek* wtfff :rolling_eyes:")
    else:
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            player.delete()
        emoji = get(client.emojis, name='face_gun_smiling')
        await ctx.send("Bye girl {}".format(emoji))
        await ctx.voice_client.disconnect()


@client.command(pass_context=True)
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@tasks.loop(hours=12)
async def called_once_a_day():
    channel = client.get_channel(862542970099204098)
    chisme = random.choice(all_chismes)
    chisme = chisme.split()
    chisme.pop(0)
    chisme.pop(0)
    await channel.send(" ".join(chisme))
    await role_routine(client)

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")

called_once_a_day.start()
client.run(my_secret)
