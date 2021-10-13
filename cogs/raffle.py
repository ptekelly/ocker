import discord
from discord.ext import commands

class RaffleGame(commands.Cog):

	
	def __init__(self,bot):
		self.bot = bot
		self.raffleactive = False
		self.currentRaffle = object


	@commands.Cog.listener()
	async def on_ready(self):
		print('Raffle COG Ready')


	@commands.command(hidden=True)
	async def printraffle(self,ctx):
#		r1 = self.currentRaffle()
		await ctx.send(self.raffle.get_raffle())
		return

	@commands.command(hidden=True)
	#async def startraffle(self,ctx, user, entries, buyin, prize):
	async def startraffle(self,ctx):
		self.currentRaffle = raffle("raffle creator", 5, 100, "prizetext")
		self.currentRaffle = True


	async def pingx(self,ctx):
		await ctx.send("pong")


class raffle(object):

	def __init__(self,user, buyin,entries_count,prize):
		self.prize = prize
		self.user = user
		self.buyin = buyin
		self.entries = {}
		self.entries_count = entries_count
		for entry in range(1,entries_count+1):
			self.entries[entry] = "__empty__"


	async def add_entry(position,user):
		if position in self.entries:
			return "Position taken"
		elif position < 1 or position > self.entries_count:
			return "must be in range 0 to 10"
		else:
			self.entries[position] = user

	async def get_raffle(self):
		msg_text = "```"
		msg_text = msg_text + "**Raffle created by " + user + "***"
		msg_text = msg_text + "\n" + "Prize: " + prize
		msg_text = msg_text + "\n" + "Cost per entry: " + str(buyin)
		msg_text = msg_text + "\n" + "**Entries**"
		for entry in entries:
			msg_text = msg_text + "\n" + entry + ": " + entries[entry]

		msg_text = msg_text + "```"

		return msg_text



def setup(bot):
	bot.add_cog(RaffleGame(bot))