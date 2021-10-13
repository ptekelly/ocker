import discord
from discord.ext import commands

class Example(commands.Cog):

	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('Example COG Ready')

	@commands.command(hidden=True)
	async def ping(self,ctx,):
		await self.pingx(ctx)

	async def pingx(self,ctx):
		await ctx.send("pong")


def setup(bot):
	bot.add_cog(Example(bot))