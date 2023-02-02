import random
import json
import os

from datetime import date
import youtube_dl
import requests
import DiscordUtils
import discord
from discord.utils import get
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import user_management_functions as umf
from chismes import Chismes



load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

def get_engine():
    """
    Returns engine object.
    """
    engine = create_engine(f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{HOST}/{DB_NAME}',
                           pool_size=20, max_overflow=0,
                           pool_pre_ping=True)

    return engine


def divide_chunks(my_list, size):
    """
    Takes in a list and yields chunks of length size.
    """
    for i in range(0, len(my_list), size):
        yield my_list[i:i + size]


def get_channel_id(channels, name):
    """
    Takes in a list of channels to find the channel
    that matches the name argument.
    """
    for channel in channels:
        if channel.name.lower() == name.lower():
            return channel.id

    return None



async def send_day_list(ctx, member_list):
    lis = list(divide_chunks(member_list, 15))
    embeds = []
    print(lis)
    for i, arr in enumerate(lis):
        embeds.append(discord.Embed(color=ctx.author.color).add_field(name=f"Page {i + 1}", value="\n".join(arr)))
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    await paginator.run(embeds)


def get_all_members(client, ctx):
    guild = client.get_guild(ctx.guild.id)
    member_list = guild.members
    return member_list


def get_member_days(ctx):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    member_join_date = ctx.author.joined_at.strftime("%d/%m/%Y")
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


def remove_tag(username):
    chars = []
    for char in username:
        if char == '#':
            break
        chars.append(char)
    return "".join(chars)


def get_quote():
    response = requests.get("http://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -James Charles"
    return (quote)


def get_random_chisme():
    engine = get_engine()
    with Session(engine) as session:
        chismes = session.query(Chismes).all()
        if chismes:
            chisme = random.choice(chismes)
            return chisme.__dict__.get('content')
        else:
            return "No chismes, you should add some."


def get_all_chismes():
    engine = get_engine()
    chisme_list = []
    with Session(engine) as session:
        chismes = session.query(Chismes).all()
    for chisme in chismes:
        chis_to_dict = chisme.__dict__
        chisme_list.append(f"id:{chis_to_dict.get('id')} chisme: {chis_to_dict.get('content')}")
    return chisme_list


def update_chismes(chisme):
    engine = get_engine()
    with Session(engine) as session:
        new_chisme = Chismes(content=chisme)
        session.add(new_chisme)
        session.commit()


def delete_chisme(index):
    engine = get_engine()
    with Session(engine) as session:
        chisme = session.get(Chismes, index)
        if chisme:
            session.delete(chisme)
            session.commit()
            return True
    return False


async def role_routine(client, ctx):
    role_list = ["Sister.💁‍♀️", "Sister Menor.🙆‍♀️", "Hermana del Medio.💇‍♀️", "Sister Mayor.🙇‍♀️"]
    channel = client.get_channel(get_channel_id(ctx.guild.channels, "General"))
    member_list = get_all_members(client, ctx)
    change_list = [[], [], [], []]
    for member in member_list:
        print(f"Checking: {format(member)}")
        days = get_member_days(ctx)
        roles = member.roles
        role = get(member.guild.roles, name="Spambot 🤖")
        role2 = get(member.guild.roles, name="Music Bot 🎶")
        role3 = get(member.guild.roles, name="Bots Extra")
        if role in roles or role2 in roles or role3 in roles:
            continue
        if days >= 30 and days < 90:
            new_role = get(member.guild.roles, name="Sister")
            old_role = get(member.guild.roles, name="Hermanastra")
            if new_role not in roles:
                await umf.update_member_role(member, old_role, new_role)
                change_list[0].append(f"{remove_tag(str(member))} is now a Sister! 💁‍♀️")
                
        elif days >= 90 and days < 180:
            new_role = get(member.guild.roles, name="Sister Menor")
            old_role = get(member.guild.roles, name="Sister")
            if new_role not in roles:
                
                change_list[1].append(f"{remove_tag(str(member))} is now a Sister Menor! 🙆‍♀️")
        elif days >= 180 and days < 300:
            new_role = get(member.guild.roles, name="Hermana del Medio")
            old_role = get(member.guild.roles, name="Sister Menor")
            if new_role not in roles:
                
                change_list[2].append(f"{remove_tag(str(member))} is now a Hermana del Medio! 💇‍♀️")
        elif days >= 300:
            new_role = get(member.guild.roles, name="Sister Mayor")
            old_role = get(member.guild.roles, name="Hermana del Medio")
            if new_role not in roles:
                await umf.update_member_role(member, old_role, new_role)
                change_list[3].append(f"{remove_tag(str(member))} is now a Sister Mayor! 🙇‍♀️")

    for i, role_update in enumerate(change_list):
        if len(role_update) == 1:
            await channel.send(role_update[0])
        elif len(role_update) > 1:
            names = []
            for memb in role_update:
                names.append(memb.split(' is')[0])
            names = ", ".join(names)
            role_name, emoji = role_list[i].split(".")
            await channel.send(f"{names} are now {role_name}!!!{emoji}")


async def search_song(client, amount, song, get_url=False):
    """
    Searches for a song on YouTube using YouTubeDL
    If entries for the song are found they will be returned,
    otherwise None will be returned.
    """
    info = await client.loop.run_in_executor(None,
        lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}
        ).extract_info(f"ytsearch{amount}:{song}",
                       download=False,
                       ie_key="YoutubeSearch")
   )

    if len(info["entries"]) == 0:
        return None

    return [entry["webpage_url"] for entry in info["entries"]] if get_url else info
