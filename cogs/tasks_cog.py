import discord
import requests
import os
import json
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime
from datetime import timedelta

class Tasks_cog(commands.Cog):

	task_list = {}
	npc_task_list = {}
	channel_list = {}
	channel_dict = {}
	duke_dict = {}



	def __init__(self,bot):
		self.bot = bot

		self.update_npc_file()
		self.index = 0
		self.printer.start()
		self.duke_dict["status"] = "Offline"
		self.duke_dict["dumped_count"] = self.get_duke_count_dump()
		print(self.duke_dict["status"])
		print(self.duke_dict["dumped_count"])



	def get_duke_count_dump(self):
	
		ret_text = ""
		v_apiSelection = "personalstats"
		v_apiType = "user"
		v_info = "itemsdumped"
		v_torn_id = "4"
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(v_torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			print(v1)
			return "ERROR:SOMEERR" 
			
		selection = v1["personalstats"]
		return selection[v_info]


	def get_duke_status(self):
	
		ret_text = ""
		v_apiSelection = "profile"
		v_apiType = "user"
		v_info = "status"
		v_torn_id = "4"
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(v_torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			print(v1)
			return "ERROR:SOMEERR" 
			
		selection = v1["last_action"]
		return selection[v_info]

	


	def cog_unload(self):
		self.printer.cancel()

	@tasks.loop(seconds=2.0)
	async def printer(self):
		if self.index == 900:
			print("Time to update npc data (30 mins).....")
			self.update_npc_file()
			print("Resetting index to 0")
			self.index = 0
		else:
			#print(self.index)
			self.index += 1
		await self.check_npc_data()

		#await self.do_duke()		



	async def do_duke(self):
		newDukeStatus = self.get_duke_status()
		#print("Duke is " + newDukeStatus)

		if self.duke_dict["status"] != "Online":
			if newDukeStatus == "Online":
				print("Duke came online")

				embed = discord.Embed(title="DUKE", 
					colour=discord.Colour(0x5dd3fa),  
					description= "Duke has come online")
				embed.set_footer(text=self.duke_dict["dumped_count"])

				
				for guild in self.channel_list:
					channel_id = self.channel_list[guild]
					myguild = self.bot.get_guild(int(guild))
					mychannel = self.bot.get_channel(channel_id)
					lootrole = discord.utils.get(myguild.roles, name="DukePing")
					await mychannel.send(lootrole.mention)
					await mychannel.send(embed=embed)


		self.duke_dict["status"] = newDukeStatus

		if self.duke_dict["status"] == "Online":
			newDukeDumpCount = self.get_duke_count_dump()
			#print("Duke dumped items " + str(newDukeDumpCount))


			if int(newDukeDumpCount) > int(self.duke_dict["dumped_count"]):
				print("Duke dumped " + str(int(newDukeDumpCount) - int(self.duke_dict["dumped_count"])) + " items")
				self.duke_dict["dumped_count"] = newDukeDumpCount

				embed = discord.Embed(title="DUKE", 
					colour=discord.Colour(0x5dd3fa),  
					description= "Duke dumped " + str(int(newDukeDumpCount) - int(self.duke_dict["dumped_count"])) + " items")

				
				for guild in self.channel_list:
					channel_id = self.channel_list[guild]
					myguild = self.bot.get_guild(int(guild))
					mychannel = self.bot.get_channel(channel_id)
					lootrole = discord.utils.get(myguild.roles, name="DukePing")
					await mychannel.send(lootrole.mention)
					await mychannel.send(embed=embed)






	

	@printer.before_loop
	async def before_printer(self):
		print('waiting...')
		await self.bot.wait_until_ready()


	async def alert(self,npc_id, level4):


		if os.path.isfile("./shared/npc_details.json") == False:
			# File doesnt exist
			response = "File doesn't exist"
			await ctx.send(response)
			return

		with open("./shared/npc_details.json","r") as inf:		
			npc_dict = json.load(inf)

		print("start alert")

		name = npc_dict[str(npc_id)]["name"]

		title = "5 min warning for " + name + "[" + str(npc_id) + "]"

		url = "https://www.torn.com/loader.php?sid=attack&user2ID="+str(npc_id)

		npc_url = npc_dict[str(npc_id)]["img_url"]

		#print(self.npc_task_list["4"]["level4"])
		description = name + " will be level 4 in 5 mins"

		footer_text = "torn time = " + datetime.utcnow().strftime("%H:%M") + " | Level 4 at " + level4.strftime("%H:%M")

		embed = discord.Embed(title=title, 
			colour=discord.Colour(0x5dd3fa), 
			url=url, 
			description= description)
		embed.set_footer(text=footer_text)
		embed.set_thumbnail(url=npc_url)

		for guild in self.channel_list:
			channel_id = self.channel_list[guild]
			myguild = self.bot.get_guild(int(guild))
			mychannel = self.bot.get_channel(channel_id)
			lootrole = discord.utils.get(myguild.roles, name="lootping")
			await mychannel.send(lootrole.mention)
			await mychannel.send(embed=embed)
	

	async def check_npc_data(self):
		now_time = datetime.utcnow()

		for npc in self.npc_task_list:
			if datetime.fromtimestamp(self.npc_task_list[npc]["5minwarn"]) > now_time:
				if datetime.fromtimestamp(self.npc_task_list[npc]["5minwarn"]) <= (now_time + timedelta(0,2)):
					print(self.npc_task_list[npc]["name"] + " is now ready")
					await self.alert(npc,datetime.fromtimestamp(self.npc_task_list[npc]["level4"]))
					#self.update_npc_file()
			

	
		

	def update_npc_file(self):

		print("updating from yata")		
		self.npc_task_list = {}
		npc_names = {"4":"Duke", "15":"Leslie", "19":"Jimmy", "20":"Fernando", "21":"Tiny", "10":"Scrooge", "17": "Easter Bunny"}
		red_colour = discord.Colour(0xe74c3c)
		blue_colour = discord.Colour(0x5dd3fa)
		green_colour = discord.Colour(0x2ecc71)

		npc_embed_colour = green_colour

		APIURL = "https://yata.yt/api/v1/loot/"


		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		print(r)
		data = r.json() # translates that response into a dict variable
		print(data)
		npc_hosp = data["hosp_out"]

		for torn_id in npc_hosp:

			hosp_out = datetime.utcfromtimestamp(npc_hosp[torn_id])
			
			level1 = hosp_out + timedelta(0,60)
			level2 = hosp_out + timedelta(0,(30*60))
			level3 = hosp_out + timedelta(0,(90*60))
			level4 = hosp_out + timedelta(0,(210*60))
			level5 = hosp_out + timedelta(0,(450*60))

			now_time = datetime.utcnow()

			self.npc_task_list[torn_id] = {"name":npc_names[torn_id],
									"hosp_out": npc_hosp[torn_id],
									"level4":datetime.timestamp(level4),
									"5minwarn":datetime.timestamp(level4 - timedelta(0,(5*60))),
									"alerted":"False"}
		


	

	@commands.Cog.listener()
	async def on_ready(self):
		print('Tasks COG Ready')

		if os.path.isfile("./channels.json"):
				# File already exists
				with open("./channels.json","r") as inf:		
					self.channel_dict = json.load(inf)

		for guild in self.bot.guilds:
			if str(guild.id) in self.channel_dict:
				for channel in guild.text_channels:
					if str(self.channel_dict[str(guild.id)]["main"]) == str(channel.id):
						#print(guild.name + " (" + str(guild.id) + ")  -  " + str(channel.name) + " (" + str(channel.id) + ")")
						self.channel_list[str(guild.id)] = channel.id
			else:
				for channel in guild.text_channels:
					if channel.name == "general":
						#print(guild.name + " (" + str(guild.id) + ")  -  " + str(channel.name) + " (" + str(channel.id) + ")")
						self.channel_list[str(guild.id)] = channel.id
	

def setup(bot):
	bot.add_cog(Tasks_cog(bot))