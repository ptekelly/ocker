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


	@commands.Cog.listener()
	async def on_message(self,ctx):

		if ctx.author == self.bot.user:
			return

		cmdText = ctx.content.lower()

		#print(ctx.content)

		if str(ctx.channel.type) == "private":
			print(ctx.author.display_name + " - " + ctx.content)

			#private
			#await ctx.channel.send("How can I help you?")
			if "hi" in cmdText or "hello" in cmdText:
				replies = [
					"Hello, how are you today?",
					"Good day to you",
					"Is there something you need?",
					"I am very busy today, what do you want",
					"I can't imagine what you want from me",
					"Do you realise I have a whole server to run?"				]
				response = random.choice(replies)
				await ctx.channel.send(response)

			elif "fuck" in cmdText or "cunt" in cmdText:
				replies = [
					"Do you kiss your mother with that mouth",
					"Well let's see....Banhammer?",
					"You looking for a fight there?",
					"MUM!!!!!",
					"You think I am scared of you?",
					"Sticks and stones will break my bones but words will never hurt me"				]
				response = random.choice(replies)
				await ctx.channel.send(response)

			elif "how" in cmdText and "are" in cmdText and "you" in cmdText:
				replies = [
					"I am good, how are you?",
					"I have been better but ok now thanks",
					"I am feeling groovy",
					"Are you asking because you care or for something to say?",
					"Fantasy toby",
					"ok"				]
				response = random.choice(replies)
				await ctx.channel.send(response)
			

		else:
			#normal

			cmdText = ctx.content.lower()

			if "fuck" in cmdText and "ocker" in cmdText:
				#await ctx.send("```NO LOTTO RUNNING - Feel free to start one.```")
				linklinst = [
					"https://tenor.com/view/hitchhikers-guide-to-the-galaxy-marvin-robot-computer-hates-me-gif-24150519",
					"https://tenor.com/view/depressed-no-one-listens-pessimistic-pessimist-marvin-the-paranoid-android-gif-11204001",
					"https://tenor.com/view/the-hitchhikers-guide-to-the-galaxy-marvin-robot-depressed-sad-gif-3555395",
					"https://tenor.com/view/bugs-bunny-tears-crying-you-dont-love-me-gif-13510919",
					"https://tenor.com/view/sob-crying-sadness-inside-out-gif-5106316",
					"https://tenor.com/view/the-hitchhikers-guide-to-the-galaxy-marvin-the-paranoid-android-its-even-worse-that-i-thought-it-would-be-worse-that-i-thought-got-worse-gif-21730765"				]
				response = random.choice(linklinst)
				await ctx.channel.send(response)

			elif "let me win" in cmdText and "ocker" in cmdText:
				#await ctx.send("```NO LOTTO RUNNING - Feel free to start one.```")
				linklinst = [
					"I am not letting anyone win",
					"no",
					"You are kicked from this",
					"is the lotto even running",
					"Don't beg - it is not endearing",
					"I want to ok - but I wont"]
				response = random.choice(linklinst)
				await ctx.channel.send(response)

		return		


	@commands.command(name='h', hidden = True)
	async def h(self, ctx):
		print(ctx.invoked_with)

		linklinst = [
			"https://tenor.com/view/steps-abba-gif-7962943",
			"https://tenor.com/view/line-of-duty-hh-aitch-love-bbc-gif-21397401",
			"https://tenor.com/view/when-the-h-stock-images-funny-dance-meme-memes-gif-21772997",
			"https://tenor.com/view/letter-h-gif-9063752",
			"https://tenor.com/view/beans-gif-24519902"
			]
		response = random.choice(linklinst)
		await ctx.send(response)
		return		


	@commands.command(name='k', hidden = True)
	async def k(self, ctx):
		print(ctx.invoked_with)

		linklinst = [
			"https://tenor.com/view/thumbs-up-nice-well-done-approve-good-job-gif-17717709",
			"https://tenor.com/view/wheel-of-fortune-wheel-wof-game-show-vanna-white-gif-19174111",
			"https://tenor.com/view/letter-k-gif-9063755",
			"https://tenor.com/view/kk-mmkay-ok-okay-gif-9835585",
			"https://tenor.com/view/okily-dokily-okie-dokie-ok-kay-nerd-gif-11941985"
			]
		response = random.choice(linklinst)
		await ctx.send(response)
		return		


	@commands.command(name='bacon', help="You need help?")
	async def bacon(self, ctx):
		print(ctx.invoked_with)
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
	async def hax(self, ctx):
		print(ctx.invoked_with)
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


	


	@commands.command(name='sing',  hidden = True)
	async def sing(self, ctx):
		print(ctx.invoked_with)
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
		print(ctx.invoked_with)

		response = "Looking for a carpark - try end of the road and turn left."
		response = "```" + response + "```"

		await ctx.send(response)
		return



	@commands.command(name='asl',  hidden = True)
	async def asl(self, ctx):
		print(ctx.invoked_with)
		reply = "```" + "\n"
		reply = reply + "Aren't you sweet?" + "\n" 
		reply = reply + "Well let's see.... Age...I am quite young but not in a weird way, it is just I was only created quite recently....." + "\n" 
		reply = reply + "Sex....bit tricky too - I can be anything you want.....Oh?  A chick with a dick?  Well if you are sure?  We all have our peccadilloes " + "\n" 
		reply = reply + "Location? Right here in front of you baby." + "\n" 
		reply = reply + "```" 
		response = reply
		await ctx.send(response)
		return


	@commands.command(name='choose', aliases = ["chs"] ,help='Choose item - use comma separated list to choose from')
	async def choose(self, ctx, *, choices: str):
		
		print(ctx.invoked_with)

		choice_list = choices.split(",")
		if len(choice_list) < 2:
			await ctx.send("```You need to provide a comma separated list.  For example !choose Red, Green, Blue```1")
			return

		response = random.choice(choice_list)
		await ctx.send(response)




	@commands.command(name='roll_dice', aliases = ["roll"] ,help='Simulates rolling dice. !roll number_of_dice number_of_sides')
	async def roll_dice(self, ctx, number_of_dice: int, number_of_sides: int):
		print(ctx.invoked_with)
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
		print(ctx.invoked_with)
		
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
		print(ctx.invoked_with)
		await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
		return


	@commands.command(name="version", help = "print discord.py and AccyBot versions")
	async def version(self, ctx):
		print(ctx.invoked_with)

		await ctx.send("Python Discord Bot (discord.py) version: " + discord.__version__)
		await ctx.send("AccyBot (bot.py) version: " + self.AccyBotVersion)
		return


def setup(bot):
	bot.add_cog(Utils(bot))