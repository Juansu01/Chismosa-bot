import discord


async def update_member_role(member, prev_role, new_role):
    """
    Grants the member a new role and removes the previous role
    from their roles.
    """
    await member.add_roles(new_role)
    await member.remove_roles(prev_role)

async def send_bot_help(channel):
    """
    Sends and embedded message with information about the
    Bot's commmands.
    """

    embed = discord.Embed(title="Help with La Chismosa",
                              description="List of Chismosa commands:")
    embed.add_field(name="Chismosa I'm depressed",
                        value="Use this command to get an inspiring message from Jaime Carlos.")
    embed.add_field(name="Chisme", value="Get a chisme from La Chismosa.")
    embed.add_field(name="Days All",
                        value="Displays a list of all members showing" 
                        " the days they have been on the server.")
    embed.add_field(name="Days <username>",
                        value="La Chismosa will tell"
                        " you the days this user has.")
    embed.add_field(name="My Days", value="La Chismosa will tell you your days.")
    embed.add_field(name="Count our sisters", value="Counts current members")
    embed.add_field(name="New Chisme <chisme>", value="Add a new chisme.")
    embed.add_field(name="Del Chisme <number>",
                        value="Deletes a chisme, number is the" 
                        " positon of the chisme in the current chisme list.")
    embed.add_field(name="List Chismes",
                        value="Shows all the chismes that"
                        " La Chismosa is currently holding.")
    embed.add_field(name="Patch notes",
                        value="La Chismosa will send you a"
                        " message with her latest change.")
    embed.add_field(name="Chismosa play <song>",
                        value="La Chismosa will search for the song and play it.")
    embed.add_field(name="Chismosa pause",
                        value="La Chismosa will pause the"
                        " song she is currently playing.")
    embed.add_field(name="Chismosa resume",
                        value="La Chismosa will resume the"
                        " song she was previously playing.")
    embed.add_field(name="Chismosa leave", value="La Chismosa will leave the voice channel.")
    await channel.send(content=None, embed=embed)
