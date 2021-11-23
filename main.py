import discord
from library.ai import AI

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("AI TESTING"))
    print('We have logged in as for AI {0.user}'.format(client))


@client.event
async def on_message(message):
    # AI Menu Tree, simulates an AI by using a menu tree
    ai = AI()
    response = ai.process_message(client, message)
    if response is not None:
        await response
        return

    await message.channel.send(response)

client.run("YOUR_TOKEN")