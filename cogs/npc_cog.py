import discord
from discord.ext import commands
import requests
import os
import os.path
import json
import __main__

from datetime import datetime
from datetime import timedelta

class Npc_cog(commands.Cog):

	def __init__(self,bot):
		self.bot = bot


#	bot = commands.Bot(command_prefix='!', case_insensitive=True)

	#emojis = ['D','L','J','F','T'] - list of npcs
	emojis = {'\U0001f1e9':"duke",'\U0001f1f1':"leslie",'\U0001f1ef':"jimmy",'\U0001f1eb':"fernando",'\U0001f1f9':"tiny"}


	@commands.Cog.listener()
	async def on_reaction_add(self,reaction, user):
		if user.bot:
			return
		msg = reaction.message
		if len(msg.embeds) == 0:
			return
		
		if reaction.emoji in self.emojis:

			if reaction.message.embeds[0].title == "Current NPC Status":
				
				await reaction.remove(user)
				embed = await self.npc_detail(self.emojis[str(reaction)])
				msg = await reaction.message.channel.send(embed=embed)

		return

	

	@commands.Cog.listener()
	async def on_ready(self):
		print('NPC COG Ready')

	@commands.command(name='duke', help='Duke ready time')
	async def duke(self,ctx):

		embed = await self.npc_detail("duke")
		msg = await ctx.send(embed=embed)
		
		return

	@commands.command(name='leslie', help='Leslie ready time')
	async def leslie(self, ctx):

		embed = await self.npc_detail("leslie")
		msg = await ctx.send(embed=embed)
		
		return

	@commands.command(name='jimmy', help='Jimmy ready time')
	async def jimmy(self, ctx):

		embed = await self.npc_detail("jimmy")
		msg = await ctx.send(embed=embed)

		return

	@commands.command(name='fernando', help='Fernando ready time')
	async def fernando(self, ctx):

		embed = await self.npc_detail("fernando")
		msg = await ctx.send(embed=embed)

		return

	@commands.command(name='tiny', help='Tiny ready time')
	async def tiny(self, ctx):

		embed = await self.npc_detail("tiny")
		msg = await ctx.send(embed=embed)
		return

	@commands.command(name='scrooge', help='Scrooge ready time')
	async def scrooge(self, ctx):

		embed = await self.npc_detail("scrooge")
		msg = await ctx.send(embed=embed)
		return

	@commands.command(name='easter', help='Easter Bunny ready time')
	async def easter(self, ctx):

		embed = await self.npc_detail("easter bunny")
		msg = await ctx.send(embed=embed)

		return

	@commands.command(name='bunny', help='Easter Bunny ready time')
	async def bunny(self, ctx):

		embed = await self.npc_detail("easter bunny")
		msg = await ctx.send(embed=embed)

		return




	@commands.command(name='npc', help='NPC ready time')
	async def npc(self, ctx, *, npc_name="list"):

		if npc_name.lower() == "list":
			embed = await self.npc_list()
			msg = await ctx.send(embed=embed)
				
			for emoji in self.emojis:
				await msg.add_reaction(emoji)

		else:
			embed = await self.npc_detail(npc_name)
			msg = await ctx.send(embed=embed)


		return



	async def npc_detail(self,npc_name):

		if npc_name.lower() == "easter" or npc_name.lower() == "bunny":
			npc_name = "easter bunny"
		red_colour = discord.Colour(0xe74c3c)
		blue_colour = discord.Colour(0x5dd3fa)
		green_colour = discord.Colour(0x2ecc71)

		npc_embed_colour = green_colour
		
		APIURL = "https://yata.yt/api/v1/loot/"
	#	response = APIURL
	#	await ctx.send(response)


		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		data = r.json() # translates that response into a dict variable
		npc_hosp = data["hosp_out"]

		#await ctx.send("hospital out information: ")
		#await ctx.send(npc_hosp)



		if os.path.isfile("./shared/npc_details.json") == False:
			# File doesnt exist
			raise __main__.NoFile("npc_details.json")

		with open("./shared/npc_details.json","r") as inf:		
			npc_dict = json.load(inf)


		for npc in npc_dict:
			if npc_dict[npc]["name"].lower() == npc_name.lower():

				if npc_dict[npc]["active"] == "no":

					npc_url = npc_dict[npc]["img_url"]

					description_text = ""

					description_text = description_text + "This NPC is not currently active. "

					if npc_dict[npc]["seasonal"] != "no":
						description_text = description_text + "\n" + npc_dict[npc]["seasonal"]

					embed = discord.Embed(title="[" + str(npc) + "] " + npc_dict[npc]["name"], 
					colour=npc_embed_colour, 
					url="https://www.torn.com/profiles.php?XID=" + str(npc),
					description = description_text)
					embed.set_thumbnail(url=npc_url)

					return embed

				description_text = "Hit points: " + str("{:,.0f}".format(npc_dict[npc]["hp"]))

				now_time = datetime.utcnow()

				if npc_dict[npc]["active"] == "yes":


					#.strftime("%H:%M")
					hosp_out = datetime.utcfromtimestamp(npc_hosp[npc])
					level1 = hosp_out + timedelta(0,60)
					level2 = hosp_out + timedelta(0,(30*60))
					level3 = hosp_out + timedelta(0,(90*60))
					level4 = hosp_out + timedelta(0,(210*60))
					level5 = hosp_out + timedelta(0,(450*60))

					now_time = datetime.utcnow()



					if now_time > level5:
						npc_name_txt = "Level 5"
						npc_value_txt = "NPC is at max level"
					
					elif now_time > level4:
						npc_name_txt = "Level 4"

						time_left = ""
						xnow = now_time
						xthen = level5
						xdiff = xthen - xnow
						xdays = xdiff.days
						xseconds = xdiff.seconds
						xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
						xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
						xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

						if xhours > 0:
							time_left = time_left + str(xhours) + " hours, " 

						time_left = time_left + str(xmins) + " minutes" 
						
						npc_value_txt = "Level 5 in " + time_left + " (" + level5.strftime("%H:%M") + ")"
					
					elif now_time > level3:
						npc_name_txt = "Level 3"

						time_left = ""
						xnow = now_time
						xthen = level4
						xdiff = xthen - xnow 
						xdays = xdiff.days
						xseconds = xdiff.seconds
						xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
						xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
						xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

						if xhours > 0:
							time_left = time_left + str(xhours) + " hours, " 

						time_left = time_left + str(xmins) + " minutes" 
						
						npc_value_txt = "Level 4 in " + time_left + " (" + level4.strftime("%H:%M") + ")"
					


					elif now_time > level2:
						npc_name_txt = "Level 2"

						time_left = ""
						xnow = now_time
						xthen = level4
						xdiff = xthen - xnow 
						xdays = xdiff.days
						xseconds = xdiff.seconds
						xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
						xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
						xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

						if xhours > 0:
							time_left = time_left + str(xhours) + " hours, " 

						time_left = time_left + str(xmins) + " minutes" 
						


						npc_value_txt = "Level 4 in " + time_left + " (" + level4.strftime("%H:%M") + ")"
					
					elif now_time > level1:
						npc_name_txt = "Level 1"

						time_left = ""
						xnow = now_time
						xthen = level4
						xdiff = xthen - xnow 
						xdays = xdiff.days
						xseconds = xdiff.seconds
						xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
						xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
						xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

						if xhours > 0:
							time_left = time_left + str(xhours) + " hours, " 

						time_left = time_left + str(xmins) + " minutes" 
						


						npc_value_txt = "Level 4 in " + time_left + " (" + level4.strftime("%H:%M") + ")"

					elif now_time < level1:
						npc_name_txt = "In Hospital"

						time_left = ""
						xnow = now_time
						xthen = level4
						xdiff = xthen - xnow 
						xdays = xdiff.days
						xseconds = xdiff.seconds
						xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
						xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
						xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

						if xhours > 0:
							time_left = time_left + str(xhours) + " hours, " 

						time_left = time_left + str(xmins) + " minutes" 
						


						npc_value_txt = "Level 4 in " + time_left + " (" + level4.strftime("%H:%M") + ")"

					else:
						npc_name_txt = "ERROR"
						npc_value_txt = "Something went wrong"

					description_text = description_text + "\n" + npc_value_txt
					
				else:
					description_text = description_text + "\n" + "Seasonal NPC: " + npc_dict[npc]["seasonal"]
					npc_name_txt = "Level 5"
					npc_value_txt = ""

				npc_url = npc_dict[npc]["img_url"]

				embed = discord.Embed(title="[" + str(npc) + "] " + npc_dict[npc]["name"] + " (" + npc_name_txt + ")", 
					colour=npc_embed_colour, 
					url="https://www.torn.com/profiles.php?XID=" + str(npc),
					description = description_text)
				embed.set_thumbnail(url=npc_url)

				items = npc_dict[npc]["items"]
				for item in items:

					loots = items[item]
					loot_list = ""
					for loot in loots:
						loot_list = loot_list + "" + loots[loot] + "\n"
					embed.add_field(name=item, value=loot_list)
				#embed.add_field(name="level4 timestamp", value=datetime.fromtimestamp(level4.timestamp()).strftime("%H:%M"))
				embed.set_footer(text="Current Torn Time (TCT): " + now_time.strftime("%H:%M"))
				
				return embed

		return


	async def npc_list(self):

		red_colour = discord.Colour(0xe74c3c)
		blue_colour = discord.Colour(0x5dd3fa)
		green_colour = discord.Colour(0x2ecc71)

		npc_embed_colour = green_colour

		APIURL = "https://yata.yt/api/v1/loot/"
	#	response = APIURL
	#	await ctx.send(response)


		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		data = r.json() # translates that response into a dict variable
		npc_hosp = data["hosp_out"]

		#await ctx.send("hospital out information: ")
		#await ctx.send(npc_hosp)



		if os.path.isfile("./shared/npc_details.json") == False:
			# File doesnt exist
			raise __main__.NoFile("npc_details.json")

		with open("./shared/npc_details.json","r") as inf:		
			npc_dict = json.load(inf)


		embed = discord.Embed(title="Current NPC Status", 
		colour=npc_embed_colour)

		for npc in npc_dict:
			if npc_dict[npc]["seasonal"] == "no":

				#.strftime("%H:%M")
				hosp_out = datetime.utcfromtimestamp(npc_hosp[npc])
				level1 = hosp_out + timedelta(0,60)
				level2 = hosp_out + timedelta(0,(30*60))
				level3 = hosp_out + timedelta(0,(90*60))
				level4 = hosp_out + timedelta(0,(210*60))
				level5 = hosp_out + timedelta(0,(450*60))

				now_time = datetime.utcnow()



				if now_time > level5:
					npc_name_txt = npc_dict[npc]["name"] + " at Level 5"
					npc_value_txt = " \u200b"
					npc_value_txt = npc_value_txt + " \n "
				
				elif now_time > level4:
					npc_name_txt = npc_dict[npc]["name"] + " at Level 4"

					time_left = ""
					xnow = now_time
					xthen = level5
					xdiff = xthen - xnow
					xdays = xdiff.days
					xseconds = xdiff.seconds
					xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
					xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
					xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

					if xhours > 0:
						time_left = time_left + str(xhours) + " hours, " 

					time_left = time_left + str(xmins) + " minutes" 
					
					npc_value_txt = "Level 5 at " + level5.strftime("%H:%M:%S") + "\n" + time_left
				
				elif now_time > level3:
					npc_name_txt = npc_dict[npc]["name"] + " at Level 3"

					time_left = ""
					xnow = now_time
					xthen = level4
					xdiff = xthen - xnow 
					xdays = xdiff.days
					xseconds = xdiff.seconds
					xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
					xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
					xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

					if xhours > 0:
						time_left = time_left + str(xhours) + " hours, " 

					time_left = time_left + str(xmins) + " minutes" 
					
					npc_value_txt = "Level 4 at " + level4.strftime("%H:%M:%S") + "\n" + time_left
				


				elif now_time > level2:
					npc_name_txt = npc_dict[npc]["name"] + " at Level 2"

					time_left = ""
					xnow = now_time
					xthen = level4
					xdiff = xthen - xnow 
					xdays = xdiff.days
					xseconds = xdiff.seconds
					xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
					xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
					xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

					if xhours > 0:
						time_left = time_left + str(xhours) + " hours, " 

					time_left = time_left + str(xmins) + " minutes" 
					


					npc_value_txt = "Level 4 at " + level4.strftime("%H:%M:%S") + "\n" + time_left
				
				elif now_time > level1:
					npc_name_txt = npc_dict[npc]["name"] + " at Level 1"

					time_left = ""
					xnow = now_time
					xthen = level4
					xdiff = xthen - xnow 
					xdays = xdiff.days
					xseconds = xdiff.seconds
					xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
					xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
					xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

					if xhours > 0:
						time_left = time_left + str(xhours) + " hours, " 

					time_left = time_left + str(xmins) + " minutes" 
					


					npc_value_txt = "Level 4 at " + level4.strftime("%H:%M:%S") + "\n" + time_left

				elif now_time < level1:
					npc_name_txt = npc_dict[npc]["name"] + " is in Hospital"

					time_left = ""
					xnow = now_time
					xthen = level4
					xdiff = xthen - xnow 
					xdays = xdiff.days
					xseconds = xdiff.seconds
					xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
					xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
					xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)

					if xhours > 0:
						time_left = time_left + str(xhours) + " hours, " 

					time_left = time_left + str(xmins) + " minutes" 
					


					npc_value_txt = "Level 4 at " + level4.strftime("%H:%M:%S") + "\n" + time_left

				else:
					npc_name_txt = "ERROR"
					npc_value_txt = "Something went wrong"

				npc_value_txt = npc_value_txt + "\n" + "\n" + "[Attack](https://www.torn.com/loader2.php?sid=getInAttack&user2ID=" + str(npc) + ") | [Profile](https://www.torn.com/profiles.php?XID=" + str(npc) + ")" + "\n "
				
				embed.add_field(name=npc_name_txt, value=npc_value_txt)
			embed.set_footer(text="Current Torn Time (TCT): " + now_time.strftime("%H:%M"))
										
		return embed

	@commands.command(name='lootrole', aliases = ["loot", "lootping"] ,help="Add the loot ping role (or remove it if you already have it")
	async def lootrole(self,ctx):

		role = discord.utils.get(ctx.guild.roles, name="lootping")
		user = ctx.author

		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}")
		else:
		  	await user.add_roles(role) #adds role if not already has it
		  	await ctx.send(f"Added {role} to {user.mention}") 

		return


def setup(bot):
	bot.add_cog(Npc_cog(bot))