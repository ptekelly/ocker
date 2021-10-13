import discord
import typing
import os
import requests
import __main__
import json

from datetime import datetime
from datetime import timedelta

from dateutil.relativedelta import relativedelta


from discord.ext import commands


class Profile_cog(commands.Cog):

	def __init__(self,bot):
		self.bot = bot
		self.xclickuser = None
		self.xclickcount = 0

	@commands.Cog.listener()
	async def on_ready(self):
		print('Profile COG Ready')



	@commands.Cog.listener()
	async def on_reaction_add(self,reaction, user):
		if user.bot:
			return
		msg = reaction.message
		if len(msg.embeds) == 0:
			return

		if reaction.emoji != "\U0001f1fd":
			return

		if user == self.xclickuser:
			self.xclickcount = self.xclickcount + 1
		else:
			self.xclickcount = 0
			self.xclickuser = user

		#print(self.xclickuser)
		#print(self.xclickcount)

		await reaction.remove(user)

		emojis = {'\U0001f1fd':"x"}
		
		myTitle = msg.embeds[0].title
		torn_id = myTitle.split('[')[1].split(']')[0]
		
		if msg.embeds[0].fields[len(msg.embeds[0].fields)-1].name == "STOP IT!!!!":
			LinkField = msg.embeds[0].fields[len(msg.embeds[0].fields)-2]
		else:		
			LinkField = msg.embeds[0].fields[len(msg.embeds[0].fields)-1]
		
		
		if "Drugs" == msg.embeds[0].fields[0].name:
			msg.embeds[0].clear_fields()
		
			field_list = await self.profile_main_fields(torn_id)

			for field in field_list:

				msg.embeds[0].add_field(name=field, value=field_list[field])	
				
		else:
			msg.embeds[0].clear_fields()
	
			field_list = await self.profile_secondary_fields(torn_id)

			for field in field_list:

				msg.embeds[0].add_field(name=field, value=field_list[field])	
			
		msg.embeds[0].add_field(name=LinkField.name, value=LinkField.value, inline = LinkField.inline)



		if msg.embeds[0].fields[len(msg.embeds[0].fields) - 1].name == "STOP IT!!!!":
			#print("remvoe field")
			msg.embeds[0].remove_field(len(msg.embeds[0].fields) - 1)

		
		if self.xclickcount > 10:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="OK " + self.xclickuser.name + " you are too good for me, I give up", inline = False)
			#print("add field > 10")

			emojis = {'\U0001f1fd':"x"}

		elif self.xclickcount > 9:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="HAHAHAHAHAHA", inline = False)
			#print("add field > 9")

			emojis = {'\U0001f1eb':"f",
						'\U0001f1fa':"u",
						'\U0001f1e8':"c",
						'\U0001f1f0':"k",
						'\U0001f1ea':"e",
						'\U0001f1e9':"d",
						'\U0001f1f3':"n",
						'\U0001f1f4':"o",
						'\U0001f1fc':"w",
						}

		
		elif self.xclickcount > 8:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="OK " + self.xclickuser.name + " what you gonna do now!!!!", inline = False)
			#print("add field > 8")

			emojis = {'\U0001f1fe':"y",
						'\U0001f1e8':"c",
						'\U0001f1fc':"w",
						'\U0001f1e6':"a",
						'\U0001f1f4':"o",
						'\U0001f1f8':"s",
						'\U0001f1f7':"r",
						'\U0001f1f6':"q",
						'\U0001f1f5':"p",
						'\U0001f1fd':"x",
						'\U0001f1f3':"n",
						'\U0001f1f2':"m",
						'\U0001f1f1':"l",
						'\U0001f1ef':"j",
						'\U0001f1ff':"z",
						'\U0001f1ee':"i",
						'\U0001f1ec':"g",
						'\U0001f1eb':"f",
						'\U0001f1fb':"v"}

			
		
		elif self.xclickcount > 7:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="Right " + self.xclickuser.name + " last warning!!!!", inline = False)
			#print("add field > 7")
		elif self.xclickcount > 5:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="I mean it " + self.xclickuser.name + " leave it alone!!!!", inline = False)
			#print("add field > 5")
		elif self.xclickcount > 2:
			msg.embeds[0].add_field(name="STOP IT!!!!", value="I know it was you " + self.xclickuser.name + "!!!!", inline = False)
			#print("add field > 2")

		embed  = msg.embeds[0]
		await msg.edit(embed=embed)
		
		if self.xclickcount > 8:
			await msg.clear_reactions()
			for emoji in emojis:
				await msg.add_reaction(emoji)
		if self.xclickcount > 10:
			self.xclickcount = 0
		
		return



	@commands.command(name='trade', help='Trade link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def trade(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "trade")
		await ctx.send(embed=embed)


	@commands.command(name='display', help='Display link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def display(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			torn_id = await __main__.get_user_data(member,"torn_id")
			#torn_id = __main__.getid(member)

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "display")
		await ctx.send(embed=embed)


	@commands.command(name='bazaar', help='Bazaar link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def bazaar(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "bazaar")
		await ctx.send(embed=embed)


	@commands.command(name='cash', help='Cash link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def cash(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "cash")
		await ctx.send(embed=embed)


	@commands.command(name='bounty', help='Bounty link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def bounty(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "bounty")
		await ctx.send(embed=embed)


	@commands.command(name='attack', help='Attack link: No parameter is your own link, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def attack(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")

		elif type(member) == int:
			torn_id = str(member)
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return

		embed = await self.user_link(torn_id, "attack")
		await ctx.send(embed=embed)


	async def user_link(self, torn_id, link_type):
		v_apiType = "user"
		v_apiSelection = "profile"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			await ctx.send(response)
			return
		else:
			name = v1['name']
			id = v1['player_id']
			role = v1['role']
			level = "Level " + str(v1['level'])
			rank = v1['rank']
			age = v1['age']
			gender = v1['gender']
			last_action = v1['last_action']
			last_online = last_action['relative']


		trade_title   = "Trade link for " + name + "[" + str(torn_id) + "]"
		display_title = "Display Case link for " + name + "[" + str(torn_id) + "]"
		bazaar_title  = "Bazaar link for " + name + "[" + str(torn_id) + "]"
		cash_title    = "Send cash link for " + name + "[" + str(torn_id) + "]"
		bounty_title  = "Bounty link for " + name + "[" + str(torn_id) + "]"
		attack_title  = "Attack link for " + name + "[" + str(torn_id) + "]"

		trade_link   = "https://www.torn.com/trade.php#step=start&userID=" + torn_id
		display_link = "https://www.torn.com/displaycase.php#display/" + torn_id
		bazaar_link  = "https://www.torn.com/bazaar.php?userId=" + torn_id +"#/"
		cash_link    = "https://www.torn.com/sendcash.php#/XID=" + torn_id
		bounty_link  = "https://www.torn.com/bounties.php?p=add&XID=" + torn_id
		attack_link  = "https://www.torn.com/loader2.php?sid=getInAttack&user2ID=" + torn_id
		

		if link_type == "trade":
			title = trade_title
			url = trade_link
		
		elif link_type == "display":
			title = display_title
			url = display_link

		elif link_type == "bazaar":
			title = bazaar_title
			url = bazaar_link

		elif link_type == "cash":
			title = cash_title
			url = cash_link

		elif link_type == "bounty":
			title = bounty_title
			url = bounty_link

		elif link_type == "attack":
			title = attack_title
			url = attack_link

		else:
			return "I am not sure what you want.  Try trade, display, bazaar, cash, bounty or attack"

		embed = discord.Embed(title=title, 
			colour=discord.Colour(0x5dd3fa), 
			url=url)
		return embed


	async def get_bars(self,torn_id):

		torn_api = await __main__.get_user_data_from_id(torn_id,"torn_api")
		#v_apiKey = await __main__.get_user_data(member,"torn_api")

		v_apiType = "user"

		v_apiSelection = "bars"
	
		
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise __main__.APIIssue("bars")
			return
		else:
			return v1

		return


	async def get_crimes(self,torn_id):

		torn_api = await __main__.get_user_data_from_id(torn_id,"torn_api")
		#v_apiKey = await __main__.get_user_data(member,"torn_api")

		v_apiType = "user"

		v_apiSelection = "crimes"
	
		
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise __main__.APIIssue("crimes")
			return
		else:
			return v1["criminalrecord"]

		return

	@commands.command(name='vitals', aliases = ["v", "vit", "vital"], help='Torn user timers etc. Requires Torn ID and Torn API registed with the bot')
	async def vitals(self, ctx, member: typing.Union[discord.Member,str] = "NA"):
		
		
		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")
		
			
		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameter is discord name (e.g. @Accy)")
			return

		#v_apiKey = await __main__.get_user_data_from_id(torn_id,"torn_api")
		torn_api = await __main__.get_user_data(member,"torn_api")
		

		v_apiType = "user"

		v_apiSelection = "bars"
	
		
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise __main__.APIIssue("vitals")
		else:
			happy = v1['happy']
			happy_current = happy['current']
			happy_max = happy['maximum']
			happy_full = happy['fulltime']

			life = v1['life']
			life_current = life['current']
			life_max = life['maximum']
			life_full = life['fulltime']

			energy = v1['energy']
			energy_current = energy['current']
			energy_max = energy['maximum']
			energy_full = energy['fulltime']

			nerve = v1['nerve']
			nerve_current = nerve['current']
			nerve_max = nerve['maximum']
			nerve_full = nerve['fulltime']
		


		v_apiSelection = "cooldowns"
	

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			await ctx.send(response)
			return
		

		cooldowns = v1['cooldowns']
		drug_cd = cooldowns['drug']
		medical_cd = cooldowns['medical']
		booster_cd = cooldowns['booster']

	

		v_apiSelection = "education"
	

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			await ctx.send(response)
			return
		else:
			edu_cd = v1['education_timeleft']
			
	
		v_apiSelection = "basic"
	

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			await ctx.send(response)
			return
		else:
			torn_name = v1['name']
			
		title = "Vitals for " + torn_name + "[" + str(torn_id) + "]"

		desc_value = ""

		desc_value = desc_value + "**Life**"
		desc_value = desc_value + "\n" + str(life_current) + "/" + str(life_max)

		if life_full > 0:

			xseconds = life_full
			xdays = divmod(xseconds, (60*60*24))[0]
			xdaysr = divmod(xseconds, (60*60*24))[1]
			xhours = divmod(xdaysr, (60*60))[0]
			xhoursr = divmod(xdaysr, (60*60))[1]
			xmins = divmod(xhoursr, (60))[0]
			xhoursr = divmod(xhours, (60))[1]
			
			life_full_text = "\nFull in "
			if xdays > 0:
				life_full_text = life_full_text + str(xdays) + "d "
			if xhours > 0:
				life_full_text = life_full_text + str(xhours) + "h "
			if xmins > 0:
				life_full_text = life_full_text + str(xmins) + "m "
			
			if (xdays + xhours + xmins) > 0:
				desc_value = desc_value + life_full_text



		desc_value = desc_value + "\n" + "**Energy**"
		desc_value = desc_value + "\n" + str(energy_current) + "/" + str(energy_max)

		if energy_full > 0:

			xseconds = energy_full
			xdays = divmod(xseconds, (60*60*24))[0]
			xdaysr = divmod(xseconds, (60*60*24))[1]
			xhours = divmod(xdaysr, (60*60))[0]
			xhoursr = divmod(xdaysr, (60*60))[1]
			xmins = divmod(xhoursr, (60))[0]
			xhoursr = divmod(xhours, (60))[1]
			
			energy_full_text = "\nFull in "
			if xdays > 0:
				energy_full_text = energy_full_text + str(xdays) + "d "
			if xhours > 0:
				energy_full_text = energy_full_text + str(xhours) + "h "
			if xmins > 0:
				energy_full_text = energy_full_text + str(xmins) + "m "

			if (xdays + xhours + xmins) > 0:
				desc_value = desc_value + energy_full_text


		desc_value = desc_value + "\n" + "**Happiness**"
		desc_value = desc_value + "\n" + str(happy_current) + "/" + str(happy_max)

		if happy_full > 0:
			xseconds = happy_full
			xdays = divmod(xseconds, (60*60*24))[0]
			xdaysr = divmod(xseconds, (60*60*24))[1]
			xhours = divmod(xdaysr, (60*60))[0]
			xhoursr = divmod(xdaysr, (60*60))[1]
			xmins = divmod(xhoursr, (60))[0]
			xhoursr = divmod(xhours, (60))[1]
			
			happy_full_text = "\nFull in "
			if xdays > 0:
				happy_full_text = happy_full_text + str(xdays) + "d "
			if xhours > 0:
				happy_full_text = happy_full_text + str(xhours) + "h "
			if xmins > 0:
				happy_full_text = happy_full_text + str(xmins) + "m "
		
			if (xdays + xhours + xmins) > 0:
				desc_value = desc_value + happy_full_text


		desc_value = desc_value + "\n" + "**Nerve**"
		desc_value = desc_value + "\n" + str(nerve_current) + "/" + str(nerve_max)

		if nerve_full > 0:
			xseconds = nerve_full
			xdays = divmod(xseconds, (60*60*24))[0]
			xdaysr = divmod(xseconds, (60*60*24))[1]
			xhours = divmod(xdaysr, (60*60))[0]
			xhoursr = divmod(xdaysr, (60*60))[1]
			xmins = divmod(xhoursr, (60))[0]
			xhoursr = divmod(xhours, (60))[1]
			
			nerve_full_text = "\nFull in "
			if xdays > 0:
				nerve_full_text = nerve_full_text + str(xdays) + "d "
			if xhours > 0:
				nerve_full_text = nerve_full_text + str(xhours) + "h "
			if xmins > 0:
				nerve_full_text = nerve_full_text + str(xmins) + "m "
	
			if (xdays + xhours + xmins) > 0:
				desc_value = desc_value + nerve_full_text


		desc_value = desc_value + "\n" + "**Medical Cooldown**"

		cd_text = ""

		if medical_cd > 0:
			xseconds = medical_cd
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
				cd_text = "None"
		else:
			cd_text = "None"

		desc_value = desc_value + "\n" + cd_text



		desc_value = desc_value + "\n" + "**Drug Cooldown**"

		cd_text = ""

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
				cd_text = "None"
		else:
			cd_text = "None"

		desc_value = desc_value + "\n" + cd_text



		desc_value = desc_value + "\n" + "**Booster Cooldown**"

		cd_text = ""

		if booster_cd > 0:
			xseconds = booster_cd
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
				cd_text = "None"
		else:
			cd_text = "None"

		desc_value = desc_value + "\n" + cd_text



		desc_value = desc_value + "\n" + "**Education Cooldown**"

		cd_text = ""

		if edu_cd > 0:
			xseconds = edu_cd
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
				cd_text = "None"
		else:
			cd_text = "None"

		desc_value = desc_value + "\n" + cd_text


		embed = discord.Embed(title=title, 
			colour=discord.Colour(0x5dd3fa), 
			url="https://www.torn.com/profiles.php?XID="+str(torn_id), 
			description= desc_value)

		msg = await ctx.send(embed=embed)


		return





	@commands.command(name='profile', aliases = ["torn", "prof", "p"], help='Torn profile: No parameter is your own profile, user name e.g. @accy (both require Torn ID registering with BOT) or any Torn ID')
	async def profile(self, ctx, member: typing.Union[discord.Member,int,str] = "NA"):
		
		

		if member == "NA":
			member = ctx.author
		
		if type(member) == discord.Member:
			#await ctx.send("Member")
			
			#torn_id = __main__.getid(member)
			torn_id = await __main__.get_user_data(member,"torn_id")
			#await ctx.send("torn_id: " + torn_id)
			if torn_id == "ERROR: id not found":
				await ctx.send("Please use !addid <yourtornid> to add your ID to the bot")
				return
			if torn_id == "ERROR: File Not found":
				await ctx.send("There was a problem with the File - tell someone, anyone, I don't know....")
				return

			member_url = member.avatar_url
			

		elif type(member) == int:
			#await ctx.send("user id")
			torn_id = str(member)
			#await ctx.send("torn_id: " + torn_id)
			discord_id = await __main__.get_user_data_from_id(torn_id,"disco_id")

			if "ERROR" in discord_id:
				member_url = "https://cdn.discordapp.com/embed/avatars/0.png"
			else:	
				user = await self.fetch_user(discord_id)	
				member_url = user.avatar_url

		elif type(member) == str:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or torn id (e.g. 2586638)")
			return


		embed = await self.profile_work(torn_id,member_url)
		msg = await ctx.send(embed=embed)

		emoji = '\U0001f1fd'
		await msg.add_reaction(emoji)

		return



	



	async def profile_work(self, torn_id,member_url):

		v_apiSelection = "profile"
		v_apiType = "user"


		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise __main__.APICallError("There is an issue with the API call")
		else:
			name = v1['name']
			id = v1['player_id']
			role = v1['role']
			level = "Level " + str(v1['level'])
			rank = v1['rank']
			age = v1['age']
			gender = v1['gender']
			last_action = v1['last_action']
			last_online = last_action['relative']

			male_icon = ':mens:'
			female_icon = ':womens:'

			if gender == 'Male':
				gender_icon = male_icon
			else:
				gender_icon = female_icon

			#days = 429
			seconds = age * 24 * 60 * 60
			nowdate = datetime.now()

			nowtimestamp = datetime.timestamp(nowdate)

			starttimestamp = nowtimestamp - seconds
			startdate = datetime.fromtimestamp(starttimestamp)

			datediff = relativedelta(nowdate, startdate)
			yearsdiff = datediff.years
			monthsdiff = datediff.months
			daysdiff = datediff.days

			textplayedsince = ""

			if yearsdiff > 0:
				textplayedsince = textplayedsince + str(yearsdiff) + " years "
			if monthsdiff > 0:
				textplayedsince = textplayedsince + str(monthsdiff) + " months "
			if daysdiff > 0:
				textplayedsince = textplayedsince + str(daysdiff) + " days "

			textplayedsince = textplayedsince + "old."


			quick_links = ""
			trade_link   = "[Trade](https://www.torn.com/trade.php#step=start&userID=" + torn_id +")"
			display_link = "[Display Cabinet](https://www.torn.com/displaycase.php#display/" + torn_id +")"
			bazaar_link  = "[Bazaar](https://www.torn.com/bazaar.php?userId=" + torn_id +"#/)"
			cash_link    = "[Send cash](https://www.torn.com/sendcash.php#/XID=" + torn_id +")"
			bounty_link  = "[Bounty](https://www.torn.com/bounties.php?p=add&XID=" + torn_id +")"
			attack_link  = "[Attack](https://www.torn.com/loader2.php?sid=getInAttack&user2ID=" + torn_id +")"
			
			quick_name = "Links"
			quick_links = quick_links + trade_link
			quick_links = quick_links + " | "
			quick_links = quick_links + display_link
			quick_links = quick_links + " | "
			quick_links = quick_links + bazaar_link
			quick_links = quick_links + " | "
			quick_links = quick_links + cash_link
			quick_links = quick_links + " | "
			quick_links = quick_links + bounty_link
			quick_links = quick_links + " | "
			quick_links = quick_links + attack_link
			quick_value = quick_links


			desc_value = role + " - " + str(level) + ", " + rank + "\n" + textplayedsince + "\n" + "Last online " + last_online

			embed = discord.Embed(title="Profile for " + name + "[" + str(id) + "] " + gender_icon, 
				colour=discord.Colour(0x5dd3fa), 
				url="https://www.torn.com/profiles.php?XID="+str(torn_id), 
				description= desc_value)
			
			embed.set_thumbnail(url=member_url)

			field_list = await self.profile_main_fields(torn_id)
			
			for field in field_list:
				embed.add_field(name=field, value = field_list[field])

			embed.add_field(name=quick_name, value=quick_value, inline = False)

			return embed


	async def profile_main_fields(self, torn_id):

		field_list = {}

		v_apiSelection = "profile"
		v_apiType = "user"


		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			await ctx.send(response)
			return
		else:
			life = v1['life']
			life_hp = life['current']
			life_max_hp = life['maximum']
			status = v1['status']
			description = status['description']
			details = status['details']
			state = status['state']
			job = v1['job']
			job_position = job['position']
			company_id = job['company_id']
			company_name = job['company_name']
			faction = v1['faction']
			faction_position = faction['position']
			faction_id = faction['faction_id']
			faction_name = faction['faction_name']
			days_in_faction = faction['days_in_faction']
			married = v1['married']
			spouse_id = married['spouse_id']
			spouse_name = married['spouse_name']
			married_days = married['duration']
			property_id = v1['property_id']
			property_type = v1['property']
			awards = v1['awards']
			friends = v1['friends']
			enemies = v1['enemies']
			forum_posts = v1['forum_posts']
			karma = v1['karma']
			if "ERROR" in str(self.get_personal_stat(torn_id, "networth")):
				networth = "Error"
			else:
				networth = "$" + str("{:,.0f}".format((self.get_personal_stat(torn_id, "networth")/1000000))) + "m"

			male_icon = ':mens:'
			female_icon = ':womens:'
			heart_icon = ':blue_heart:'
			employ_icon = ':construction_worker:'
			faction_icon = ':crossed_swords:'

			jail_icon = ":woman_police_officer:"
			hospital_icon = ":hospital:"
			travel_icon = ":airplane:"
			okay_icon = ":white_check_mark:"

			married_icon = ':heart:'
			property_icon = ':Property:'
			stats_icon = ':bar_chart:'
			forum_icon = ':speech_balloon:'


			

			job_name = employ_icon + " Employment"
			if company_id == 0:
				job_value = "Working for the " + job_position 
			else:
				job_value = job_position + " at [" + company_name + "](https://www.torn.com/joblist.php#/p=corpinfo&ID=" + str(company_id) + ")"

			faction_field_name = faction_icon + " Faction"
			if faction_id == 0:
				faction_value = "Why you no in a faction?"
			else:
				faction_value = faction_position + " of [" + faction_name + "](https://www.torn.com/factions.php?step=profile&ID=" + str(faction_id) + "#/)"
			
			married_name = married_icon + " Marriage"
			if spouse_id == 0:
				married_value = "Single and ready to mingle"
			else:
				married_value = "Married to [" + spouse_name + "](https://www.torn.com/profiles.php?XID=" + str(spouse_id) + ") for " + str(married_days) + " days" 

			married_value = married_value  + "\n" + "**Property:** [" + property_type + "](https://www.torn.com/properties.php#/p=propertyinfo&ID=" + str(property_id) + "&userID=" + str(torn_id) + ")"



			if state == "Traveling":
				status_icon = travel_icon
			elif state == "Hospital":
				status_icon = hospital_icon
			elif state == "Jail":
				status_icon = jail_icon
			else:
				status_icon = okay_icon

			status_name = heart_icon + " Status " + str(life_hp) + "/" + str(life_max_hp)
			status_value = status_icon + " " + description

			stats_name = stats_icon + " Social Statistics"
			stats_value = "**Networth:** " + networth + "\n" + "**Awards:** " + str(awards) + "\n" + "**Friends:** " + str(friends) + "\n" + "**Enemies:** " + str(enemies) + "\n" + "[Other Statistics](https://www.torn.com/personalstats.php?ID=" + str(torn_id) + ")"

			forum_name = forum_icon + " Forum Statistics"
			forum_value = "**Forum Posts:** " + str(forum_posts) + "\n" + "**Karma:** " + str(karma)

			field_list[status_name] = status_value
			field_list[job_name] = job_value
			field_list[faction_field_name] = faction_value
			field_list[married_name] = married_value
			field_list[stats_name] = stats_value
			field_list[forum_name] = forum_value
			
			return field_list


	async def profile_secondary_fields(self,torn_id):

		field_list = {}

		pstats = await self.get_personal_stats_from_id(torn_id)
		
		drugsFieldValue = ""
		drugsFieldValue = drugsFieldValue + "Drugs used: " + str(pstats["drugsused"]) + "\n"
		drugsFieldValue = drugsFieldValue + "Times overdosed: " + str(pstats["overdosed"]) + "\n"
		drugsFieldValue = drugsFieldValue + "Rehabilitations: " + str(pstats["rehabs"]) + "\n"
		drugsFieldValue = drugsFieldValue + "Rehabilitation fees: $" + str("{:,.0f}".format(pstats["rehabcost"])) + "\n"
		drugsFieldValue = drugsFieldValue + "Cannabis: " + str(pstats["cantaken"]) + "\n"
		drugsFieldValue = drugsFieldValue + "Ecstasy: " + str(pstats["exttaken"]) + "\n"
		drugsFieldValue = drugsFieldValue + "Ketamine: " + str(pstats["kettaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "LSD: " + str(pstats["lsdtaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "Opium: " + str(pstats["opitaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "PCP: " + str(pstats["pcptaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "Shrooms: " + str(pstats["shrtaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "Speed: " + str(pstats["spetaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "Vicodin: " + str(pstats["victaken"]) + "\n"	 
		drugsFieldValue = drugsFieldValue + "Xanax: " + str(pstats["xantaken"]) + "\n"	 

		field_list["Drugs"] = drugsFieldValue



		bars_data = await self.get_bars(torn_id)

		crimeFieldValue = ""
		crimeFieldValue = crimeFieldValue + "Natural Nerve: " + str(bars_data["nerve"]["maximum"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Current Nerve: " + str(bars_data["nerve"]["current"]) + "\n"

		crime_data = await self.get_crimes(torn_id)

		crimeFieldValue = crimeFieldValue + "\n" + "**Crimes**" + "\n"
		
		crimeFieldValue = crimeFieldValue + "Selling Illegal Products: " + str(crime_data["selling_illegal_products"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Theft: " + str(crime_data["theft"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Auto Theft: " + str(crime_data["auto_theft"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Drug Deals: " + str(crime_data["drug_deals"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Computer Crimes: " + str(crime_data["computer_crimes"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Murder: " + str(crime_data["murder"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Fraud: " + str(crime_data["fraud_crimes"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Other: " + str(crime_data["other"]) + "\n"
		crimeFieldValue = crimeFieldValue + "Total: " + str(crime_data["total"]) + "\n"

		field_list["Nerve"] = crimeFieldValue


		return field_list


	async def get_personal_stats_from_id(self,torn_id):
		v_apiSelection = "personalstats"
		v_apiType = "user"

		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			response = v1["error"]["error"] 
			return(response)
		else:
			return(v1["personalstats"])



	def get_personal_stat(self,torn_id = 0, stat="NA"):
		
		if torn_id == 0:
			return "ERROR:NO_ID"
		elif stat == "NA":
			return "ERROR:NO_STAT"


		ret_text = ""
		v_apiSelection = "personalstats"
		v_apiType = "user"
		APIURL = self.bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+self.bot.v_apiKey
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			return "ERROR:SOMEERR" 
			
		selection = v1["personalstats"]
		return selection[stat]




def setup(bot):
	bot.add_cog(Profile_cog(bot))