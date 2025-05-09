import discord
from discord.ext import commands
from discord import app_commands

class Hello(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="hello", description="Says hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hello {interaction.user.mention}!",
            ephemeral=True
        )

async def setup(client: commands.Bot):
    await client.add_cog(Hello(client))