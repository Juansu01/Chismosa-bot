import requests
import json
from replit import db
import discord
from discord.utils import get
import random
from datetime import date


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
    return(quote)

def get_chisme():
    chisme = requests.get('https://jasonpersonaldomain.com/chismosabot/random')
    json_data = json.loads(chisme.text)
    quote = json_data['quote']['quote']
    return quote

def update_chismes(chisme):
    if "chismes" in db.keys():
        chismes = list(db["chismes"])
        chismes.append(chisme)
        db["chismes"] = chismes
    else:
        db["chismes"] = chisme

def delete_chisme(index):
    chismes = db["chismes"]
    if len(chismes) > index:
        del chismes[index]
        db["chismes"] = chismes
        return True
    else:
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

    channel = client.get_channel(862542970099204098)
    # await channel.send(random.choice(db["chismes"]))