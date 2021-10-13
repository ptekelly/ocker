import discord
import typing
import os
import requests
import __main__
import json

from discord.ext import commands


class Faction(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		print('Faction COG loaded')


	@commands.Cog.listener()
	async def on_ready(self):
		print('Faction COG Ready')




	async def get_married(self,torn_id):
		
		found = False
		married = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "profile"
				
				APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					married = "Call Error"
				else:
					if v1["married"]["spouse_id"] == 0:
						married = "False"
					else:
						married = "True"

		return(married)

	
	async def get_e(self,torn_id):
		
		found = False
		energy_current = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "bars"
				
				APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					energy_current = "Call Error"
				else:
					energy = v1['energy']
					energy_current = energy['current']
					energy_max = energy['maximum']
					energy_full = energy['fulltime']

					energy_current = str(energy_current) + "e"
			

		return(energy_current)


	async def get_cd(self,torn_id):
		
		found = False
		cd_text = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "cooldowns"
				
				APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					drug_cd = "Call Error"
					cd_text = drug_cd

				else:
				
					#print(v1)
					cooldowns = v1['cooldowns']
					drug_cd = cooldowns['drug']
					medical_cd = cooldowns['medical']
					booster_cd = cooldowns['booster']


					if drug_cd > 0:
						xseconds = drug_cd
						xdays = divmod(xseconds, (60*60*24))[0]
						xdaysr = divmod(xseconds, (60*60*24))[1]
						xhours = divmod(xdaysr, (60*60))[0]
						xhoursr = divmod(xdaysr, (60*60))[1]
						xmins = divmod(xhoursr, (60))[0]
						xhoursr = divmod(xhours, (60))[1]
						
						cd_text = ""
						if xdays > 0:
							cd_text = cd_text + str(xdays) + "d "
						if xhours > 0:
							cd_text = cd_text + str(xhours) + "h "
						if xmins > 0:
							cd_text = cd_text + str(xmins) + "m "
				
						if (xdays + xhours + xmins) == 0:
							cd_text = "0 "
					else:
						cd_text = "0 "

					cd_text = cd_text + "cd"

		return(cd_text)
			
	
	async def get_nnb(self,torn_id):

		found = False
		nnb = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "bars"
				
				APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					nnb = "Call Error"
				else:
					nerve = v1['nerve']
					nerve_current = nerve['current']
					nerve_max = nerve['maximum']
					nerve_full = nerve['fulltime']

					nnb = str(nerve_max) + " NNB"
			

		return(nnb)

	
	async def get_maxhappy(self,torn_id):

		found = False
		max_hap = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "bars"
				
				APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					max_hap = "Call Error"
				else:
					happy = v1['happy']
					happy_current = happy['current']
					happy_max = happy['maximum']
					happy_full = happy['fulltime']

					max_hap = str(happy_max) + " MH"
			

		return(max_hap)
	


	async def get_property(self,torn_id):

		found = False
		property = "No API"

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			for disco_user in dict:
				if dict[disco_user]["torn_id"] == str(torn_id):
					if "torn_api" in dict[disco_user]:
						torn_api = dict[disco_user]["torn_api"]
						found = True

			if found == True:
				
				v_apiType = "user"
				v_apiSelection = "profile"
				
				APIURL = self.bot.v_apiAddress+v_apiType+'/?selections='+v_apiSelection+'&key='+torn_api
				r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
				v1 = r.json() # translates that response into a dict variable
				if "error" in v1:
					property = "Call Error"
				else:
					property = v1['property']			

		return(property)



	@commands.command(name='teams', aliases = ["faction", "team"], help='Provide a list of faction members split by teams')
	async def teams(self, ctx, extra = "NA"):

		#print(ctx.guild.roles)
		
		extra = extra.lower()
		if extra not in ["nnb","na"]:
			await ctx.send("What extra did you want? Only options so far is nnb")
			return
		
		embed = await self.teamwork(ctx.guild, extra)
		await ctx.send(embed=embed)
		return



	def is_mgt():
	    async def predicate(ctx):

	    	server_id = str(ctx.guild.id)
	    	this_channel = ctx.message.channel
	    	this_channel_name = this_channel.name
	    	this_channel_id = this_channel.id
	    	channel_allowed = False

	    	if os.path.isfile("./channels.json"):
	    		# File already exists
	    		with open("./channels.json","r") as inf:		
	    			channel_dict = json.load(inf)

	    			if server_id in channel_dict:
	    				#print("Server id and file exist")
	    				if this_channel_id == channel_dict[server_id]["mgt"]:
	    					#print("This channel matches allowd channel")
	    					channel_allowed = True

	    	if channel_allowed == False:
	    		#print("delete?")
	    		await ctx.message.delete()
	    	return channel_allowed
	    return commands.check(predicate)




	@commands.command(name='chain2', aliases = ["c2", "chains2"], hidden = True)
	@is_mgt()
	async def chain2(self,ctx):
		embed = await self.chainx(2)
		await ctx.send(embed=embed)
		return 

	@commands.command(name='chain4', aliases = ["c4", "chains4"], hidden = True)
	@is_mgt()
	async def chain4(self,ctx):
		embed = await self.chainx(4)
		await ctx.send(embed=embed)
		return 


	async def chainx(self,chaincount):

		v_apiType = "faction"
		v_apiSelection = "chains"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		
		if "error" in v1:
			raise __main__.APICallError("4chains")
			return
		chains = {}
		allchains = v1["chains"]
		for chain in allchains:
			if allchains[chain]["chain"] in [2500, 5000]:
				chains[chain] = allchains[chain]

		mykey = []
		for x in chains.keys():
			mykey.append(int(x))

		mykey.sort(reverse = True)


		sortlist = {}
		count = 1
		for key in mykey:
			if count > chaincount:
				break
			sortlist[str(key)] = chains[str(key)]
			count = count + 1
		
		keysort = sortlist

		#for chain in sortlist:
		#	print(str(chain) + ": " + str(sortlist[chain]))

		v_apiType = "faction"
		v_apiSelection = "basic"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		
		if "error" in v1:
			raise __main__.APICallError("4chain")
			return
		chainreports = {}
		for user in v1["members"]:
			chainreports[user] = {"name":v1["members"][user]["name"],"chains":{},"total":0}
			for chain in keysort:
				chainreports[user]["chains"][chain] = 0


		for chain in keysort:

			v_apiType = "torn"
			v_apiSelection = "chainreport"
	#		emded_desc="(**Attacks/Leaves/Respect**)" + "\n"

			APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(chain)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
			r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
			v1 = r.json() # translates that response into a dict variable
			
			if "error" in v1:
				raise __main__.APICallError("4chain")
				return
			
			chainList = {}

			members = v1["chainreport"]["members"]
			for user in members:
				if user in chainreports:
					chainreports[user]["chains"][chain] = members[user]["leave"]
			
		
		for user in chainreports:
			total = 0
			for chain in chainreports[user]["chains"]:
				total = total + chainreports[user]["chains"][chain]
			chainreports[user]["total"] = total
		#print(chainreports)

			
		sortlist = sorted(chainreports.items(), key=lambda x:x[1]["total"], reverse = True)
		sortlist = dict(sortlist)

		#print(sortlist)

		if chaincount == 2:
			emded_desc = "Format is ch1/ch2/**total**"
		else:
			emded_desc = "Format is ch1/ch2/ch3/ch4/**total**"
			
		emded_desc = emded_desc + "\n"
		emded_desc = emded_desc + "Chain IDs are:"
		emded_desc = emded_desc + "\n"
		for chain in keysort:
			emded_desc = emded_desc + str(chain) + "\n"
		emded_desc = emded_desc + "\n"


		for user in sortlist:
			emded_desc = emded_desc + sortlist[user]["name"] + "[" + str(user) + "] - "
			for chain in sortlist[user]["chains"]:
				emded_desc = emded_desc + str(sortlist[user]["chains"][chain]) + "/"

			emded_desc = emded_desc + "**" + str(sortlist[user]["total"]) + "**"
			emded_desc = emded_desc + "\n"

		#print(emded_desc)

		title_text = "Chain report"
		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		return(embed)
		




	@commands.command(name='chain', hidden = True)
	@is_mgt()
	async def chain(self,ctx):

		v_apiType = "faction"
		v_apiSelection = "basic"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		
		if "error" in v1:
			raise __main__.APICallError("basicFaction")
			return
		faction_members = {}
		for user in v1["members"]:
			faction_members[user] = v1["members"][user]["name"]

		v_apiType = "faction"
		v_apiSelection = "chainreport"
		emded_desc="(**Attacks/Leaves/Respect**)" + "\n"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		
		if "error" in v1:
			raise __main__.APICallError("basicFaction")
			return
		
		chainList = {}

		members = v1["chainreport"]["members"]
		for user in members:
			if user in faction_members:
				chainList[user] = {"name":faction_members[user] , "respect": members[user]["respect"],"attacks":members[user]["attacks"],"leaves":members[user]["leave"]}
			
			
		sortlist = sorted(chainList.items(), key=lambda x:x[1]["leaves"], reverse = True)
		sortlist = dict(sortlist)

		for user in sortlist:
			emded_desc = emded_desc + sortlist[user]["name"] + " (" + str(user) + ")"
			emded_desc = emded_desc + " - " + str(sortlist[user]["attacks"]) + "/" + str(sortlist[user]["leaves"])
			emded_desc = emded_desc + "/" + str(sortlist[user]["respect"])
			emded_desc = emded_desc + "\n"


		title_text = "Chain report"
		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
#		embed.set_footer(text="Option: " + extra)
		await ctx.send(embed=embed)
		return



	@commands.command(name='stacked', aliases = ["st"], hidden = True)
	@is_mgt()
	async def stacked(self,ctx):

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				user_dict = json.load(inf)
				#print("file found")
		else:
			raise __main__.NoFile("users.json")

		checkUserList = {}
		for user in user_dict:
			checkUserList[str(user_dict[user]["torn_id"])] = {"api": user_dict[user].get("torn_api","No API")}

#		print(checkUserList)

		vBasicFactionMembers = await self.basicFactionMembers()
		checkList = {}

		emded_desc = ""


		for member in vBasicFactionMembers:
			checkList[member] = {"name":vBasicFactionMembers[member]["name"]}
			if member in checkUserList:
				if checkUserList[member]["api"] == "No API":
					checkList[member]["result"] = "Not Setup"
				else:
					apicheck = await self.get_e(member)
					if apicheck == "Call Error":
						checkList[member]["result"] = "Not Setup"
					else:
						checkList[member]["result"] = "OK"

			else:
				checkList[member]["result"] = "Not Setup"

#		print(checkList)

		fullyList = {}
		setupList = {}
		withCDList = {}
		partiallyReadyList = {}
		notReadyList = {}
		notSetupList = {}

		for member in checkList:
			if checkList[member]["result"] == "Not Setup":
				notSetupList[member] = checkList[member]["name"]
			
			elif checkList[member]["result"] == "OK":
				setupList[member] = checkList[member]["name"]

		for member in setupList:
			current_e_txt = await self.get_e(member)
			current_e = int(current_e_txt.rstrip("e"))
			current_cd = await self.get_cd(member)
			if current_e == 1000 and current_cd == "0 cd":
				fullyList[member] = {"name":checkList[member]["name"], "cd":current_cd, "e":current_e_txt}
			elif current_e == 1000 and current_cd != "0 cd":
				withCDList[member] = {"name":checkList[member]["name"], "cd":current_cd, "e":current_e_txt}
			elif current_e < 150:
				notReadyList[member] = {"name":checkList[member]["name"], "cd":current_cd, "e":current_e_txt}
			else:
				partiallyReadyList[member] = {"name":checkList[member]["name"], "cd":current_cd, "e":current_e_txt}





		emded_desc = "**Fully Stacked [" + str(len(fullyList)) + "]**" + "\n"
		sortlist = sorted(fullyList.items(), key=lambda x:x[1]["name"].lower())
		sortlist = dict(sortlist)
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member]["name"] + " [" + str(member) + "] (" + sortlist[member]["cd"] + ", " + sortlist[member]["e"] + ")" +"\n"

		emded_desc = emded_desc  + "\n" + "**Stacked but with CD [" + str(len(withCDList)) + "]**" + "\n"
		sortlist = sorted(withCDList.items(), key=lambda x:x[1]["name"].lower())
		sortlist = dict(sortlist)
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member]["name"] + " [" + str(member) + "] (" + sortlist[member]["cd"] + ", " + sortlist[member]["e"] + ")" +"\n"

		emded_desc = emded_desc  + "\n" + "**Partially Stacked [" + str(len(partiallyReadyList)) + "]** (less than 1ke)" + "\n"
		sortlist = sorted(partiallyReadyList.items(), key=lambda x:x[1]["name"].lower())
		sortlist = dict(sortlist)
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member]["name"] + " [" + str(member) + "] (" + sortlist[member]["cd"] + ", " + sortlist[member]["e"] + ")" +"\n"

		emded_desc = emded_desc + "\n" + "**Not Stacking [" + str(len(notReadyList)) + "]** (less than 150e)" + "\n"
		sortlist = sorted(notReadyList.items(), key=lambda x:x[1]["name"].lower())
		sortlist = dict(sortlist)
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member]["name"] + " [" + str(member) + "] (" + sortlist[member]["cd"] + ", " + sortlist[member]["e"] + ")" +"\n"

		emded_desc = emded_desc + "\n" + "**User not setup with Ocker [" + str(len(notSetupList)) + "]**" + "\n"
		sortlist = sorted(notSetupList.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"


		title_text = "Stacking check"
		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		#embed.set_footer(text="Option: " + extra)
		await ctx.send(embed=embed)
		return


	@commands.command(name='botcheck', aliases = ["bc"], hidden = True)
	@is_mgt()
	async def botcheck(self,ctx):

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				user_dict = json.load(inf)
				#print("file found")
		else:
			raise __main__.NoFile("users.json")

		checkUserList = {}
		for user in user_dict:
			checkUserList[str(user_dict[user]["torn_id"])] = {"api": user_dict[user].get("torn_api","No API")}

#		print(checkUserList)

		vBasicFactionMembers = await self.basicFactionMembers()
		checkList = {}


		leftList = {}

		for member in checkUserList:
			if member not in vBasicFactionMembers:
				leftList[member] = __main__.get_user_name_from_id(member)



		emded_desc = ""


		for member in vBasicFactionMembers:
			checkList[member] = {"name":vBasicFactionMembers[member]["name"]}
			if member in checkUserList:
				if checkUserList[member]["api"] == "No API":
					checkList[member]["result"] = "No API"
				else:
					apicheck = await self.get_e(member)
					if apicheck == "Call Error":
						checkList[member]["result"] = "API Error"
					else:
						checkList[member]["result"] = "OK"

			else:
				checkList[member]["result"] = "No Torn ID"

#		print(checkList)

		ok_list = {}
		noIDList = {}
		noAPIList = {}
		aPIErrorList = {}

		for member in checkList:
			if checkList[member]["result"] == "No API":
				noAPIList[member] = checkList[member]["name"]
			
			elif checkList[member]["result"] == "No Torn ID":
				noIDList[member] = checkList[member]["name"]
			
			elif checkList[member]["result"] == "API Error":
				aPIErrorList[member] = checkList[member]["name"]

			elif checkList[member]["result"] == "OK":
				ok_list[member] = checkList[member]["name"]

#		print(noIDList)
		sortlist = sorted(noIDList.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
#		print(sortlist)
		emded_desc = "**Needs ID** [" + str(len(sortlist)) + "]" + "\n"
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"

		sortlist = sorted(noAPIList.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
		emded_desc = emded_desc  + "\n" + "**Needs API** [" + str(len(sortlist)) + "]" + "\n"
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"

		sortlist = sorted(aPIErrorList.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
		emded_desc = emded_desc + "\n" + "**API Error** [" + str(len(sortlist)) + "]" + "\n"
		for member in sortlist:
			emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"

		sortlist = sorted(ok_list.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
		emded_desc = emded_desc + "\n" + "**Complete** [" + str(len(sortlist)) + "]" + "\n"
		#for member in sortlist:
		#	emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"

		emded_desc = emded_desc + "\n" + "**Not in faction** [" + str(len(leftList)) + "]" + "\n"
		for member in leftList:
			emded_desc = emded_desc + leftList[member] + " [" + str(member) + "]" + "\n"


		title_text = "bot check"
		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		#embed.set_footer(text="Option: " + extra)
		await ctx.send(embed=embed)
		return


	@commands.command(name='xteams', aliases = ["xteam"], hidden = True)
	@is_mgt()
	async def xteams(self, ctx, extra = "NA"):
		extra = extra.lower()

		if extra not in ["e","cd","ecd","p","mh","nnb","mhp"]:
			await ctx.send("What extra did you want?")
			return

		embed = await self.teamwork(ctx.guild, extra)
		msg = await ctx.send(embed=embed)

		return


		
		
	
	async def teamwork(self, vguild, extra = "NA"):
		
		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				user_dict = json.load(inf)
				#print("file found")
		else:
			raise __main__.NoFile("users.json")

		faction_teams = ["Blue","Red","Green","Orange","Yellow","Pink"]

		faction_leader_role = "HelloHigh Leader"
		faction_manager_role = "Management"
		
		team_leader_role = "Leader of XXX Team"
		team_member_role = "XXX Team"

		vBasicFactionMembers = await self.basicFactionMembers()
		

		field_list = {}
		for team in faction_teams:
			member_list = ""
		
			#team leaders  
			role = discord.utils.get(vguild.roles, name=team_leader_role.replace("XXX", team))
			if role == None:
				leader_name = team_leader_role.replace("XXX", team) + " role not defined"
			else:
				if len(role.members) == 0:
					leader_name = "TBD"

				member = role.members[0].id
				if str(member) in user_dict:
					torn_id = user_dict[str(member)]["torn_id"]
					torn_link = "https://www.torn.com/profiles.php?XID=" + torn_id
					if torn_id in vBasicFactionMembers:
						torn_name = vBasicFactionMembers[torn_id]["name"]
						torn_status = vBasicFactionMembers[torn_id]["status"]["state"]
						#leader_name =  "[" + torn_name + "[" + torn_id + "]" + "](" + torn_link + ")"
						leader_name = torn_name + "[" + torn_id + "]"
						if extra == "e":
							current_e = await self.get_e(torn_id)
							leader_name = leader_name + " (" + current_e + ")"
						elif extra == "p":
							property = await self.get_property(torn_id)
							leader_name = leader_name + " (" + property + ")"
						elif extra == "mh":
							max_hap = await self.get_maxhappy(torn_id)
							leader_name = leader_name + " (" + max_hap + ")"
						elif extra == "mhp":
							property = await self.get_property(torn_id)
							max_hap = await self.get_maxhappy(torn_id)
							leader_name = leader_name + " (" + property + ", " + max_hap + ")"
						elif extra == "nnb":
							nnb = await self.get_nnb(torn_id)
							leader_name = leader_name + " (" + nnb + ")"
						elif extra == "cd":
							current_cd = await self.get_cd(torn_id)
							leader_name = leader_name + " (" + current_cd + ")"
						elif extra == "ecd":
							current_e = await self.get_e(torn_id)
							current_cd = await self.get_cd(torn_id)
							leader_name = leader_name + " (" + current_e + ", " + current_cd + ")"
						
					else:
						leader_name = role.members[0].display_name + " (not in faction)"
				else:
					leader_name = role.members[0].display_name + " (No ID)"

			leader = leader_name + " (***Team Leader***)" + "\n"
			
		
			#team members
			member_list = ""

			role = discord.utils.get(vguild.roles, name=team_member_role.replace("XXX", team))
			if role == None:
				member_list = member_list + " - " + team_member_role.replace("XXX", team) + " role not defined"  + "\n"
			else:

				if len(role.members) == 0:
					member_list = member_list + " - No members for this team"  + "\n"
				else:
					for member in role.members:
						if str(member.id) in user_dict:
							torn_id = user_dict[str(member.id)]["torn_id"]
							torn_link = "https://www.torn.com/profiles.php?XID=" + torn_id
							if torn_id in vBasicFactionMembers:
								torn_name = vBasicFactionMembers[torn_id]["name"]
								torn_status = vBasicFactionMembers[torn_id]["status"]["state"]
								member_list = member_list +  " - " + torn_name + "[" + torn_id + "]"
								if extra == "e":
									current_e = await self.get_e(torn_id)
									member_list = member_list + " (" + current_e + ")"
								elif extra == "p":
									property = await self.get_property(torn_id)
									member_list = member_list + " (" + property + ")"
								elif extra == "mh":
									max_hap = await self.get_maxhappy(torn_id)
									member_list = member_list + " (" + max_hap + ")"
								elif extra == "mhp":
									property = await self.get_property(torn_id)
									max_hap = await self.get_maxhappy(torn_id)
									member_list = member_list + " (" + property + ", " + max_hap + ")"
								elif extra == "nnb":
									nnb = await self.get_nnb(torn_id)
									member_list = member_list + " (" + nnb + ")"
								elif extra == "cd":
									current_cd = await self.get_cd(torn_id)
									member_list = member_list + " (" + current_cd + ")"
								elif extra == "ecd":
									current_e = await self.get_e(torn_id)
									current_cd = await self.get_cd(torn_id)
									member_list = member_list + " (" + current_e + ", " + current_cd + ")"
								#member_list = member_list + "\n"

							else:
								member_list = member_list	+ " - " + member.display_name + " (not in faction)"
						else:
							member_list = member_list	+ " - " + member.display_name + " (No ID)"

						member_list = member_list + "\n"

			field_list[team] = leader + member_list



		#faction leader

		faction_leader = "**Faction Leader**" + "\n"
		role = discord.utils.get(vguild.roles, name=faction_leader_role)
		if role == None:
			faction_leader_name = faction_leader_role + " role not defined" + "\n"
		else:

			if len(role.members) == 0:
				faction_leader_name = " - Faction leader not set" + "\n"
			else:
				member = role.members[0].id
				if str(member) in user_dict:
					torn_id = user_dict[str(member)]["torn_id"]
					torn_link = "https://www.torn.com/profiles.php?XID=" + torn_id
					if torn_id in vBasicFactionMembers:
						torn_name = vBasicFactionMembers[torn_id]["name"]
						torn_status = vBasicFactionMembers[torn_id]["status"]["state"]
						faction_leader_name = torn_name + "[" + torn_id + "]"
						if extra == "e":
							current_e = await self.get_e(torn_id)
							faction_leader_name = faction_leader_name + " (" + current_e + ")"
						elif extra == "p":
							property = await self.get_property(torn_id)
							faction_leader_name = faction_leader_name + " (" + property + ")"
						elif extra == "mh":
							max_hap = await self.get_maxhappy(torn_id)
							faction_leader_name = faction_leader_name + " (" + max_hap + ")"
						elif extra == "mhp":
							property = await self.get_property(torn_id)
							max_hap = await self.get_maxhappy(torn_id)
							faction_leader_name = faction_leader_name + " (" + property + ", " + max_hap + ")"
						elif extra == "nnb":
							nnb = await self.get_nnb(torn_id)
							faction_leader_name = faction_leader_name + " (" + nnb + ")"
						elif extra == "cd":
							current_cd = await self.get_cd(torn_id)
							faction_leader_name = faction_leader_name + " (" + current_cd + ")"
						elif extra == "ecd":
							current_e = await self.get_e(torn_id)
							current_cd = await self.get_cd(torn_id)
							faction_leader_name = faction_leader_name + " (" + current_e + ", " + current_cd + ")"
						
					else:
						faction_leader_name = role.members[0].display_name + " (not in faction)" + "\n"
				else:
					faction_leader_name = role.members[0].display_name + " (No ID)" + "\n"

		faction_leader = faction_leader + faction_leader_name + "\n"

	
		#management list 
		management_list = ""

		managers = "**Managers**" + "\n"
		role = discord.utils.get(vguild.roles, name=faction_manager_role)
		if role == None:
			management_list = management_list + faction_manager_role + " role not defined" + "\n"
		else:

			if len(role.members) == 0:
				management_list = management_list + " - No managers set" + "\n"
			else:
				for member in role.members:
					if str(member.id) in user_dict:
						torn_id = user_dict[str(member.id)]["torn_id"]
						torn_link = "https://www.torn.com/profiles.php?XID=" + torn_id
						if torn_id in vBasicFactionMembers:
							torn_name = vBasicFactionMembers[torn_id]["name"]
							torn_status = vBasicFactionMembers[torn_id]["status"]["state"]
							management_list = management_list + torn_name + "[" + torn_id + "]"
							if extra == "e":
								current_e = await self.get_e(torn_id)
								management_list = management_list + " (" + current_e + ")"
							elif extra == "p":
								property = await self.get_property(torn_id)
								management_list = management_list + " (" + property + ")"
							elif extra == "mh":
								max_hap = await self.get_maxhappy(torn_id)
								management_list = management_list + " (" + max_hap + ")"
							elif extra == "mhp":
								property = await self.get_property(torn_id)
								max_hap = await self.get_maxhappy(torn_id)
								management_list = management_list + " (" + property + ", " + max_hap + ")"
							elif extra == "nnb":
								nnb = await self.get_nnb(torn_id)
								management_list = management_list + " (" + nnb + ")"
							elif extra == "cd":
								current_cd = await self.get_cd(torn_id)
								management_list = management_list + " (" + current_cd + ")"
							elif extra == "ecd":
								current_e = await self.get_e(torn_id)
								current_cd = await self.get_cd(torn_id)
								management_list = management_list + " (" + current_e + ", " + current_cd + ")"
							management_list = management_list + "\n"
						else:
							management_list = management_list	+ member.display_name + " (not in faction)" + "\n"
					else:
						management_list = management_list	+ member.display_name + " (No ID)" + "\n"

			managers = managers + management_list + "\n"


		#build embed
		emded_desc = faction_leader + "\n" + managers
		for field in field_list:
			emded_desc = emded_desc + "***[" + field + " Team" + "]***" + "\n"
			emded_desc = emded_desc + field_list[field] + "\n"
		

		title_text = "Hello High Teams"
		if extra == "e":
			title_text = title_text + " (With energy levels)"
		elif extra == "p":
			title_text = title_text + " (With property)"
		elif extra == "mh":
			title_text = title_text + " (With max happy)"
		elif extra == "mhp":
			title_text = title_text + " (With property and max happy)"
		elif extra == "nnb":
			title_text = title_text + " (With natural nerve)"
		elif extra == "cd":
			title_text = title_text + " (With drug cooldowns)"
		elif extra == "ecd":
			title_text = title_text + " (With energy and drug cd)"

		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		embed.set_footer(text="Option: " + extra)
		return embed
	



	@commands.command(name='bankers', aliases = ["banker"], help='Provide a list of members with the banking role')
	async def bankers(self, ctx):
		
		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				user_dict = json.load(inf)
				#print("file found")
		else:
			raise __main__.NoFile("users.json")

		role = discord.utils.get(ctx.message.guild.roles, name="HelloHigh Banking")
		
		hhBankers = {}
		for member in role.members:
			hhBankers[str(member.id)] = {"discord_name": member.display_name,"discord_status": str(member.status), "torn_status":"TBC"}

		if len(hhBankers) == 0:
			await ctx.send("No members currently have banking privilage.")
			return

		vBasicFactionMembers = await self.basicFactionMembers()
		if vBasicFactionMembers == "ERROR":
			await ctx.send("An error")
			return



		emded_desc = ""

		emded_desc = "**Banking role**" + "\n"
		for member in hhBankers:
			
			if member in user_dict:
				torn_id = user_dict[member]["torn_id"]
				torn_link = "https://www.torn.com/profiles.php?XID=" + torn_id
				discord_status = hhBankers[member]["discord_status"]			
				if torn_id in vBasicFactionMembers:
					torn_name = vBasicFactionMembers[torn_id]["name"]
					torn_status = vBasicFactionMembers[torn_id]["status"]["state"]
					emded_desc = emded_desc +  "[" + torn_name + "[" + torn_id + "]" + "](" + torn_link + ")" + " - Discord status: " + discord_status + " - Torn Status: " + torn_status + "\n"
				else:
					emded_desc = emded_desc	+ hhBankers[member]["discord_name"] + " (user not in the faction - remove role)" + "\n"
			else:
				emded_desc = emded_desc	+ hhBankers[member]["discord_name"] + " (user needs to !add_id)" + "\n"

			
		embed = discord.Embed(title=":bank: Hello High", 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/tab=armoury",
		description = emded_desc)
								
		await ctx.send(embed=embed)
	
		return


	@commands.command(name='flying', aliases = ["fly", "flyers", "flyer"], help='Provide list of travelling members (aliases: !fly,  !flyers, !flyer)')
	async def flying(self, ctx):
	
		vBasicFactionMembers = await self.basicFactionMembers()
		

		flyers = {}
		for member in vBasicFactionMembers:

			if vBasicFactionMembers[member]["status"]["state"] == "Traveling":
				flyers[member] = {"name": vBasicFactionMembers[member]["name"],
									"state": vBasicFactionMembers[member]["status"]["state"],
									"description" : vBasicFactionMembers[member]["status"]["description"]
									}
		

		if len(flyers) > 0:
			emded_desc = "**Flying Members**" + "\n"
			for member in flyers:
				emded_desc = emded_desc +  "[" + flyers[member]["name"] + "[" + member + "]" + "](https://www.torn.com/profiles.php?XID=" + member + ")    " + flyers[member]["description"]
				
				try:
					dummy = await __main__.eta_work(member)
				
					if type(dummy) == discord.embeds.Embed:
						eta_text = dummy.fields[len(dummy.fields)-1].value
						eta_text_short = eta_text[eta_text.find("(")+1:eta_text.find(")")].replace(" Hour", "h").replace(" Minutes","m")
						#print(string[string.find("(")+1:string.find(")")])
						emded_desc = emded_desc + " - ETA " + eta_text_short
				except:
					pass

				emded_desc = emded_desc + "\n"
			embed = discord.Embed(title=":airplane: Hello High", 
			colour=discord.Colour(0x5dd3fa), 
			url="https://www.torn.com/factions.php?step=your#/",
			description = emded_desc)
									
			await ctx.send(embed=embed)
	
		else:
			await ctx.send("No members are currently flying.")
		return



	@commands.command(name='allthesingleladies', aliases = ["single", "singles"], help='Provide list of single members (aliases: !fly,  !flyers, !flyer)')
	async def allthesingleladies(self, ctx):
	

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				user_dict = json.load(inf)
				#print("file found")
		else:
			raise __main__.NoFile("users.json")

		vBasicFactionMembers = await self.basicFactionMembers()
		singlelist = {}


		emded_desc = ""

		#print(vBasicFactionMembers)
		for torn_id in vBasicFactionMembers:
			if await self.get_married(torn_id) == "False":
				singlelist[torn_id] = vBasicFactionMembers[torn_id]["name"]

		
#		print(singlelist)
		sortlist = sorted(singlelist.items(), key=lambda x:x[1].lower())
		sortlist = dict(sortlist)
		
#		print(sortlist)

		for member in sortlist:
			emded_desc = emded_desc + sortlist[member] + " [" + str(member) + "]" + "\n"

	
		title_text = "'A'll the 'S'ingle 'L'adies"
		embed = discord.Embed(title=title_text, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/factions.php?step=your#/",
		description = emded_desc)
		
		embed.set_thumbnail(url="https://factionimages.torn.com/52171c9a-7608-8e67-2344388.jpg")
		await ctx.send(embed=embed)
		return



	async def basicFactionMembers(self):
	
		vBasicFaction = await self.basicFaction()
		members = vBasicFaction["members"]
		return members




	async def basicFaction(self):
	

		v_apiType = "faction"
		v_apiSelection = "basic"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		
		if "error" in v1:
			raise __main__.APICallError("basicFaction")

		return v1



def setup(bot):
	bot.add_cog(Faction(bot))