"""
This layout is strange but discord.py seems to really want a more functional design
newer top layer will be needed to determine when this file is imported
"""
import logging
from collections import defaultdict
import os

import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure

logger = logging.getLogger(__name__)


def is_administrator(ctx):
    """
    checks if the user has administrative privs in the room
    Args:
        ctx: context of the command

    Returns:

    """
    return ctx.message.author.permissions_in(ctx.message.channel).administrator


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def ping(self, ctx):
        """
        Returns pong to let you know I am here and you are special
        """
        await ctx.channel.send("pong")

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send("Well hello there Mr. {0.name}~".format(member))
        else:
            await ctx.send(
                "Welcome back Mr {0.name}... You having a good day?".format(member)
            )
        self._last_member = member

    @commands.command()
    async def cute(self, ctx, *, member: discord.Member = None):
        await ctx.send("/giphy puppy")


class MessageMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.offending = defaultdict(int)
        # Just to save on typing
        self.processor = bot.processor

    def generate_identifier(self, message):
        """ '
        Simply generates a unique identifier based on the message.  DO NOT CHANGE THIS unless you want to lose counts
        """
        return self.bot.TYPE + message.author.name + message.channel.guild.name

    async def warn_dm(self, message, infractions):
        """
        Gives a warning to the user about their conduct
        Args:
            message: offending message
            infractions: how many infractions

        Returns: None
        """
        await message.author.send(
            f"You have a new infraction bringing you up to {infractions} in "
            f"{message.channel.guild.name} Continued infractions will get you kicked "
            f"from the server."
        )

    async def kick_explain(self, message, infractions):
        """
        Lets the user know they have been booted
        Args:
            message: message object
            infractions: count of infractions

        Returns:

        """
        await message.author.send(
            f"Oh hambergers! You {infractions} infractions in {message.channel.guild.name} "
            f"and have been kicked."
        )
        await message.author.kick(reason="You have been removed.")

    async def wipe_message(self, message):
        """
        Wipes the message and sends a warning
        Args:
            message: message object to use to delete and then send a message to author

        Returns:

        """
        await message.delete()
        await message.channel.send(
            f"That is not very nice language {message.author.name}. Deleting."
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user == message.author:
            return

        # Classify the message
        bad_message = self.processor.evaluate_message(message.content)
        if bad_message:
            await self.wipe_message(message)

            identifier = self.generate_identifier(message)

            count = self.processor.add_infraction(identifier)
            if self.processor.should_take_action(identifier):
                await self.kick_explain(message, count)
            else:
                await self.warn_dm(message, count)


class Buttersbot(commands.Bot):
    TYPE = "DISCORD"

    def __init__(self, command_prefix, processor, **options):
        super().__init__(command_prefix, **options)
        self.processor = processor
        self.add_check(is_administrator)
        self.add_cog(Greetings(self))
        self.add_cog(MessageMonitor(self))

    async def on_ready(self):
        logger.info(f"Logged on as {self.user.name}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.channel.send(
                f"Gee Wiz you can't do that, {ctx.message.author.name}"
            )
        else:
            await ctx.channel.send(
                f"loo loo loo you broken the discord, {ctx.message.author.name}"
            )
