import asyncio

import requests
import discord
from discord.ext import commands
from patrons import verified_patron_email
from google_sheets import add_patron_to_sheets


class BotCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.email_message = "Hello! In order to help you today, please provide me with an email address associated " \
                             "with your patreon subscription."
        self.steam_id_message = "I have verified that you are an active Patron. Please provide me with your steam64id," \
                                " so I may add you to our Patron Database. If you need help finding your Steam64ID, " \
                                "please refer to this link: https://steamid.io/lookup/ "

    @commands.command(name="patreon")
    async def patreon(self, ctx: commands.Context):
        user = ctx.author
        user_email = await self.gather_user_data(user, self.email_message, verify_email=True)
        success, message = verified_patron_email(user_email)
        if not success:
            await user.send(message)
            return

        steam_id = await self.gather_user_data(user, self.steam_id_message)
        if not valid_steam64id(steam_id):
            await user.send("Invalid steam64id, please try again!")
            return
        final_message = add_patron_to_sheets(user_email, steam_id)
        await user.send(embed=embed_message(final_message))

    async def gather_user_data(self, user, message: str, verify_email=False):
        try:
            await user.send(embed=embed_message(message))
            reply = await self.bot.wait_for("message", timeout=120)

            if verify_email:
                if not valid_email(email_address=reply.content):
                    await user.send("Invalid email, please try again!")
                    return
            return reply.content
        except asyncio.TimeoutError:
            await user.send("Session timed out, please try again later.")


def valid_steam64id(steam64id: str) -> bool:
    return len(steam64id) == 17


def valid_email(email_address: str) -> bool:
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email_address})

    status = response.json()['status']
    return status == "valid"


def embed_message(message):
    return discord.Embed(title=message)


def setup(bot: commands.Bot):
    bot.add_cog(BotCommands(bot))
