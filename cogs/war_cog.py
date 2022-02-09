import discord
import json
import requests
import os

from datetime import datetime
from datetime import timedelta
from discord.ext import commands
from discord.ext import tasks


class War_cog(commands.Cog):


	waralert = False

	task_list = {}
	channel_list = {}
	channel_dict = {}
	chainchecktime = 90	

	first = True
	current_war_id = 0
	
	us_name = ""
	us_id = 0
	them_name = ""
	them_id = 0	
	current_start_timestamp = 0
	current_war_data = {}

	now_target = 0
	now_lead = 0

	now_timestamp = 0
	now_us_score = 0
	now_us_chain = 0
	
	now_them_score = 0
	now_them_chain = 0
	
	
	then_target = 0
	then_lead = 0

	then_timestamp = 0
	then_us_score = 0
	then_us_chain = 0
	
	then_them_score = 0
	then_them_chain = 0

	change_target = 0
	change_lead = 0

	change_timestamp = 0
	change_us_score = 0
	change_us_chain = 0
	
	change_them_score = 0
	change_them_chain = 0



	def __init__(self,bot):
		self.bot = bot

#		self.update_npc_file()
		self.index = 0
		self.printer.start()

		print("init")


	@commands.Cog.listener()
	async def on_ready(self):
		print('War COG Ready')

		if os.path.isfile("./channels.json"):
				# File already exists
				with open("./channels.json","r") as inf:		
					self.channel_dict = json.load(inf)

		for guild in self.bot.guilds:
			if str(guild.id) in self.channel_dict:
				for channel in guild.text_channels:
					if str(self.channel_dict[str(guild.id)]["warchnl"]) == str(channel.id):
						self.channel_list[str(guild.id)] = channel.id

		return


	@tasks.loop(seconds=10.0)
	async def printer(self):
		if self.waralert == False:
			return

		if self.index == 60:
			print("Time to send war info (10 mins).....")
			await self.getwar()
			print("Resetting index to 0")
			self.index = 0
		else:
			#print(self.index)
			self.index += 1
		await self.chaincheck()

		return


	@commands.command(name="waralerton", hidden = True)
	async def waralerton(self,ctx):

		self.waralert = True


		await ctx.send("```War alerting is turned on ```")

		return


	@commands.command(name="waralertoff", hidden = True)
	async def waralertoff(self,ctx):

		self.waralert = False


		await ctx.send("```War alerting is turned off ```")

		return


	@commands.command(name="setct", hidden = True)
	async def setct(self,ctx,chaintime:int=90):

		self.chainchecktime = chaintime

		await ctx.send("```Chain time threshhold set to " + str(chaintime) + " seconds```")

		return



	@commands.command(name="ct", hidden = True)
	async def ct(self,ctx,chaintime:int=0):

		await self.chaincheck(chaintime)
		return


	async def chaincheck(self,chaintime:int=0):
		v_apiSelection = "chain"
		v_apiType = "faction"

		
		APIURL = self.bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise APIIssue("war")
			return

		else:

			if chaintime == 0:
				chaintime = self.chainchecktime
			if int(v1["chain"]["timeout"]) < chaintime:
				for guild in self.channel_list:
					channel_id = self.channel_list[guild]
					myguild = self.bot.get_guild(int(guild))
					mychannel = self.bot.get_channel(channel_id)

					title = "Chain Timer Alert"

					description = "The current chain cooldown " + str(v1["chain"]["timeout"]) + " seconds is less than the alert threshhold of " + str(chaintime) + " seconds."
					description = description + "\n"
					description = description + "Chain: " + str(v1["chain"]["current"]) + " - Max: " + str(v1["chain"]["max"])
					footer = "Chain started: " + datetime.utcfromtimestamp(v1["chain"]["start"]).strftime("%H:%M %d %B %Y")

					embed = discord.Embed(title=title, 
							colour=discord.Colour(0x5dd3fa), 
							url="https://www.torn.com/factions.php?step=your#/",
							description = description)
						
					embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
					
					embed.set_footer(text=footer)


					await mychannel.send(embed=embed)
					

					
		return



	async def check_chain(self):
		print("check_chain")
		return


	@printer.before_loop
	async def before_printer(self):
		print('waiting...')
		await self.bot.wait_until_ready()

		return


	def cog_unload(self):
		self.printer.cancel()

		return
	

	@commands.command(name='enemy', help='War enemy summary.')
	async def enemy(self, ctx):
		if self.them_id == 0:
			await ctx.send("Try running the !war command first")
		else:
			await ctx.send("War opponent: " + self.them_name + " (" + str(self.them_id) + ")")

			#https://api.torn.com/faction/40420?selections=basic&key=MWeZy6Y8IIoX6tsM

			v_apiSelection = "basic"
			v_apiType = "faction"

			
			APIURL = self.bot.v_apiAddress+v_apiType+'/'+str(self.them_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey+'&comment=ocker_enemy'
			r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
			v1 = r.json() # translates that response into a dict variable
			if "error" in v1:
				raise APIIssue("enemy")
				return
			
			enemy_list = ""
			members = v1.get("members","NA")
			if members == "NA":
				await ctx.send("error with api")
				return
			for tornid in members:
				enemy_list = enemy_list + members[tornid]["name"] + " [" + str(tornid) + "] - "
				enemy_list = enemy_list + members[tornid]["status"]["description"] + " - Last Action " + members[tornid]["last_action"]["relative"]
				enemy_list = enemy_list + "\n"


			await ctx.send(enemy_list)

		return


	@commands.command(name='war', help='War update.')
	async def war(self, ctx):

		await self.getwar()
		return


	async def getwar(self):
		v_apiSelection = "rankedwars"
		v_apiType = "torn"

		
		APIURL = self.bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey+'&comment=pkwarcall'
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise APIIssue("war")
			return

		for warid in v1["rankedwars"]:
			#print(warid)
			for faction in v1["rankedwars"][warid]["factions"]:
				if v1["rankedwars"][warid]["factions"][faction]["name"] == "Hello High" and v1["rankedwars"][warid]["war"]["winner"]==0:
					self.current_war_id = warid
					self.current_war_data = v1["rankedwars"][warid]


		if self.current_war_id == 0:
			await ctx.send("```No Current Ranked War found.```")
			return
		else:
			self.now_timestamp = datetime.timestamp(datetime.utcnow())

			self.current_start_timestamp = self.current_war_data["war"]["start"]

			title = "Current Ranked War for Hello High"
			footer = "War started: " 

			footer = footer + (datetime.utcfromtimestamp(self.current_start_timestamp).strftime("%H:%M %d %B %Y"))


			for faction in self.current_war_data["factions"]:
				if self.current_war_data["factions"][faction]["name"] == "Hello High":
					self.us_name = self.current_war_data["factions"][faction]["name"]
					self.us_id = faction
					
					self.now_us_score = self.current_war_data["factions"][faction]["score"]
					self.now_us_chain = self.current_war_data["factions"][faction]["chain"]

				else:
					self.them_name = self.current_war_data["factions"][faction]["name"] 
					self.them_id = faction

					self.now_them_score = self.current_war_data["factions"][faction]["score"]
					self.now_them_chain = self.current_war_data["factions"][faction]["chain"]



			self.now_target = self.current_war_data["war"]["target"]
			
			self.now_lead = self.now_us_score - self.now_them_score 

			if self.first == False:
				self.change_target = self.now_target - self.then_target
				self.change_lead = self.now_lead - self.then_lead
				self.change_us_score = self.now_us_score - self.then_us_score
				self.change_us_chain = self.now_us_chain - self.then_us_chain
				self.change_them_score = self.now_them_score - self.then_them_score
				self.change_them_chain = self.now_them_chain - self.then_them_chain
				self.change_timestamp = self.now_timestamp - self.then_timestamp


			self.then_target = self.now_target
			self.then_lead = self.now_lead

			self.then_timestamp = self.now_timestamp
			self.then_us_score = self.now_us_score
			self.then_us_chain = self.now_us_chain
			
			self.then_them_score = self.now_them_score
			self.then_them_chain = self.now_them_chain




			if (self.now_lead) >0:
				description = "Lead: " + "{:,d}".format(abs(self.now_lead))
			else:
				description = "Deficit: " + "{:,d}".format(abs(self.now_lead))
			if self.first == False:
				description = description + " (" + "{:,d}".format(self.change_lead) + ")"
			

			description = description + "\n"
			description = description + "Target: " + "{:,d}".format(self.now_target)
			if self.first == False:
				description = description + " (" + "{:,d}".format(self.change_target) + ")"

			now_field_us_title = self.us_name
			now_field_us_value = "Score: " + "{:,d}".format(self.now_us_score)
			if self.first == False:
				now_field_us_value = now_field_us_value + " (" + "{:,d}".format(self.change_us_score) + ")"

			now_field_us_value = now_field_us_value + "\n"
			now_field_us_value = now_field_us_value + "Chain: " + "{:,d}".format(self.now_us_chain)
			if self.first == False:
				now_field_us_value = now_field_us_value + " (" + "{:,d}".format(self.change_us_chain) + ")"

			now_field_them_title = self.them_name
			now_field_them_value = "Score: " + "{:,d}".format(self.now_them_score)
			if self.first == False:
				now_field_them_value = now_field_them_value + " (" + "{:,d}".format(self.change_them_score) + ")"

			now_field_them_value = now_field_them_value + "\n"
			now_field_them_value = now_field_them_value + "Chain: " + "{:,d}".format(self.now_them_chain)
			if self.first == False:
				now_field_them_value = now_field_them_value + " (" + "{:,d}".format(self.change_them_chain) + ")"

			if self.first == False:
				footer = footer + "\n"
				footer = footer + "Values in brackets are changes from " + str(int(self.change_timestamp/60)) + " minutes ago"


			v_apiSelection = "chain"
			v_apiType = "faction"

			
			APIURL = self.bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
			r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
			v1 = r.json() # translates that response into a dict variable
			if "error" in v1:
				print("APIIssue(war)")
			else:

				footer = footer + "\n" + "Current chain cooldown is " + str(v1["chain"]["timeout"]) + " seconds"




			embed = discord.Embed(title=title, 
				colour=discord.Colour(0x5dd3fa), 
				url="https://www.torn.com/factions.php?step=your#/",
				description = description)
			embed.add_field(name=now_field_us_title, value=now_field_us_value, inline = True)
			embed.add_field(name=now_field_them_title, value=now_field_them_value, inline = True)
				
			embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
			
			embed.set_footer(text=footer)



			for guild in self.channel_list:
				channel_id = self.channel_list[guild]
				myguild = self.bot.get_guild(int(guild))
				mychannel = self.bot.get_channel(channel_id)
				await mychannel.send(embed=embed)

			
		self.first = False

		return


def setup(bot):
	bot.add_cog(War_cog(bot))