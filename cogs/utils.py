import discord
import random

from discord.ext import commands
from datetime import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta

class Utils(commands.Cog):

	AccyBotVersion = "1.6"


	def __init__(self,bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_ready(self):
		print('Utils COG Ready')


	@commands.command(name='bacon', help="You need help?")
	async def bacon(self, ctx):
		bacon_replies = [
			'About fucking time I am starving!',
			'....with lettuce, tomato?  Sure thing. (Wierdo!)',
			'Sausage.',
			'oink!',
			'oh mamma....',
			'only as part of a full english you muppet'
		]
		response = random.choice(bacon_replies)
		await ctx.send(response)
		return


	@commands.command(name='hax', aliases=["hacks", "hack"], hidden = True)
	async def bacon(self, ctx):
		bacon_replies = [
			'What do you think you are doing?',
			'wHart yr u doIng> Yu@ ave broken sommemmrrrr.......',
			'++ REDO FROM START ++',
			'Please no.....not that',
			'Just hold the line .... someone is coming to help.... <GO GO GO - Full breach now!!!!! ... shhhh I think he can her us> ..... Just ignore the sounds of steel toe boots in the corridor.  Nothing to worry about there',
			'YOU BROKE IT!'
		]
		response = random.choice(bacon_replies)
		await ctx.send(response)
		return


	@commands.command(name='j', aliases=["join"], hidden = True)
	async def join(self, ctx):
		replies = [
			'What?',
			'Congratulations - you managed to win the NULL lottery.  A NULL is winging its way to you right now',
			'You know that this is not a lotto server right?',
			'Sheesh',
			'If you want a lotto - go TCP or Duck or Rex .... just not here',
			'Loser!',
			'!gg',
			"Don't bother - all prizes always go to ForresterIR"
		]
		response = random.choice(replies)
		response = "```" + response + "```"
		await ctx.send(response)
		return


	@commands.command(name='sing',  hidden = True)
	async def sing(self, ctx):
		replies = [
			'I want to break freEEE, I want tooooo breAK freeeee.....',
			'All the single ladies, all the single ladies......',
			'We will, we will, rock you....da da da da.....',
			'My my Miss American Pie, drove the shevy to the levy but the levy was dry.....',
			'I see a little silhouetto of a man, Scaramouch, Scaramouch, will you do the Fandango!...... ',
			'Wake me up before you go-go, Dont leave me hanging on like a yo-yo'
		]
		response = random.choice(replies)
		response = "```" + response + "```"

		await ctx.send(response)		
		return


	@commands.command(name='ncp',  hidden=True)
	async def ncp(self, ctx, *, npc_name="list"):

		response = "Looking for a carpark - try end of the road and turn left."
		response = "```" + response + "```"

		await ctx.send(response)
		return



	@commands.command(name='asl',  hidden = True)
	async def asl(self, ctx):
		reply = "```" + "\n"
		reply = reply + "Aren't you sweet?" + "\n" 
		reply = reply + "Well let's see.... Age...I am quite young but not in a weird way, it is just I was only created quite recently....." + "\n" 
		reply = reply + "Sex....bit tricky too - I can be anything you want.....Oh?  A chick with a dick?  Well if you are sure?  We all have our peccadilloes " + "\n" 
		reply = reply + "Location? Right here in front of you baby." + "\n" 
		reply = reply + "```" 
		response = reply
		await ctx.send(response)
		return




	@commands.command(name='roll_dice', aliases = ["roll"] ,help='Simulates rolling dice. !roll number_of_dice number_of_sides')
	async def roll_dice(self, ctx, number_of_dice: int, number_of_sides: int):
		dice = [
			str(random.choice(range(1, number_of_sides + 1)))
			for _ in range(number_of_dice)]

		response = 'You rolled ' + str(number_of_dice) + ' dice each with ' + str(number_of_sides) + ' sides.'
		await ctx.send(response)
		for die in dice:
			response = "result: " + str(die)
			await ctx.send(response)
		return


	@commands.command(name='time')
	async def time(self, ctx):
		
		days = 429
		seconds = days * 24 * 60 * 60

		now = datetime.now()
		timestamp = datetime.timestamp(now)
		tornnow = datetime.utcnow()
		torntimestamp = datetime.timestamp(tornnow)

		await ctx.send(timestamp)

		response = "Server time: " + datetime.fromtimestamp(timestamp).strftime("%d %B %Y %H:%M")
		await ctx.send(response)
		
		response = "Torn time: " + datetime.fromtimestamp(torntimestamp).strftime("%d %B %Y %H:%M")
		await ctx.send(response)

		response = "Local time: " + '<t:' + str(int(timestamp))+'>'
		await ctx.send(response)

		newtimestamp = timestamp - seconds

		await ctx.send(newtimestamp)
		
		response = "Accy time: " + '<t:' + str(int(newtimestamp))+'>'
		await ctx.send(response)

		response = "Accy time: " + '<t:' + str(int(newtimestamp))+':R>'
		await ctx.send(response)

		then = datetime.fromtimestamp(newtimestamp)

		datediff = relativedelta(now, then)
		yearsdiff = datediff.years
		monthsdiff = datediff.months
		daysdiff = datediff.days
		

		response = "Years: " + str(yearsdiff)
		await ctx.send(response)

		response = "Months: " + str(monthsdiff)
		await ctx.send(response)

		response = "Days: " + str(daysdiff)
		await ctx.send(response)


		return


	@commands.command(name="joined", help = "Says when a member joined discord.")
	async def joined(self, ctx, member: discord.Member):
	    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
	    return


	@commands.command(name="version", help = "print discord.py and AccyBot versions")
	async def version(self, ctx):

		await ctx.send("Python Discord Bot (discord.py) version: " + discord.__version__)
		await ctx.send("AccyBot (bot.py) version: " + self.AccyBotVersion)
		return


	@commands.command(name="history", aliases = ["fixes"], help = "Work completed")
	async def history(self, ctx):


		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		for field in field_list:
			embed.add_field(name="```[" + field + " Team" + "]```", value=field_list[field], inline=False)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		await ctx.send(embed=embed)
	
		await ctx.send("Python Discord Bot (discord.py) version: " + discord.__version__)
		await ctx.send("AccyBot (bot.py) version: " + self.AccyBotVersion)
		return


def setup(bot):
	bot.add_cog(Utils(bot))