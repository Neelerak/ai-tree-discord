import discord
from dateutil.tz import gettz
from dateutil import parser


class Event:

    @staticmethod
    def process_message(model, message):
        return model

    @staticmethod
    async def respond(message, model, client):
        await message.channel.send('What is the name of the event?')

    @staticmethod
    def next():
        return EventOwner()


class EventOwner:

    @staticmethod
    def process_message(model, message):
        # collect kill location
        model.name = message.clean_content
        return model

    @staticmethod
    async def respond(message, model, client):
        await message.channel.send('Whos is running this event?')

    @staticmethod
    def next():
        return EventDate


class EventDate:

    @staticmethod
    def process_message(model, message):
        # collect kill location
        if message.clean_content.lower() == 'me':
            model.owner = message.author.display_name
        else:
            model.owner = message.clean_content
        return model

    @staticmethod
    async def respond(message, model, client):
        await message.channel.send('When will this event happen?')

    @staticmethod
    def next():
        return EventDescription


class EventDescription:

    @staticmethod
    def process_message(model, message):
        # collect kill locationstrptime
        tzinfos = {
            "EST": gettz("America/New York"),
            "CST": gettz("America/Chicago"),
            "MST": gettz("America/Boise"),
            "PST": gettz("America/Los Angeles")
        }
        datetime_object = parser.parse(message.clean_content, tzinfos=tzinfos)
        model.datetime = datetime_object
        return model

    @staticmethod
    async def respond(message, model, client):
        await message.channel.send('Give me more information.')

    @staticmethod
    def next():
        return EventRecap


class EventRecap:

    @staticmethod
    def process_message(model, message):
        # collect kill location
        model.description = message.clean_content
        return model

    @staticmethod
    async def respond(message, model, client):
        # TODO, you will want to customize this section for your own wording and bot name
        bot = discord.utils.get(message.author.guild.members, name="YOUR_BOT_NAME")

        date_string = model.datetime.strftime('%m/%d/%Y %I:%M %p MST')

        embed = discord.Embed(
            title='{0} on {1}'.format(model.name, date_string),
            description='{0} on {1}, this will be lead by {2}'.format(model.name, date_string,
                                                                      model.owner) + '\n\n' + model.description + '\n\nPlease respond with <YOUR EMOJI> to RSVP so we can plan our build '
                                                                                                                  'out and ships',
            color=0xffc641
        )
        text_channel_name = model.name.lower().replace(' ', '-') + '-' + model.datetime.strftime('%Y%m%d')
        voice_channel_name = model.name + ' ' + model.datetime.strftime('%Y%m%d')
        embed.add_field(name="Text Channel", value='#' + text_channel_name, inline=True)
        embed.add_field(name="Voice Channel", value='#' + voice_channel_name, inline=True)
        embed.set_author(name=bot.display_name,
                         icon_url=bot.avatar_url)

        await message.channel.send(embed=embed)
        await message.channel.send('Does the contract look correct?')

    @staticmethod
    def next():
        return EventCorrect


class EventCorrect:

    @staticmethod
    def process_message(model, message):
        # collect kill location
        if message.clean_content.lower() == 'yes':
            model.insert_record(model.name,
                                model.description,
                                model.owner,
                                model.datetime)
            return model
        return False

    @staticmethod
    async def rebuttal(message):
        await message.channel.send('Event has been canceled')

    @staticmethod
    async def respond(message, model, client):
        bot = discord.utils.get(message.author.guild.members, name="YOUR BOT NAME")

        date_string = model.datetime.strftime('%m/%d/%Y %I:%M %p MST')

        embed = discord.Embed(
            title='{0} on {1}'.format(model.name, date_string),
            description='{0} on {1}, this will be lead by {2}'.format(model.name, date_string,
                                                                      model.owner) + '\n\n' + model.description + '\n\nPlease respond with <YOUR EMOJI> to RSVP so we can plan our build '
                                                                                                                  'out and ships',
            color=0xffc641
        )
        embed.set_author(name=bot.display_name,
                         icon_url=bot.avatar_url)

        events_channel = discord.utils.get(message.author.guild.channels, name='events')

        flcategory = discord.utils.get(bot.guild.categories, name='Front Lines')
        overwrites = {
            bot.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        text_channel_name = model.name.lower().replace(' ', '-') + '-' + model.datetime.strftime('%Y%m%d')
        voice_channel_name = model.name + ' ' + model.datetime.strftime('%Y%m%d')
        text_channel = await bot.guild.create_text_channel(text_channel_name, category=flcategory, overwrites=overwrites)
        voice_channel = await bot.guild.create_voice_channel(voice_channel_name, category=flcategory, overwrites=overwrites)
        embed.add_field(name="Text Channel", value=text_channel.mention, inline=True)
        embed.add_field(name="Voice Channel", value=voice_channel.mention, inline=True)

        await events_channel.send(embed=embed)
        await message.channel.send('I will transmit the details of the event')

    @staticmethod
    def next():
        return None
