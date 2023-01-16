from datetime import date
import random
import json

import DiscordUtils
import discord
import requests
from discord.utils import get
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from chismes import Chismes

user = "chismosa_dev"
passw = "chismosa_dev_pwd"
host = "localhost"
db = "chismosa_dev_db"


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


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


def get_all_members(client):
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
    engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_size=20, max_overflow=0,
                           pool_pre_ping=True)
    with Session(engine) as session:
        chismes = session.query(Chismes).all()
        if chismes:
            chisme = random.choice(chismes)
            return chisme.__dict__.get('content')
        else:
            return "No chismes, you should add some."


def get_all_chismes():
    engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_size=20, max_overflow=0,
                           pool_pre_ping=True)
    chisme_list = []
    with Session(engine) as session:
        chismes = session.query(Chismes).all()
    for chisme in chismes:
        chis_to_dict = chisme.__dict__
        chisme_list.append(f"id:{chis_to_dict.get('id')} chisme: {chis_to_dict.get('content')}")
    return chisme_list


def update_chismes(chisme):
    engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_size=20, max_overflow=0,
                           pool_pre_ping=True)
    with Session(engine) as session:
        new_chisme = Chismes(content=chisme)
        session.add(new_chisme)
        session.commit()


def delete_chisme(index):
    engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_size=20, max_overflow=0,
                           pool_pre_ping=True)
    with Session(engine) as session:
        chisme = session.get(Chismes, index)
        if chisme:
            session.delete(chisme)
            session.commit()
            return True
    return False


async def role_routine(client):
    role_list = ["Sister.💁‍♀️", "Sister Menor.🙆‍♀️", "Hermana del Medio.💇‍♀️", "Sister Mayor.🙇‍♀️"]
    channel = client.get_channel(862591362369191966)
    member_list = get_all_members(client)
    change_list = [[], [], [], []]
    for member in member_list:
        print("Checking: {}".format(member))
        days = get_member_days(member)
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
                print("Granting: {} role: Sister".format(member))
                change_list[0].append("{} is now a Sister! 💁‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 90 and days < 180:
            new_role = get(member.guild.roles, name="Sister Menor")
            old_role = get(member.guild.roles, name="Sister")
            if new_role not in roles:
                print("Granting: {} role: Sister Menor".format(member))
                change_list[1].append("{} is now a Sister Menor! 🙆‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 180 and days < 300:
            new_role = get(member.guild.roles, name="Hermana del Medio")
            old_role = get(member.guild.roles, name="Sister Menor")
            if new_role not in roles:
                print("Granting: {} role: Hermana del Medio".format(member))
                change_list[2].append("{} is now a Hermana del Medio! 💇‍♀️".format(remove_tag(str(member))))
                await member.add_roles(new_role)
                await member.remove_roles(old_role)
        elif days >= 300:
            new_role = get(member.guild.roles, name="Sister Mayor")
            old_role = get(member.guild.roles, name="Hermana del Medio")
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

