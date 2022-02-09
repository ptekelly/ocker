import discord
import os
import json
import requests
import __main__
import re
import asyncio
import typing
import random

from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from random import randrange

class Lotto_cog(commands.Cog):

	lottoObject = {}
	lottoEntries = {}
	listenlist = {}
	lottoMgr = "lottomgr"
	listenChannel = ""
	listen = False
	fidlisten = False
	ftslisten = False
	listenwho = ""
	fidlistenwho = ""
	ftslistenwho = ""
	doorlisten = False
	doortimer = 30
	cooldownTimer = 15
	listenTimer = 120
	cooldownOn = False
	topLeaderCount = 5
	lottoPing = "Lotto Ping"
	userlist = {}
	ftsphrase = ""
	ftswordlist = ["Paramount",
		"Welcome to the party",
		"Jumping jack flash",
		"Hospital",
		"Flapjack",
		"Casino Royale",
		"Revenge of the Jedi",
		"Friendship",
		"Cosmos",
		"Starbase",
		"Jump the shark",
		"Katapult",
		"Carpark",
		"Raiders of the lost ark",
		"Rubiks Cube",
		"Household",
		"Fireplace",
		"Garden room",
		"Picture frame",
		"Love",
		"Railway",
		"Runway",
		"Pat the dog"
		]

	red_colour = discord.Colour(0xe74c3c)
	blue_colour = discord.Colour(0x5dd3fa)
	green_colour = discord.Colour(0x2ecc71)

	def __init__(self,bot):
		self.bot = bot

		self.lottoObject["status"] = "Off"

	@commands.Cog.listener()
	async def on_ready(self):
		print('Lotto COG Ready')

	@commands.Cog.listener()
	async def on_message(self,ctx):
		#print(ctx.content)
		cmdText = ctx.content.replace('\xa0', ' ')
		#print(cmdText)

		if ctx.author == self.bot.user:
			return
		if self.listen == False and self.fidlisten == False  and self.ftslisten == False and self.doorlisten == False:
			return
		if ctx.channel != self.listenChannel:
			return

		if self.listen == True:

			if ctx.author != self.listenwho:
				return
			if not(cmdText.startswith("You sent")):
				return

			sendType = ""
			cash = 0
			item = ""
			itemCount = 1
			itemValue = 0
			prizeValue = 0



			if cmdText.startswith("You sent $"):
				sendType = "Cash"

				cash = int(re.search('(?<=\$)(.*?)(?=\s)', cmdText).group(0).replace(",",""))


			elif cmdText.startswith("You sent a pair of "):
				sendType = "Item"
				itemCount = 1

				item = re.search('(^You sent a pair of )(.*?)(?= to)', cmdText).group(2)
				prefix = "a pair of "

			elif cmdText.startswith("You sent an "):
				sendType = "Item"
				itemCount = 1

				item = re.search('(^You sent an )(.*?)(?= to)', cmdText).group(2)

				prefix = "an "

			elif cmdText.startswith("You sent a "):
				sendType = "Item"
				itemCount = 1

				item = re.search('(^You sent a )(.*?)(?= to)', cmdText).group(2)

				prefix = "a "

			elif cmdText.startswith("You sent some "):
				sendType = "Item"
				itemCount = 1

				item = re.search('(^You sent some )(.*?)(?= to)', cmdText).group(2)

				prefix = "some "

			else:
				sendType = "Item"
				#print(sendType)
				#print(ctx.content)
				item = re.search('(?<=x )(.*?)(?= to)', cmdText).group(1)
				#print(item)

				x = int(re.search('(^You sent )(.*?)(?=x)', cmdText).group(2).replace(",",""))
				#print(x)
				itemCount = x

				prefix = str(x) + " x "

			if sendType == "Cash":
				#await self.listenChannel.send("Cash sent: Value = " + str(cash))
				response = await self.addprize(ctx.author,"Cash", cash)
				totalPrizeValue = cash
				prizeName = "cash"
			elif sendType == "Item":
				singleItemValue = await self.get_items_value(item)
				#await self.listenChannel.send(str(itemCount) + " " + item + "(s) sent. Item value = " + str(singleItemValue) + ". Prize Value = " + str(singleItemValue * itemCount))
				response =  await self.addprize(ctx.author,"Item",singleItemValue*itemCount)
				totalPrizeValue = singleItemValue * itemCount
				prizeName = prefix + item
			else:
				await self.listenChannel.send("Not sure what happened")
				return

			
			title = "Lotto Send line Registered"

			description = "Send line from **" + ctx.author.display_name + "** has been registered for **" + prizeName + "**.  " 
			description = description + "\n" + "Total prize value: $" + str("{:,.0f}".format(totalPrizeValue))

			footer = str("{:,.0f}".format(response["newCashCount"])) + " cash prizes sent valuing: $" + str("{:,.0f}".format(response["newCashValue"]))

			footer = footer + "\n"
			footer = footer + str("{:,.0f}".format(response["newItemCount"])) + " item prizes valuing: $" + str("{:,.0f}".format(response["newItemValue"]))

			embed = discord.Embed(title=title, 
				colour=discord.Colour.orange(), 
				description = description)
			
			embed.set_thumbnail(url=ctx.author.avatar_url)
			embed.set_footer(text=footer)


			await self.listenChannel.send(embed=embed)	

			if self.lottoObject["listencount"] > 1:
				self.lottoObject["listencount"] = self.lottoObject["listencount"] - 1
				await self.listenChannel.send("Multi prize draw - you have " + str(self.lottoObject["listencount"]) + " send lines to complete.")	
			else:
				await self.dolistenoff()
			return

		elif self.fidlisten == True:
			if str(ctx.author.id) in self.userlist:

				if str(ctx.content) == self.userlist[str(ctx.author.id)]["torn_id"]:

					if ctx.author == self.fidlistenwho:
						await ctx.channel.send("```You cannot enter your own lotto```")
						return


					self.fidlisten = False

					self.lottoObject["status"] = "Off"
					self.lottoObject["listencount"] = 1

					title = ctx.author.display_name + " is the FID Winner"

					description = "Prize: " + self.lottoObject["prize"]
					description = description + "\n" + "Listen turned on for " + self.lottoObject["owner"]

					embed = discord.Embed(title=title, 
						colour=discord.Colour.orange(), 
						description = description)
					
					embed.set_thumbnail(url=ctx.author.avatar_url)

					await self.listenChannel.send(embed=embed)	


					await self.dolisten(ctx.channel,self.fidlistenwho,self.lottoObject["listencount"])

					cooldown = self.listenTimer * self.lottoObject["listencount"]
					while cooldown != 0:
						cooldown = cooldown - 1
						if self.listen == False:
							return
						await asyncio.sleep(1)
					await self.dolistenoff()
					await ctx.channel.send("```Heh " + self.lottoObject["owner"] + ", you didn't provide a send line - speak to a manager and beg for listen to be turned on```")


		elif self.ftslisten == True:
			if str(ctx.author.id) in self.userlist:

				if str(ctx.content).strip().lower() == self.ftsphrase.strip().lower():

					if ctx.author == self.ftslistenwho:
						await ctx.channel.send("```You cannot enter your own lotto```")
						return


					self.ftslisten = False

					self.lottoObject["status"] = "Off"
					self.lottoObject["listencount"] = 1

					title = ctx.author.display_name + " is the FTS Winner"

					description = "Prize: " + self.lottoObject["prize"]
					description = description + "\n" + "Listen turned on for " + self.lottoObject["owner"]

					embed = discord.Embed(title=title, 
						colour=discord.Colour.orange(), 
						description = description)
					
					embed.set_thumbnail(url=ctx.author.avatar_url)

					await self.listenChannel.send(embed=embed)	


					await self.dolisten(ctx.channel,self.ftslistenwho,self.lottoObject["listencount"])

					cooldown = self.listenTimer * self.lottoObject["listencount"]
					while cooldown != 0:
						cooldown = cooldown - 1
						if self.listen == False:
							return
						await asyncio.sleep(1)
					await self.dolistenoff()
					await ctx.channel.send("```Heh " + self.lottoObject["owner"] + ", you didn't provide a send line - speak to a manager and beg for listen to be turned on```")


		elif self.doorlisten == True:
			#print("listing for door")
			if ctx.author != self.listenwho:
				return

			if not(str(ctx.content).strip().lower().startswith("pick")):
				return

			if int(ctx.content[5:].strip()) >0 and int(ctx.content[5:].strip()) <= self.lottoObject["prizecount"]:

				door_prize = random.choice(self.lottoObject["prizes"])
				
				doorchoice = "Door " + ctx.content[5:].strip() 
				title = "You have chosen " + doorchoice
				description = "You reach over and with nervous anticipation you reach out your hand and wrap your fingers around the large shiny knob giving it a slow gentle twist."
				description = description + "\n"
				if door_prize.lower().strip() in ["nothing","nowt","f all", "fuck all", "zilch"]:
					win = False
					description = description + "\n" + "You chose " + doorchoice.lower() + "... and ... BAD LUCK ... you have won " + door_prize 

				else:	
					win = True
					description = description + "\n" + "You have chosen " + doorchoice.lower() + " ... and ... you have won '" + door_prize + "' from " + self.lottoObject["owner"]

				description = description + "\n"

				otherprizes = self.lottoObject["prizes"]

				otherprizes.remove(door_prize)

				if len(otherprizes) == 1:
					otherpizestext = "The other possible prize was " + otherprizes[0]
				else:
					otherpizestext = ""
					position = 1
					for pz in otherprizes:
						otherpizestext = otherpizestext + pz.strip()
						if position == len(otherprizes) - 1:
							otherpizestext = otherpizestext + " and "
						elif position < len(otherprizes):
							otherpizestext = otherpizestext + ", "
						position = position + 1


				#otherpizestext = ", ".join(otherprizes)

				footer = "The other possible prizes were " + otherpizestext

				embed = discord.Embed(title=title, 
						colour=discord.Colour.orange(), 
						description = description)
					
				embed.set_thumbnail(url=ctx.author.avatar_url)
				embed.set_footer(text=footer)

				await self.listenChannel.send(embed=embed)

				self.doorlisten = False
				self.lottoObject["lottotype"] = ""

				if win == False:
					return


				await self.dolisten(ctx.channel,self.doorlistenwho,self.lottoObject["listencount"])

				cooldown = self.listenTimer
				while cooldown != 0:
					#await ctx.channel.send(cooldown)
					cooldown = cooldown - 1
					if self.listen == False:
						return
					await asyncio.sleep(1)
				await self.dolistenoff()
				await ctx.channel.send("```Heh " + self.lottoObject["owner"] + ", you didn't provide a send line - speak to a manager and beg for listen to be turned on```")




			return

		return


	async def get_items_value(self, item_name):
		print("get_items_value")
		v_apiType = 'torn'
		v_apiSelection = 'items'

		APIURL = self.bot.v_apiAddress+v_apiType+'/?selections='+v_apiSelection+'&key='+ self.bot.v_apiKey

		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		data = r.json() # translates that response into a dict variable
		selection = data["items"]
		found = False
		singleItemValue = 0
		for item in selection:
			if item_name.lower() == selection[item]["name"].lower():
				found = True
				singleItemValue = selection[item]["market_value"]

		return singleItemValue





	async def addprize(self, member, prizeType, prizeValue):
		print("addprize")

		member = str(member.id)
		cashValue = 0
		cashCount = 0
		itemValue = 0
		itemCount = 0
		maxPrizeValue = prizeValue
		firstTimestamp = datetime.timestamp(datetime.utcnow())
		lastTimestamp = datetime.timestamp(datetime.utcnow())


		if os.path.isfile("./prizes.json"):

			with open("./prizes.json","r") as inf:
				dict = json.load(inf)
			if member in dict:
				cashValue = dict[member].get("cashValue",0)
				cashCount = dict[member].get("cashCount",0)
				itemValue = dict[member].get("itemValue",0)
				itemCount = dict[member].get("itemCount",0)
				maxPrizeValue = max(prizeValue,dict[member].get("maxPrizeValue",0))
				firstTimestamp = dict[member].get("firstTimestamp",datetime.timestamp(datetime.utcnow()))
				lastTimestamp = datetime.timestamp(datetime.utcnow())

				
				if prizeType == "Cash":
					newCashValue = cashValue + prizeValue
					newCashCount = cashCount + 1
					newItemValue = itemValue
					newItemCount = itemCount
				else:
					newCashValue = cashValue
					newCashCount = cashCount
					newItemValue = itemValue + prizeValue
					newItemCount = itemCount + 1

				dict[member].update({'cashValue' : newCashValue})
				dict[member].update({'cashCount' : newCashCount})
				dict[member].update({'itemValue' : newItemValue})
				dict[member].update({'itemCount' : newItemCount})
				dict[member].update({'maxPrizeValue' : maxPrizeValue})
				dict[member].update({'firstTimestamp' : firstTimestamp})
				dict[member].update({'lastTimestamp' : lastTimestamp})

				#print("Prizes Updated")

			else:
				if prizeType == "Cash":
					newCashValue = cashValue + prizeValue
					newCashCount = cashCount + 1
					newItemValue = itemValue
					newItemCount = itemCount
				else:
					newCashValue = cashValue
					newCashCount = cashCount
					newItemValue = itemValue + prizeValue
					newItemCount = itemCount + 1

				dict[member] = {'cashValue' : newCashValue,'cashCount' : newCashCount,'itemValue' : newItemValue,'itemCount' : newItemCount,'maxPrizeValue' : maxPrizeValue, 'firstTimestamp' : firstTimestamp, 'lastTimestamp' : lastTimestamp}

				#print("Prize Added")

		else:
			if prizeType == "Cash":
				newCashValue = cashValue + prizeValue
				newCashCount = cashCount + 1
				newItemValue = itemValue
				newItemCount = itemCount
			else:
				newCashValue = cashValue
				newCashCount = cashCount
				newItemValue = itemValue + prizeValue
				newItemCount = itemCount + 1

			dict = {member: {'cashValue' : newCashValue, 'cashCount' : newCashCount, 'itemValue' : newItemValue, 'itemCount' : newItemCount,'maxPrizeValue' : maxPrizeValue, 'firstTimestamp' : firstTimestamp, 'lastTimestamp' : lastTimestamp}}

			#print("Prize added (new file)")

		with open("./prizes.json", "w") as data_file:
					json.dump(dict, data_file, indent=2)


		response = {"newCashValue":newCashValue,"newCashCount":newCashCount,"newItemValue":newItemValue,"newItemCount":newItemCount,'maxPrizeValue' : maxPrizeValue, 'firstTimestamp' : firstTimestamp, 'lastTimestamp' : lastTimestamp}
		return response



	async def checklottouser(self, member):
		#print("checklottouser")	
		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			
			if str(member.id) not in dict:
				#description = description + member.display_name + " has not been setup with Ocker yet."
				return "missing user"
			
			torn_id = dict[str(member.id)].get("torn_id","missing user")

			if torn_id == "missing user":
				return torn_id

			user_api = dict[str(member.id)].get("torn_api","missing api")
			
			if user_api == "missing api":
				return "missing api"

			
			v_apiType = "user"
			v_apiSelection = "bars"
	
			APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ user_api
			r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
			v1 = r.json() # translates that response into a dict variable
			if "error" in v1:
				return "invalid api"

			return torn_id				
				
		else:
			return "file error"
		

		

	def is_lotto():
	    async def predicate(ctx):
	    	#print("is_lotto")

	    	server_id = str(ctx.guild.id)
	    	this_channel = ctx.message.channel
	    	this_channel_name = this_channel.name
	    	this_channel_id = this_channel.id
	    	channel_allowed = False

	    	if os.path.isfile("./channels.json"):
	    		#print("File already exists")
	    		with open("./channels.json","r") as inf:		
	    			#print("open file")
	    			channel_dict = json.load(inf)

	    			if server_id in channel_dict:
	    				#print("Server id and file exist")
	    				if this_channel_id == channel_dict[server_id]["lottochnl"]:
	    					#print("This channel matches allowd channel")
	    					channel_allowed = True

	    	if channel_allowed == False:
	    		#print("delete?")
	    		await ctx.message.delete()
	    	return channel_allowed
	    return commands.check(predicate)

	
	async def is_lotto_mgr(self,member):
		#print("is_lotto_mgr")
		manager = False
		for role in member.roles:
			#print(role.name)
			if self.lottoMgr == role.name:
				manager = True
				
		#print("manager? " + str(manager))
		return manager


	@commands.command(name="startlotto", aliases = ["sl"], hidden = True)
	@is_lotto()
	async def startlotto(self,ctx,*, prize):
		print(ctx.invoked_with)

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			self.lottoObject["prizes"] = prize
			self.lottoObject["prizecount"] = 1
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "lotto"

			self.lottoEntries = {}

			title = self.lottoObject["owner"] + " has started a lotto."
			description = "Prize: '" + self.lottoObject["prize"] + "'"
			footer = "Type !join (or !j) to enter."
						

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)

			await ctx.send(embed=embed)	




	@commands.command(name="startlinear", aliases = ["sle","linear"], hidden = True)
	@is_lotto()
	async def startlinear(self,ctx,prize:int):
		print(ctx.invoked_with)

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			self.lottoObject["prizes"] = prize
			self.lottoObject["prizecount"] = 1
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "linear"

			self.lottoEntries = {}

			title = self.lottoObject["owner"] + " has started a linear lotto."
			description = "Prize: $" + str("{:,.0f}".format(self.lottoObject["prize"])) + " per entry."
			footer = "Type !join (or !j or !le) to enter."						

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)

			await ctx.send(embed=embed)	





	@commands.command(name="firstid", aliases = ["fid"], hidden = True)
	@is_lotto()
	async def firstid(self,ctx, *, prize):
		print(ctx.invoked_with)

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)

		else:
			await ctx.send("```Problem with file```")
			return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.userlist = dict
			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			self.lottoObject["prizes"] = prize
			self.lottoObject["prizecount"] = 1
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "fid"

			self.fidlisten = True
			self.fidlistenwho = ctx.author
			self.listenChannel = ctx.channel


			title = self.lottoObject["owner"] + " has started a FID."
			description = "First person to type their ID wins:"
			description = description + "\n" + "Prize: '" + self.lottoObject["prize"] + "'"
			footer = "Type your torn ID to enter."
						

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)

			await ctx.send(embed=embed)	



		return

	@commands.command(name="firsttosay", aliases = ["fts"], hidden = True)
	@is_lotto()
	async def firsttosay(self,ctx, *, prize):
		print(ctx.invoked_with)

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)

		else:
			await ctx.send("```Problem with file```")
			return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.ftsphrase = random.choice(self.ftswordlist)

			self.userlist = dict
			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			self.lottoObject["prizes"] = prize
			self.lottoObject["prizecount"] = 1
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "fts"

			self.ftslisten = True
			self.ftslistenwho = ctx.author
			self.listenChannel = ctx.channel


			title = self.lottoObject["owner"] + " has started a FTS."
			description = "First person to type '**" + self.ftsphrase + "**' wins:"
			description = description + "\n" + "Prize: '" + self.lottoObject["prize"] + "'"
			footer = "Type the phrase above to enter."
						

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)

			await ctx.send(embed=embed)	



		return




	@commands.command(name="startadderlotto", aliases = ["sal","startadd"], hidden = True)
	@is_lotto()
	async def startaddderlotto(self,ctx, *, prizeline):
		print(ctx.invoked_with)

		#print(prizeline)
		incremental = 0

		splitprize = prizeline.split(" ")
		#print(splitprize)

		#print(len(splitprize))

		lastitem = splitprize[len(splitprize)-1]

		#print(lastitem)

		if len(splitprize) == 1 and prizeline.startswith("x") and prizeline[1:].isdigit():
			await ctx.send("```I think you forget to specify a prize```")
			return

		if lastitem.startswith("x") and lastitem[1:].isdigit():

			prize = prizeline[0:len(prizeline)-len(lastitem)-1]

			incremental = int(lastitem[1:])
		else:
			prize = prizeline
			incremental = 1

		#await ctx.send("Prize name: " + prize + " - Number of prizes given per entrant: " + str(incremental))
		#print(incremental)
		#print(prize)

		#return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			self.lottoObject["prizes"] = prize
			self.lottoObject["prizecount"] = 1

			self.lottoObject["incremental"] = incremental

			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "adder"


			self.lottoEntries = {}

			title = self.lottoObject["owner"] + " has started an adder lotto."
			description = "Prize: " + str(self.lottoObject["incremental"]) + "x '" + self.lottoObject["prize"] + "' per entry."

			footer = "Type !join (or !j) to enter."

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)

			await ctx.send(embed=embed)	



	@commands.command(name="startmultilotto", aliases = ["sml","startmulti"], hidden = True)
	@is_lotto()
	async def startmultilotto(self,ctx,*, prize):
		print(ctx.invoked_with)

		if len(prize.split(",")) == 1:
			await ctx.send("```This is the multi command - your prizes should be seperated by commas.  E.g. !sml prize 1, prize 2, prize 3```")
			return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			prizes = prize.split(",")
			self.lottoObject["prizes"] = prizes
			self.lottoObject["prizecount"] = len(prizes)
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "multi"


			self.lottoEntries = {}

			title = self.lottoObject["owner"] + " has started a multi lotto."
			description = "Prizes: \n"

			for aprize in prizes:
				description = description + " - " + aprize.strip() + "\n"			
			footer = "Type !join (or !j) to enter."

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)
			await ctx.send(embed=embed)	

		return			


	@commands.command(name="startdoorlotto", aliases = ["sdl","door"], hidden = True)
	@is_lotto()
	async def startdoorlotto(self,ctx,*, prize):
		print(ctx.invoked_with)

		await ctx.message.delete()

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)

		else:
			await ctx.send("```Problem with file```")
			return


		if len(prize.split(",")) == 1:
			await ctx.send("```This lotto type needs at least 2 prizes your prizes should be seperated by commas.  E.g. !door prize 1, prize 2, prize 3```")
			return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running```")
			return

		if self.listen == True:
			await ctx.send("```You cannot start a lotto as I am listening for response from " + self.listenwho.display_name + ".```")
			return		

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to start a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to start a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to start a lotto```")
		else:

			self.userlist = dict
			self.doorlisten = True
			self.doorlistenwho = ctx.author
			self.lottoObject["status"] = "On"
			self.lottoObject["owner"] = member.display_name
			self.lottoObject["ownerID"] = torn_id
			self.lottoObject["prize"] = prize

			prizes = prize.split(",")
			self.lottoObject["prizes"] = prizes
			self.lottoObject["prizecount"] = len(prizes)
			self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())

			self.lottoObject["lottotype"] = "door"


			self.lottoEntries = {}

			title = self.lottoObject["owner"] + " has started a door lotto."
			description = "You will only know the prizes once the winner picks a door. \n"
			acount = 1
			for aprize in prizes:
				description = description + " - Door " + str(acount) + "\n"
				acount = acount + 1			

			footer = "Type !join (or !j) to enter."

			role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
			await ctx.send(role.mention)

			embed = discord.Embed(title=title, 
				colour=discord.Colour.dark_green(), 
				description = description)
			
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)
			await ctx.send(embed=embed)	
			
		return



	@commands.command(name="lotto", hidden = True)
	@is_lotto()
	async def lotto(self,ctx):
		print(ctx.invoked_with)
		footer = "Type !join (or !j) to enter."
		if self.lottoObject["status"] == "Off":
			await ctx.send("```NO LOTTO RUNNING - Feel free to start one.```")
		else:
			if self.lottoObject["lottotype"] == "linear":
				title = "Linear lotto is currently running. "
				description = "Prize: $" + str("{:,.0f}".format(self.lottoObject["prize"])) + " per entrant"
				description = description + "\n" + "Current prize total: $" + str("{:,.0f}".format(self.lottoObject["prize"] * (len(self.lottoEntries) + 1)))
				description = description + "\n" 
				footer = "Type !join (or !j or !le) to enter."

			elif self.lottoObject["lottotype"] == "adder":
				title = "Adder lotto is currently running."
				description = "Prize: " + str("{:,.0f}".format(self.lottoObject["incremental"])) + "x '" + self.lottoObject["prize"] + "' per entry."
				if len(self.lottoEntries) == 0:
					description = description = "\n" + "No-one has entered the lotto yet."
				else:
					description = description + "\n" + "Current prize: " + str("{:,.0f}".format(self.lottoObject["incremental"] * len(self.lottoEntries))) + "x '" + self.lottoObject["prize"] + "'"
				description = description + "\n" 

			elif self.lottoObject["lottotype"] == "multi":
				title = "Multi lotto is currently running. "
				description = "Prizes:"
				description = description + "\n" 
				for aprize in self.lottoObject["prizes"]:
					description = description + " - " + aprize.strip() + "\n"			


			elif self.lottoObject["lottotype"] == "door":
				title = "Door lotto is currently running. "
				description = "Prizes: to be confirmed when winner picks a door"
				description = description + "\n" 
				 

			else:
				title = "Lotto is currently running."

				description = "Prize: '" + self.lottoObject["prize"] + "'"
				description = description + "\n" 

			description = description + "\n" + self.lottoObject["owner"] + " started lotto at " + datetime.utcfromtimestamp(self.lottoObject["timestamp"]).strftime("%H:%M")

			footer = footer + "\nThere are currently " + str(len(self.lottoEntries)) + " entries in the lotto."
			embed = discord.Embed(title=title, 
				colour=discord.Colour.purple(), 
				description = description)
			embed.set_footer(text=footer)
			await ctx.send(embed=embed)	



	@commands.command(name='join', aliases=["j","le"], hidden = True)
	@is_lotto()
	async def join(self, ctx):
		#print("join")
		print(ctx.invoked_with)
		cmdalias = ctx.invoked_with
		if self.lottoObject["status"] == "Off" or self.lottoObject["lottotype"] == "fid" or self.lottoObject["lottotype"] == "fts":
			
			#await ctx.send("```NO LOTTO RUNNING - Feel free to start one.```")
			linklinst = [
				"https://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558",
				"https://tenor.com/view/haha-good-one-the-office-smh-no-gif-14556369",
				"https://tenor.com/view/gordon-ramsey-shame-no-disappointed-disappointment-gif-4705923",
				"https://tenor.com/view/kid-sad-face-pout-baby-gif-10184641",
				"https://tenor.com/view/no-nooo-nope-eat-fingerwag-gif-23757070",
				"https://tenor.com/view/no-let-me-think-nope-no-way-hmm-no-gif-22904160",
				"https://tenor.com/view/despicbable-me-minions-uh-no-no-eh-no-gif-3418009",
				"https://tenor.com/view/elmo-shrug-i-dont-know-gif-14167687",
				"https://tenor.com/view/mr-bean-checking-time-waiting-gif-11570520",
				"https://tenor.com/view/no-sleep-its-been84years-titanic-gif-13077787",
				"https://tenor.com/view/never-gets-old-perfection-serious-happy-proud-gif-12347134"
				]
			response = random.choice(linklinst)
			await ctx.send(response)
			return		

		if cmdalias == "le" and self.lottoObject["lottotype"] != "linear":
			await ctx.send("```Only use !le for linear lottos - for normal lotto use !j or !join```")
			return

		member = ctx.author
		#print(member)
		
		torn_id = await self.checklottouser(member)
		#print(torn_id)


		if torn_id == "missing user":
			await ctx.send("```You must register with the bot to be able to join a lotto```")
		elif torn_id == "missing api":
			await ctx.send("```You must add your api to the bot to be able to join a lotto```")
		elif torn_id == "invalid api":
			await ctx.send("```Your API is not valid, you must re-add a valid api to the bot to be able to join a lotto```")
		else:

			for user in self.lottoEntries:
				if self.lottoEntries[user] == torn_id:
					await ctx.send("```You are already in the lotto (no multi entries allowed)```")
					return
			
			if torn_id == self.lottoObject["ownerID"]:
				await ctx.send("```You cannot enter your own lotto```")
				return

			self.lottoEntries[len(self.lottoEntries)+1] = torn_id

			#print(self.lottoEntries)
			footer = "Type !join (or !j) to enter."

			if self.lottoObject["lottotype"] == "linear":
				title = member.display_name + " has joined the linear lotto."
				description = "Lotto Prize: $" + str("{:,.0f}".format(self.lottoObject["prize"])) + " per entry."
				description = description + "\n" + "Current prize total: $" + str("{:,.0f}".format(self.lottoObject["prize"] * (len(self.lottoEntries) + 1))) 
				footer = "Type !join (or !j or !le) to enter."

			elif self.lottoObject["lottotype"] == "adder":
				title = member.display_name + " has joined the adder lotto."
				description = "Lotto Prize: " + str(self.lottoObject["incremental"]) + "x '" + self.lottoObject["prize"] + "' per entry."
				description = description + "\n" +  "Current Prize total: " + str("{:,.0f}".format(self.lottoObject["incremental"] * len(self.lottoEntries))) + "x '" + self.lottoObject["prize"]  + "'"
				
			elif self.lottoObject["lottotype"] == "multi":
				title = member.display_name + " has joined the multi lotto."
				description = "Prize:" + "\n"
				for aprize in self.lottoObject["prizes"]:
					description = description + " - " + aprize.strip() + "\n"	

			elif self.lottoObject["lottotype"] == "door":
				title = member.display_name + " has joined the door lotto."
				description = "Lotto Prize will only be known when the winner chooses a door!" 
				
			else:
				title = member.display_name + " has joined the lotto."
				description = "Lotto Prize: '" + self.lottoObject["prize"] + "'" 

			description = description + "\n" + "Entry # " + str(len(self.lottoEntries)) + "."
			footer = footer + "\n" + "Lotto by " + self.lottoObject["owner"] + " started at " + datetime.utcfromtimestamp(self.lottoObject["timestamp"]).strftime("%H:%M")

			embed = discord.Embed(title=title, 
				colour=discord.Colour.green(), 
				description = description)
			embed.set_thumbnail(url=member.avatar_url)
			embed.set_footer(text=footer)	

			await ctx.send(embed=embed)	

		return



	@commands.command(name='cancellotto', aliases=["cl"], hidden = True)
	@is_lotto()
	async def cancellotto(self, ctx):
		print(ctx.invoked_with)
		if self.lottoObject["status"] != "On":
			await ctx.send("```There is no lotto currently running```")
			return
					
		member = ctx.author
		manager = False
		for role in member.roles:
			#print(role.name)
			if self.lottoMgr == role.name:
				manager = True

		if manager == True:
			await ctx.send("```Lotto cancelled by order of management```")
			self.lottoObject["status"] = "Off"
			self.fidlisten = False
			self.fidlistenwho = ""
			self.ftslisten = False
			self.ftslistenwho = ""
			self.doorlisten = False
			self.doorlistenwho = ""
					
		else:
			await ctx.send("```Only management can cancel lottos```")
				
		return
	

	@commands.command(name='draw', hidden = True)
	@is_lotto()
	async def draw(self, ctx):
		print(ctx.invoked_with)
	
		if self.lottoObject["status"] != "On":
			await ctx.send("```There is no lotto currently running```")
			return
					
		

		member = ctx.author

		if self.lottoObject["owner"] != member.display_name:
			await ctx.send("```Only " + self.lottoObject["owner"] +" can draw the lotto```")
			return			


		if len(self.lottoEntries) == 0:
			await ctx.send("```No one has entered the lotto yet!  If you want to cancel please ask a manager.```")
			return
				
		await self.do_draw(ctx.channel, member)

		return


	async def do_draw(self, thechannel, member):
		print("do draw")

		if len(self.lottoEntries) == 1:
			winposition = 1
		else:
			winposition = randrange(1, len(self.lottoEntries))

		torn_id = self.lottoEntries[winposition]
		
		torn_name = __main__.get_user_name_from_id(torn_id)

		disco_id = await __main__.get_user_data_from_id(torn_id, "disco_id")

		#print(disco_id)
		user = await self.bot.fetch_user(disco_id)
		#print(user)

		myguild = thechannel.guild
		#print(myguild)

		user2 = await myguild.fetch_member(disco_id)
		#print(user2)


		if self.lottoObject["lottotype"] == "multi":
			title = "Multi Prize Lotto Draw........"

			description = torn_name + "[" + str(torn_id) + "] has won these prizes from " + self.lottoObject["owner"] + "."
			description = description + "\n"
			for aprize in self.lottoObject["prizes"]:
				description = description + " - " + aprize.strip() + "\n"

		elif self.lottoObject["lottotype"] == "door":
			title = "Door Prize Lotto Draw........"

			description = torn_name + "[" + str(torn_id) + "] has won a prize from " + self.lottoObject["owner"] + "."
			description = description + "\n"
			description = description + "Your prize is behind one of these doors:"
			description = description + "\n"
			doornum = 1
			for aprize in self.lottoObject["prizes"]:
				description = description + " - Door " + str(doornum) + "\n"
				doornum = doornum + 1
			description = description + "\n"
			description = description + torn_name + "[" + str(torn_id) + "] you need to type 'pick 1' or 'pick 2' etc to open one of the doors and look behind it"
			description = description + "\n"
			

		elif self.lottoObject["lottotype"] == "lotto":
			title = "Lotto Draw........"

			description = torn_name + "[" + str(torn_id) + "] has won **'" + self.lottoObject["prize"] + "'** from " + self.lottoObject["owner"] + "."
			description = description + "\n"

		elif self.lottoObject["lottotype"] == "adder":
			title = "Adder Lotto Draw........"

			description = torn_name + "[" + str(torn_id) + "] has won **" + str("{:,.0f}".format(self.lottoObject["incremental"] * len(self.lottoEntries))) + "x '" + self.lottoObject["prize"] + "'** from " + self.lottoObject["owner"] + "."
			description = description + "\n"

		else:
			title = "Linear Lotto Draw........"

			description = torn_name + "[" + str(torn_id) + "] has won **$" + str("{:,.0f}".format(self.lottoObject["prize"] * (len(self.lottoEntries) + 1))) + "** from " + self.lottoObject["owner"] + "."
			description = description + "\n"

		description = description + "[Profile](https://www.torn.com/profiles.php?XID=" + str(torn_id) + ") link for " + torn_name + "."

		embed = discord.Embed(title=title, 
			colour=discord.Colour.blurple(), 
			description = description)
		
		await thechannel.send(user.mention)
		msg = await thechannel.send(embed=embed)

		self.lottoObject["status"] = "Off"
		self.lottoEntries = {}
		
		if self.lottoObject["lottotype"] == "door":
			self.lottoObject["listencount"] = 1
			self.doorlisten = True

			await self.dolisten(thechannel,user2,self.lottoObject["listencount"])

			cooldown = self.doortimer
			while cooldown != 0:
				#await thechannel.send(cooldown)
				cooldown = cooldown - 1

				footer = "You have " + str(cooldown) + " seconds to pick a door"

				msg.embeds[0].set_footer(text=footer)
				embed  = msg.embeds[0]
				await msg.edit(embed=embed)

				if cooldown == 10:
					await thechannel.send(user.mention)
					await thechannel.send("https://tenor.com/view/tick-tock-debate-me-community-muthafucka-gif-15396401")


				if self.doorlisten == False:
					return
				await asyncio.sleep(1)
			await self.dolistenoff()
			await thechannel.send("```Heh " + torn_name + ", you didn't choose a door now you will never know what the prizes were```")

		else:	
			self.lottoObject["listencount"] = self.lottoObject["prizecount"]
			#print(member)
		
			await self.dolisten(thechannel,member,self.lottoObject["listencount"])

			cooldown = self.listenTimer * self.lottoObject["listencount"]
			while cooldown != 0:
				cooldown = cooldown - 1
				if self.listen == False:
					return
				await asyncio.sleep(1)
			await self.dolistenoff()
			await thechannel.send("```Heh " + self.lottoObject["owner"] + ", you didn't provide a send line - speak to a manager and beg for listen to be turned on```")




	@commands.command(name='lastcall', aliases = ["lc"] , hidden = True)
	@is_lotto()
	async def lastcall(self, ctx):
		print(ctx.invoked_with)
		if self.lottoObject["status"] != "On":
			await ctx.send("```There is no lotto currently running```")
			return
					
		

		member = ctx.author

		if self.lottoObject["owner"] != member.display_name:
			await ctx.send("```Only " + self.lottoObject["owner"] +" can last call the lotto```")
			return			

		role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
		
		await ctx.send("@here" + " and " + role.mention)
		
		if self.lottoObject["lottotype"] == "linear":
			await ctx.send("```Last call for Linear lotto by " + self.lottoObject["owner"] + ", use !join (or !j or !le) to enter. Current prize is $" + str("{:,.0f}".format(self.lottoObject["prize"] * (len(self.lottoEntries) + 1))) + ".```")

		elif self.lottoObject["lottotype"] == "door":
			await ctx.send("```Last call for Door lotto by " + self.lottoObject["owner"] + ", use !join (or !j or !le) to enter. Current prize is chosen when winner is drawn.```")

		elif self.lottoObject["lottotype"] == "adder":
			await ctx.send("```Last call for Adder lotto by " + self.lottoObject["owner"] + ", use !join (or !j) to enter. Current prize is " + str("{:,.0f}".format(self.lottoObject["incremental"] * len(self.lottoEntries))) + "x '" + self.lottoObject["prize"] + "'.```")

		else:
			await ctx.send("```Last call for lotto by " + self.lottoObject["owner"] + ", use !join (or !j) for a chance to win '" + self.lottoObject["prize"] + "'.```")

		return


	@commands.command(name="cooldown", aliases=["cd"], hidden = True)
	@is_lotto()
	async def cooldown(self, ctx):
		print(ctx.invoked_with)
		if self.cooldownOn == True:
			await ctx.send("```Cooldown is already running```")
			return

		if self.lottoObject["status"] != "On":
			await ctx.send("```There is no lotto currently running```")
			return

		member = ctx.author

		if self.lottoObject["owner"] != member.display_name:
			await ctx.send("```Only " + self.lottoObject["owner"] +" can draw the lotto```")
			return			


		if len(self.lottoEntries) == 0:
			await ctx.send("```No one has entered the lotto yet!  If you want to cancel please ask a manager.```")
			return
	
		self.cooldownOn = True
		title = "Lotto will draw soon"
		countdown = self.cooldownTimer

		description = "Lotto will draw in " + str(countdown) + " seconds"
		
		embed = discord.Embed(title=title, 
			colour=discord.Colour.orange(), 
			description = description)
		
		msg = await ctx.send(embed=embed)

		while countdown != 0:
			countdown = countdown - 1
			
			msg.embeds[0].description = "Lotto will draw in " + str(countdown) + " seconds"
			embed  = msg.embeds[0]
			await msg.edit(embed=embed)
			await asyncio.sleep(1)
		msg.embeds[0].description = "DRAW......"
		embed  = msg.embeds[0]
		await msg.edit(embed=embed)
		self.cooldownOn = False

		await self.do_draw(ctx.channel, member)
		

		return


	@commands.command(name='listen', hidden = True)
	@is_lotto()
	async def listen(self, ctx, member: discord.Member, listencount: int=1):
		print(ctx.invoked_with)
		if await self.is_lotto_mgr(ctx.author) == False:
			await ctx.send("Command only for lotto managers")
			return

		if self.lottoObject["status"] == "On":
			await ctx.send("```There is a lotto already running - you cannot start listen at this time```")
			return


		if self.listen == True:
			await ctx.send("```I am already listening for response from " + self.listenwho.display_name + ".```")
			return		

		await self.dolisten(ctx.channel, member, listencount)
		return


	async def dolisten(self, channel, member, listencount:int=1):

		if self.lottoObject["lottotype"] == "door":
			self.listenChannel = channel
			self.listenwho = member
			self.lottoObject["listencount"] = listencount
		
		else:
			self.listen = True
			self.listenChannel = channel
			self.listenwho = member
			self.lottoObject["listencount"] = listencount
			if listencount > 1:
				await self.listenChannel.send("```" + str(listencount) + " x listens turned on for " + member.display_name + " please paste your send lines.```")
			else:
				await self.listenChannel.send("```Listen turned on for " + member.display_name + " please paste your send line.```")
		return



	@commands.command(name='listenoff', hidden = True)
	@is_lotto()
	async def listenoff(self,ctx):
		print(ctx.invoked_with)
		member = ctx.author

		if await self.is_lotto_mgr(member) == False:
			await ctx.send("Command only for lotto managers")
			return
		
		await self.dolistenoff()
		await ctx.channel.send("```Listen turned off```")


		return


	async def dolistenoff(self):
		self.listen = False
		self.listenChannel = ""
		self.listenwho = ""
		self.lottoObject["listencount"] = 1
		return


	@commands.command(name='total', hidden = True)
	@is_lotto()
	async def total(self, ctx, member: typing.Union[discord.Member,str] = "NA"):
		print(ctx.invoked_with)
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:
			if os.path.isfile("./prizes.json"):

				with open("./prizes.json","r") as inf:
					dict = json.load(inf)
				if str(member.id) in dict:
					cashValue = dict[str(member.id)].get("cashValue",0)
					cashCount = dict[str(member.id)].get("cashCount",0)
					itemValue = dict[str(member.id)].get("itemValue",0)
					itemCount = dict[str(member.id)].get("itemCount",0)
					totalValue = cashValue + itemValue
					totalCount = cashCount + itemCount
					
					maxPrizeValue = dict[str(member.id)].get("maxPrizeValue",0)
					firstTimestamp = dict[str(member.id)].get("firstTimestamp",0)
					lastTimestamp = dict[str(member.id)].get("lastTimestamp",0)

					title = "Lotto totals for " + member.display_name + "."

					description = "First lotto run on: " + datetime.fromtimestamp(firstTimestamp).strftime("%d %B %Y")
					description = description + "\n" 
					description = description + "Last lotto run on: " + datetime.fromtimestamp(lastTimestamp).strftime("%d %B %Y")
					description = description + "\n"
					description = description + "Maximum prize valiue given so far: $" + str("{:,.0f}".format(maxPrizeValue))
					
					cashFieldName = "Cash"
					if cashCount == 0:
						cashFieldValue = "No cash prizes sent as yet."
					else:
						cashFieldValue = "Prize Count: " + str("{:,.0f}".format(cashCount))
						cashFieldValue = cashFieldValue + "\n"
						cashFieldValue = cashFieldValue + "Total Value: $" + str("{:,.0f}".format(cashValue))
						cashFieldValue = cashFieldValue + "\n"
						cashFieldValue = cashFieldValue + "Average Value: $" + str("{:,.0f}".format(cashValue/cashCount))
					
					itemFieldName = "Items"
					if itemCount == 0:
						itemFieldValue = "No item prizes sent as yet."
					else:
						itemFieldValue = "Prize Count: " + str("{:,.0f}".format(itemCount))
						itemFieldValue = itemFieldValue + "\n"
						itemFieldValue = itemFieldValue + "Total Value: $" + str("{:,.0f}".format(itemValue))
						itemFieldValue = itemFieldValue + "\n"
						itemFieldValue = itemFieldValue + "Average Value: $" + str("{:,.0f}".format(itemValue/itemCount))

					totalFieldName = "Totals"
					if totalCount == 0:
						totalFieldValue = "No prizes sent as yet."
					else:
						totalFieldValue = "Prize Count: " + str("{:,.0f}".format(totalCount))
						totalFieldValue = totalFieldValue + "\n"
						totalFieldValue = totalFieldValue + "Total Value: $" + str("{:,.0f}".format(totalValue))
						totalFieldValue = totalFieldValue + "\n"
						totalFieldValue = totalFieldValue + "Average Value: $" + str("{:,.0f}".format(totalValue/totalCount))


					lottoList = await self.getLottoList()

					keyindex = list(lottoList).index(str(member.id)) if str(member.id) in lottoList else None

					leaderPosition = keyindex + 1

					footer = "Position in lotto leaderboard: " + str(leaderPosition)

					embed = discord.Embed(title=title, 
						colour=discord.Colour.purple(), 
						description = description)

					embed.add_field(name=cashFieldName, value=cashFieldValue,inline=True)
					embed.add_field(name=itemFieldName, value=itemFieldValue,inline=True)
					embed.add_field(name=totalFieldName, value=totalFieldValue,inline=False)
					
					embed.set_thumbnail(url=member.avatar_url)

					embed.set_footer(text=footer)	

					await ctx.send(embed=embed)	


					return
				else:
					await ctx.send("```" + member.display_name + " has not completed any lottos as yet.```")
					return
			else:
				await ctx.send("```Problem with leaderboard file - see managers for details```")
				return


		elif member.lower() == "all":
			if os.path.isfile("./prizes.json"):
				cashValue = 0
				cashCount = 0
				itemValue = 0
				itemCount = 0
				maxPrizeValue = 0
				firstTimestamp = datetime.timestamp(datetime.utcnow())
				lastTimestamp = 0


				with open("./prizes.json","r") as inf:
					dict = json.load(inf)
				for member_id in dict:
					cashValue = cashValue + dict[member_id].get("cashValue",0)
					cashCount = cashCount + dict[member_id].get("cashCount",0)
					itemValue = itemValue + dict[member_id].get("itemValue",0)
					itemCount = itemCount + dict[member_id].get("itemCount",0)
					totalValue = cashValue + itemValue
					totalCount = cashCount + itemCount
					
					if dict[member_id].get("maxPrizeValue",0) > maxPrizeValue:
						maxPrizeValue = dict[member_id].get("maxPrizeValue",0)

					if dict[member_id].get("firstTimestamp",0) < firstTimestamp:
						firstTimestamp = dict[member_id].get("firstTimestamp",0)

					if dict[member_id].get("lastTimestamp",0) > lastTimestamp:
						lastTimestamp = dict[member_id].get("lastTimestamp",0)


				title = "Lotto totals for entire lottery."

				description = "First lotto run on: " + datetime.fromtimestamp(firstTimestamp).strftime("%d %B %Y")
				description = description + "\n" 
				description = description + "Last lotto run on: " + datetime.fromtimestamp(lastTimestamp).strftime("%d %B %Y")
				description = description + "\n"
				description = description + "Maximum prize value given so far: $" + str("{:,.0f}".format(maxPrizeValue))
				
				cashFieldName = "Cash"
				if cashCount == 0:
					cashFieldValue = "No cash prizes sent as yet."
				else:
					cashFieldValue = "Prize Count: " + str("{:,.0f}".format(cashCount))
					cashFieldValue = cashFieldValue + "\n"
					cashFieldValue = cashFieldValue + "Total Value: $" + str("{:,.0f}".format(cashValue))
					cashFieldValue = cashFieldValue + "\n"
					cashFieldValue = cashFieldValue + "Average Value: $" + str("{:,.0f}".format(cashValue/cashCount))
				
				itemFieldName = "Items"
				if itemCount == 0:
					itemFieldValue = "No item prizes sent as yet."
				else:
					itemFieldValue = "Prize Count: " + str("{:,.0f}".format(itemCount))
					itemFieldValue = itemFieldValue + "\n"
					itemFieldValue = itemFieldValue + "Total Value: $" + str("{:,.0f}".format(itemValue))
					itemFieldValue = itemFieldValue + "\n"
					itemFieldValue = itemFieldValue + "Average Value: $" + str("{:,.0f}".format(itemValue/itemCount))

				totalFieldName = "Totals"
				if totalCount == 0:
					totalFieldValue = "No prizes sent as yet."
				else:
					totalFieldValue = "Prize Count: " + str("{:,.0f}".format(totalCount))
					totalFieldValue = totalFieldValue + "\n"
					totalFieldValue = totalFieldValue + "Total Value: $" + str("{:,.0f}".format(totalValue))
					totalFieldValue = totalFieldValue + "\n"
					totalFieldValue = totalFieldValue + "Average Value: $" + str("{:,.0f}".format(totalValue/totalCount))


				embed = discord.Embed(title=title, 
					colour=discord.Colour.purple(), 
					description = description)

				embed.add_field(name=cashFieldName, value=cashFieldValue,inline=True)
				embed.add_field(name=itemFieldName, value=itemFieldValue,inline=True)
				embed.add_field(name=totalFieldName, value=totalFieldValue,inline=False)
					

				await ctx.send(embed=embed)	


				return
			else:
				await ctx.send("```Problem with leaderboard file - see managers for details```")
				return



		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameter is discord name (e.g. @Accy)")
			return


	@commands.command(name="top", hidden = True)
	@is_lotto()
	async def top(self,ctx, topCount: int = 0):
		print(ctx.invoked_with)
		if topCount < 0:
			await ctx.send("```What are you playing at?```")
			return
		#if topCount > 10:
		#	topCount = 10
		if topCount == 0:
			maxListSize = self.topLeaderCount
		else:
			maxListSize = topCount
		lottoList = await self.getLottoList()
		if "Error" in lottoList:
			await ctx.send("```There was issue with the leaderboard - see manager about it```")
			return
		if len(lottoList) < maxListSize:
			maxListSize = len(lottoList)
			topList = lottoList
		else:
			topList = {k: lottoList[k] for k in list(lottoList)[:maxListSize]}
#			first2pairs = {k: mydict[k] for k in list(mydict)[:2]}

		title = "Lotto leaderboard (top " + str(maxListSize) + " players)"
		description = ""
		position = 1
		for member in topList:
			user = await self.bot.fetch_user(int(member))
			description = description + "" + str(position) + ": " + ctx.guild.get_member(int(member)).display_name
			#description = description + "\n"
			description = description + " ($" + str("{:,.0f}".format(topList[member])) + ")"
			description = description + "\n"
			#description = description + "\n"
			position = position + 1

		footer = "Complete leaderboard size: " + str(len(lottoList))
		embed = discord.Embed(title=title, 
			colour=discord.Colour.purple(), 
			description = description)
		embed.set_footer(text=footer)
		await ctx.send(embed=embed)

	
	async def getLottoList(self):
		
		lottoDict = {}
		if os.path.isfile("./prizes.json"):

			with open("./prizes.json","r") as inf:
				adict = json.load(inf)
			if len(adict) == 0:
				return "Error: no entries"
			for member in adict:
				lottoDict[member] = adict[member]["cashValue"]+adict[member]["itemValue"]
				sortLottolist = sorted(lottoDict.items(), key=lambda x:x[1], reverse = True)
				sortLottolist = dict(sortLottolist)
	
			return sortLottolist
		else:
			return "Error: File issue"
		return
		

	@commands.command(name="lottohelp", aliases=["lh"], hidden = True)
	@is_lotto()
	async def lottohelp(self, ctx, helpcommand = "na"):
		print(ctx.invoked_with)
		if helpcommand.startswith("!"):
			helpcommand = helpcommand[1:]

		helpcommand = helpcommand.lower()

		lottoHelpDict = {}
		if os.path.isfile("./lottohelp.json"):

			with open("./lottohelp.json","r") as inf:
				adict = json.load(inf)
			if len(adict) == 0:
				await ctx.send("```problem with help file```")
				return
	
			if helpcommand != "na":
				helpItem = adict.get(helpcommand,"notfound")
				if helpItem == "notfound":
					await ctx.send("```Help for command " + helpcommand + " not found```")
					return


				title = "Lotto Command Help Details"

				description = "**!" + helpcommand + "**"
				description = description + "\n"

				description = description + adict[helpcommand]["longhelp"]
				description = description + "\n"
				description = description + "Aliases: " + adict[helpcommand]["aliases"]

				footer = "Type !lh with no parameter for list of all lotto commands"
				embed = discord.Embed(title=title, 
					colour=discord.Colour.gold(), 
					description = description)
				embed.set_footer(text=footer)
				await ctx.send(embed=embed)
				
				return

			title = "Lotto Help Command List"
			description = "All lottery commands can only be run in the 'lotto' channel. \nAll commands start with !\nAliases for commands are in brackets (e.g. join (j) means command !join can also be run using !j \nYou must be fully registered with the Bot to run or join a lotto."
			description = description + "\n"
			description = description + "\n"

			
			for helpcommand in adict:
				if adict[helpcommand]["main"] == "True":

					description = description + "**" + helpcommand + "** (" + adict[helpcommand]["aliases"] + ")" 
					description = description + "\n"
					description = description + adict[helpcommand]["shorthelp"]
					description = description + "\n"
					description = description + "\n"


			footer = "Type !lh <Command> for help on individual commands"
			embed = discord.Embed(title=title, 
				colour=discord.Colour.gold(), 
				description = description)
			embed.set_footer(text=footer)
			await ctx.send(embed=embed)

		else:
			await ctx.send("```problem with help file```")
			return

	@commands.command(name='lottorole', aliases = ["lottoping"] ,help="Add the lotto ping role (or remove it if you already have it")
	async def lottorole(self,ctx):

		role = discord.utils.get(ctx.guild.roles, name=self.lottoPing)
		user = ctx.author

		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}")
		else:
		  	await user.add_roles(role) #adds role if not already has it
		  	await ctx.send(f"Added {role} to {user.mention}") 

		return


	@commands.command(name='bottom', hidden = True)
	@is_lotto()
	async def bottom(self, ctx):
		print(ctx.invoked_with)

		await ctx.send("```I have not checked but it must be Purp at the bottom surely!!!```")
		return
		

	@commands.command(name='openit', hidden = True)
	async def openit(self, ctx, *, line:str):
		print(ctx.invoked_with)
		
		description = ""
		itemcount = 0

		if line.startswith("You open up the pack to find "):
			if "Vicodin" in line:
				itemname = "Vicodin"
				itemcount = 10
			else:
				itemname = "Xanax"
				itemcount = 10
			itemvalue = await self.get_items_value(itemname)
			totalvalue = itemcount * itemvalue

			title = "Opening Drug Pack ........"


			containervalue = await self.get_items_value("Drug Pack")

			
			footer = "Value of Drug Pack" + " $" + str("{:,.0f}".format(containervalue))

			description = description + str(itemcount) + " x " + itemname + " ($" + str("{:,.0f}".format(totalvalue)) + ")" +"\n"
			
			containtertotal = totalvalue

			description = description + "\n"

			description = description + "***Total for content of Drug Pack***\n"
			description = description + "$" + str("{:,.0f}".format(containtertotal))
		

		else:

			if line.startswith("You opened the "):
				linex = re.search('(You opened the )(.*?)( and received )(.*)', line)
			else:
				if " gained " in line:
					linex = re.search('(You opened a )(.*?)( and gained )(.*)', line)
				else:
					linex = re.search('(You opened a )(.*?)( containing )(.*)', line)
				
			

			title = "Opening " + linex.group(2) + "........"
			
			items =  linex.group(4).split(",")
			
			itemdict = {}
			containtertotal = 0

			containtervalue = await self.get_items_value(linex.group(2))
			
			for item in items:

				itemname = re.search('(?<=x )(.*)', item).group(1)

				itemcount = int(re.search('(.*?)(?=x)', item).group(0))

				itemvalue = await self.get_items_value(itemname)

				totalvalue = itemcount * itemvalue

				itemdict[itemname] = {"itemcount": itemcount, "itemvalue": itemvalue, "totalvalue": totalvalue}

		#	itemcount = len(items)

			#await ctx.send(line2)
			#await ctx.send(itemdict)
			
			footer = "Value of " + linex.group(2) + " $" + str("{:,.0f}".format(containtervalue))

			for item in itemdict:
				description = description + str(itemdict[item]["itemcount"]) + " x " + item + " ($" + str("{:,.0f}".format(itemdict[item]["totalvalue"])) + ")" +"\n"
				containtertotal = containtertotal + itemdict[item]["totalvalue"]

			description = description + "\n"

			description = description + "***Total for content of " + linex.group(2) + "***\n"
			description = description + "$" + str("{:,.0f}".format(containtertotal))
		


		embed = discord.Embed(title=title, 
			colour=discord.Colour.gold(), 
			description = description)
		embed.set_footer(text=footer)

		await ctx.send(embed=embed)


	@commands.command(name='win', hidden = True)
	@is_lotto()
	async def win(self, ctx):
		print(ctx.invoked_with)
		member = ctx.author

		linklinst = [
			"https://tenor.com/view/loser-gif-8484142",
			"https://tenor.com/view/loser-looser-gif-9321909",
			"https://tenor.com/view/you-lose-good-day-sir-willy-wonka-and-the-chocolate-factory-you-lost-you-miss-nervous-gif-21443353"
			]
		response = random.choice(linklinst)
		await ctx.send(response)

		return
		


	@commands.command(name='fake', hidden = True)
	@is_lotto()
	async def fake(self, ctx):
		print(ctx.invoked_with)
		member = ctx.author

		if await self.is_lotto_mgr(member) == False:
			await ctx.send("Command only for lotto managers")
			return
		
		self.lottoObject["status"] = "On"
		self.lottoObject["owner"] = "Brasshole"
		self.lottoObject["ownerID"] = 2524886
		self.lottoObject["prize"] = "TEST"
		self.lottoObject["lottotype"] = "lotto"
		self.lottoObject["timestamp"] = datetime.timestamp(datetime.utcnow())
		self.lottoEntries = {}


	@commands.command(name='addplayers', hidden = True)
	@is_lotto()
	async def addplayers(self, ctx):
		print(ctx.invoked_with)
		member = ctx.author

		if await self.is_lotto_mgr(member) == False:
			await ctx.send("Command only for lotto managers")
			return
		
		self.lottoEntries = {1: '2512014', 2: '2344388', 3: '2512014', 4: '2339658', 5: '2360622'}



def setup(bot):
	bot.add_cog(Lotto_cog(bot))