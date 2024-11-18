import discord
from discord.ext import commands

class mycogs(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(title="Ping", description="Latency in ms", color=discord.Color.Blue())

        await ctx.send(embed=ping_embed)

async def setup(bot):
    await bot.add_cog(mycogs(bot))