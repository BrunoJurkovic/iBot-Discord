# We import the discord.py library to help us with the API calls and such
import discord
import time
import asyncio
# This is the part of the code which reads the users token from a file names token.
def read_file():
    with open('token') as f:
        variable = f.read()

    return variable


private_token = read_file()

client = discord.Client()

# We create some of the needed variables for later
allowed_channels = ['commands', 'staff']
greet_channel = ['welcome'] # This makes it so that users can only be greeted in the right channel
allowed_user = ['iApexx#8325']
messages = joined_users = 0

# This is a function to refresh the statistics.txt file, make sure to create it for the logging to work!
async def refresh_stats():
    await client.wait_until_ready()
    global messages, joined_users

    while not client.is_closed():
        try:
            with open('statistics.txt', 'a') as file:
                file.write(f""" Time Stamp: {int(time.time())}, Messages: {messages}, Members Joined: {joined_users} \n""")

                messages = 0
                joined_users = 0

                await asyncio.sleep(10)

        except Exception as exception:
            print(exception)
            await asyncio.sleep(10)

# This is dedicated to greeting users
@client.event
async def on_user_join(member):
    global joined_users
    joined_users += 1
    # TODO: Make users be able to pick their own channels

    if str(member.guild.channel) in greet_channel:
        await greet_channel.send(f"""Thank you to user {member.mention} for joining this server!\n""")


@client.event
async def on_message(msg):
    global messages
    messages += 1
    server_id = client.get_guild(422531871314935810)
    #Checks if the user sends help, in which we return the help menu
    if str(msg.channel) in allowed_channels and str(msg.author) in allowed_user:
        if msg.content.find('!!help') != -1:
            # TODO: Implement the help message
            await msg.channel.send('Hey, this is not implemented yet.')

        elif msg.content == '!!members':
            await msg.channel.send(f"""There are {server_id.member_count} members in this Discord server.""")

    else:
        print(f"""The user {msg.author} attempted to run command {msg.content} in the channel {msg.channel}""")


client.loop.create_task(refresh_stats())
client.run(private_token)