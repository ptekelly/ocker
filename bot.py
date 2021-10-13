# bot.py
import os
import random
import requests
import json
import discord
import os.path
import sched, time
import re
import threading
import typing
import collections
import traceback
import sys

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APIKEY = os.getenv('API_KEY')
APIADDRESS = os.getenv('API_ADDRESS')

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)

bot.v_apiKey = APIKEY
bot.v_apiAddress = APIADDRESS


@bot.command(hidden = True)
async def load(ctx, filename):
	bot.load_extension(f'cogs.{filename}')
	print('loading ' + filename + ".py")

@bot.command(hidden = True)
async def unload(ctx, filename):
	print('unloading ' + filename + ".py")
	bot.unload_extension(f'cogs.{filename}')

if os.path.isdir("./cogs/"):
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			print("Loading: " + filename)
			bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
	print('Bot Online.')

	channel_list = {}
	channel_dict = {}

	if os.path.isfile("./channels.json"):
		# File already exists
		with open("./channels.json","r") as inf:		
			channel_dict = json.load(inf)

	for guild in bot.guilds:
		if str(guild.id) in channel_dict:
			for channel in guild.text_channels:
				if str(channel_dict[str(guild.id)]["main"]) == str(channel.id):
					print(guild.name + " (" + str(guild.id) + ")  -  " + str(channel.name) + " (" + str(channel.id) + ")")
					channel_list[str(guild.id)] = channel.id
		else:
			for channel in guild.text_channels:
				if channel.name == "general":
					print(guild.name + " (" + str(guild.id) + ")  -  " + str(channel.name) + " (" + str(channel.id) + ")")
					channel_list[str(guild.id)] = channel.id
	for guild in channel_list:

		channel_id = channel_list[guild]
		myguild = bot.get_guild(int(guild))
		mychannel = bot.get_channel(channel_id)
		channel_greet = ""

		channel_greet = channel_greet + str(bot.user.display_name) + " is online"

		await mychannel.send(channel_greet)





	



@bot.check
async def checkchannel(ctx):

	#print(bot.command)

	#print(str(ctx.message.channel.type))
	if str(ctx.message.channel.type) == "private":
		channel_allowed = True
		return channel_allowed
	else:	
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
					if this_channel_id == channel_dict[server_id]["main"] or this_channel_id == channel_dict[server_id]["mgt"]:
						#print("This channel matches allowd channel")
						channel_allowed = True
						return channel_allowed
					else:
						#print("this is not allowed channel")
						await ctx.message.delete()
						return channel_allowed
				else:
					#print("Server id does not exist - but file does - therefore allowed to post")
					channel_allowed = True
					return channel_allowed
		else:
			#print("file does not exist")
			channel_allowed = True
			return channel_allowed


class NoFile(commands.CommandError):
	pass

class NoDiscordID(commands.CommandError):
	pass

class NoAPI(commands.CommandError):
	pass

class APIIssue(commands.CommandError):
	pass

class APICallError(commands.CommandError):
	pass



@bot.command()
async def test(ctx):
	user = discord.utils.get(ctx.guild.members, name = "Accy", discriminator = "1819")
	await ctx.send(user)

@bot.event
async def on_command_error(ctx, error):
	user = discord.utils.get(ctx.guild.members, name = "Accy", discriminator = "1819")

	if isinstance(error, commands.ChannelNotFound):
		return
	if isinstance(error, commands.errors.CheckFailure):
		pass
		#await ctx.send("Not this channel, dummy!!")
	elif isinstance(error, commands.errors.BadArgument):
		await ctx.send("Try the correct type of argumment for this command.  See !help <command> for more details")
	elif isinstance(error, NoFile):
		await ctx.send("The file **" + str(error) + "** is missing. Please speak to " + user.mention)
	elif isinstance(error, NoDiscordID):
		await ctx.send("The discord id is missing.  See !addid for more details.")
	elif isinstance(error, NoAPI):
		await ctx.send("API key is missing.  See !addapi for more details.")
	elif isinstance(error, APIIssue):
		await ctx.send("There is a problem with your API Key - try re-adding it with !addapi <YourAPIKey>")
	elif isinstance(error, APICallError):
		await ctx.send("There is a problem with the API call: from " + error)
	elif isinstance(error, commands.errors.MissingRequiredArgument):
		await ctx.send("You are missing the proper argument for this command - see help for more details")
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



#remove this no longer used
def xgetid(member):
	discord_id = str(member.id)
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)
		selection = dict.get(discord_id,"ERROR: id not found")
		if selection == "ERROR: id not found":
			raise NoDiscordID("Missing Discord ID")
			#response = selection
		else:
			response = selection["torn_id"]
	else:
		#response = "ERROR: File Not found"
		raise NoFile("missing file")
	#await ctx.send(response)
	return response



async def get_user_data(member,infotype):
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)
			#print("file found")
	else:
		raise NoFile("users.json")

	discord_id = str(member.id)
	if discord_id in dict:

		if infotype == "torn_id":
			if "torn_id" in dict[discord_id]:
				return(dict[discord_id]["torn_id"])
			else:
				raise NoDiscordID("No discord id")
		elif infotype == "torn_api":
			if "torn_api" in dict[discord_id]:
				return(dict[discord_id]["torn_api"])
			else:
				raise NoAPI("No API")
		else:
			return("ERROR:Infotype invalue")

	else:
		raise NoDiscordID("no discord")

	return


async def get_user_data_from_id(torn_id,infotype):
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)

	else:
		raise NoFile("users.json")

	found = False
#	print("pre loop")
	for disco_user in dict:
		#print(disco_user)
		if dict[disco_user]["torn_id"] == torn_id:
			#print(torn_id)
			#print(disco_user)
			disco_user_id = disco_user
			if "torn_api" in dict[disco_user]:
				torn_api = dict[disco_user]["torn_api"]
				if "eta_lock" in dict[disco_user]:
					eta_lock = dict[disco_user]["eta_lock"]
				else:
					eta_lock = "ERROR:No eta_lock for this user"
				found = True
			else:
				raise NoAPI("no api")
				return

	if found:
		#print("found")
		if infotype == "disco_id":
			#print("disco id asked for")
			return(disco_user_id)
		elif infotype == "torn_api":
			return(torn_api)
		elif infotype == "eta_lock":
			return(eta_lock)
		else:
			return("ERROR:Infotype invalue")

	else:
		#print("not found")
		return("ERROR:no user")

	#print("Unknown")
	return("ERROR:Unknown")


@bot.command(name='travel', help='!travel lists all travel destinations.  !travel <dest> will list items for sale in that desitnation (eg arg, argentina)')
async def travel(ctx, *dest):
	

	dest = " ".join(dest)

	if os.path.isfile("./destinations.json") == False:
		# File doesnt exist
		raise NoFile("destinations.json")		
	if os.path.isfile("./lookupdest.json") == False:
		# File doesnt exist
		raise NoFile("lookupdest.json")

	with open("./destinations.json","r") as inf:		
		dest_dict = json.load(inf)

	with open("./lookupdest.json","r") as inf:		
		lookup_dest_dict = json.load(inf)


	APIURL = "https://yata.yt/api/v1/travel/export/"


	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	data = r.json() # translates that response into a dict variable
	selection = data["stocks"]

	if len(dest) == 0:

		dest_list = ""

		country_list = {}

		for country in selection:
			country_list[dest_dict[country]["realname"]] = country


		for country in sorted(country_list):
			dest_list = dest_list + country + " (" + country_list[country] + ")\n"

		embed = discord.Embed(title=":airplane: Foreign Travel", 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/travelagency.php")
		embed.add_field(name="Possible Destinations", value=dest_list)
									
		await ctx.send(embed=embed)
		return

	else:

		if dest.lower() in lookup_dest_dict:
			stock_list = {}
			no_stock_list = {}
			for stock in selection[lookup_dest_dict[dest.lower()]]["stocks"]:
				if stock["quantity"] == 0:

					no_stock_list[stock["name"]] = "$" +  str("{:,.0f}".format(stock["cost"]))
				else:
					stock_list[stock["name"]] = str(stock["quantity"]) + " @ $" +  str("{:,.0f}".format(stock["cost"]))

			stocked_field = ""

			for stocked in sorted(stock_list):
				stocked_field = stocked_field + "***" + stocked + "*** (" + stock_list[stocked] + ")\n"
			
			no_stocked_field = ""

			for no_stocked in sorted(no_stock_list):
				no_stocked_field = no_stocked_field + "***" + no_stocked + "*** (" + no_stock_list[no_stocked] + ")\n"

		else:
			response = "Destination not found"		
			await ctx.send(response)
			return

		special_text = ""
		if "special" in dest_dict[lookup_dest_dict[dest.lower()]]:
			special_text = ":sunny: Special: **" + dest_dict[lookup_dest_dict[dest.lower()]]["special"] + "**"


		embed = discord.Embed(title=":airplane: Stock list for " + dest_dict[lookup_dest_dict[dest.lower()]]["realname"], 
		colour=discord.Colour(0x5dd3fa), 
		url="https://wiki.torn.com/wiki/" + dest_dict[lookup_dest_dict[dest.lower()]]["wikilink"],
		description=special_text)
		embed.set_thumbnail(url="https://www.torn.com/images/v2/travel_agency/flags/fl_" + dest_dict[lookup_dest_dict[dest.lower()]]["imagetag"] + ".png")
		embed.add_field(name="In Stock", value=stocked_field,inline=True)
		embed.add_field(name="Out of Stock", value=no_stocked_field,inline=True)
		embed.set_footer(text="Stock list last updated at " + (datetime.utcfromtimestamp(selection[lookup_dest_dict[dest.lower()]]["update"]).strftime("%H:%M")) + " (Torn time)")

									
		await ctx.send(embed=embed)
		return


	return



def strip_tags(text):

	new_text = ""

	left_tag = ""
	right_tag = ""
	tagged_text = ""

	ltag = False
	rtag = False
	tagged = False

	for c in text:
		if c == "<":
			if tagged:
				rtag = True
				ltag = False
			else:
				ltag = True
				rtag = False
		elif c == ">":
				if rtag:
					tagged = False
					#await ctx.send(left_tag)

					if "bold" in left_tag:
						tagged_text = "**" + tagged_text + "**"
					elif "italic" in left_tag:
						tagged_text = "*" + tagged_text + "*"

					#if len(tagged_text) >0:
						#await ctx.send(tagged_text)
					#await ctx.send(right_tag)

					rtag = False
					new_text = new_text + tagged_text
					left_tag = ""
					right_tag = ""
					tagged_text = ""
				if ltag:
					tagged = True
					ltag = False

		else:
			if ltag:
				left_tag = left_tag + c
			elif rtag:
				right_tag = right_tag + c
			elif tagged:
				tagged_text = tagged_text + c
			else:
				new_text = new_text + c

	return new_text



async def fc_stocks_by_item():
	if os.path.isfile("./destinations.json") == False:
		# File doesnt exist
		response = "File doesn't exist"
		await ctx.send(response)
		return "Error"
		
	if os.path.isfile("./lookupdest.json") == False:
		# File doesnt exist
		response = "File doesn't exist"
		await ctx.send(response)
		return "Error"


	with open("./destinations.json","r") as inf:		
		dest_dict = json.load(inf)

	with open("./lookupdest.json","r") as inf:		
		lookup_dest_dict = json.load(inf)

	fc_list_by_item = {}

	APIURL = "https://yata.yt/api/v1/travel/export/"

	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	data = r.json() # translates that response into a dict variable
	for_stock = data["stocks"]

	for country in for_stock:
		for stock in for_stock[country]["stocks"]:	
			if stock["name"] in fc_list_by_item:
				fc_list_by_item[stock["name"]][dest_dict[country]["realname"]] = {"cost": stock["cost"],"update":for_stock[country]["update"], "quantity": stock["quantity"]}
			else:
				fc_list_by_item[stock["name"]] = {dest_dict[country]["realname"]: {"cost": stock["cost"],"update":for_stock[country]["update"], "quantity": stock["quantity"]}}
	
	return fc_list_by_item
	




def get_user_name_from_id(user_id):
	v_apiType = "user"
	v_apiSelection = "basic"
	APIURL = bot.v_apiAddress+v_apiType+'/'+str(user_id)+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	if "error" in selection:
		return "error:  cannot find user with that ID"
	return selection["name"]



@bot.command(name="estimate", aliases=["est"], help="Estimate stats for given Torn ID")
async def estimate(ctx, torn_id: typing.Union[int,str]= 0):

	if type(torn_id) == str:
		await ctx.send("Not a torn user id")
		return

	if torn_id == 0:
		await ctx.send("Provide a valid torn user id")
		return

	stat_level = 0
	stat_count = 0
	stat_total = 0
	est_stat_text = ""

	rank_names = {"Absolute beginner":0,
					"Beginner":1,
					"Inexperienced":2,
					"Rookie":3,
					"Novice":4,
					"Below average":5,
					"Average":6,
					"Reasonable":7,
					"Above average":8,
					"Competent":9,
					"Highly competent":10,
					"Veteran":11,
					"Distinguished":12,
					"Highly distinguished":13,
					"Professional":14,
					"Star":15,
					"Master":16,
					"Outstanding":17,
					"Celebrity":18,
					"Supreme":19,
					"Idolized":20,
					"Champion":21,
					"Heroic":22,
					"Legendary":23,
					"Elite":24,
					"Invincible":25
				}

	v_apiType = "user"
	v_apiSelection = "profile"
	APIURL = bot.v_apiAddress+v_apiType+'/'+str(torn_id)+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	if "error" in selection:
		await ctx.send("there is an issue with the user id")
		return


	name = selection["name"]
	level = selection["level"]
	rank = selection["rank"]

	v_apiType = "user"
	v_apiSelection = "crimes"
	APIURL = bot.v_apiAddress+v_apiType+'/'+str(torn_id)+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	v1 = selection["criminalrecord"]
	if "error" in selection:
		await ctx.send("there is an issue with the user id")
		return

	crimes = v1["total"]

	v_apiType = "user"
	v_apiSelection = "personalstats"
	APIURL = bot.v_apiAddress+v_apiType+'/'+str(torn_id)+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	v1 = selection["personalstats"]
	if "error" in selection:
		await ctx.send("there is an issue with the user id")
		return

	networth = v1["networth"]
	useractivity = v1["useractivity"] # time played
	xantaken = v1["xantaken"] #xanax used
	refills = v1["refills"] #energy refills
	energydrinkused = v1["energydrinkused"] #energy cans

	xseconds = useractivity
	xdays = divmod(xseconds, (60*60*24))[0]
	xdaysr = divmod(xseconds, (60*60*24))[1]
	xhours = divmod(xdaysr, (60*60))[0]
	xhoursr = divmod(xdaysr, (60*60))[1]
	xmins = divmod(xhoursr, (60))[0]
	xminsr = divmod(xhoursr, (60))[1]
	
	timeplayed_text = "Time Played: "
	if xdays > 0:
		timeplayed_text = timeplayed_text + str(xdays) + "d "
	if xhours > 0:
		timeplayed_text = timeplayed_text + str(xhours) + "h "
	if xmins > 0:
		timeplayed_text = timeplayed_text + str(xmins) + "m "
	
	


	activity_field = timeplayed_text + "\n"
	activity_field = activity_field + "Xanax Taken: " + str(xantaken) + "\n"
	activity_field = activity_field + "Energy Refills: " + str(refills) + "\n"
	activity_field = activity_field + "Energy Cans Drunk: " + str(energydrinkused)
	

	if crimes > 50000:
		stat_count = stat_count + 6
	elif crimes > 30000:
		stat_count = stat_count + 5
	elif crimes > 20000:
		stat_count = stat_count + 4
	elif crimes > 10000:
		stat_count = stat_count + 3
	elif crimes > 5000:
		stat_count = stat_count + 2
	elif crimes > 100:
		stat_count = stat_count + 1


	if level > 99:
		stat_count = stat_count + 8
	elif level > 70:
		stat_count = stat_count + 7
	elif level > 49:
		stat_count = stat_count + 6
	elif level > 30:
		stat_count = stat_count + 5
	elif level > 25:
		stat_count = stat_count + 4
	elif level > 10:
		stat_count = stat_count + 3
	elif level > 5:
		stat_count = stat_count + 2
	elif level > 1:
		stat_count = stat_count + 1
		

	if networth > 50000000000:
		stat_count = stat_count + 5
	elif networth > 5000000000:
		stat_count = stat_count + 4
	elif networth > 500000000:
		stat_count = stat_count + 3
	elif networth > 50000000:
		stat_count = stat_count + 2
	elif networth > 5000000:
		stat_count = stat_count + 1

	for x in rank_names:
		if rank.startswith(x):
			stat_total = rank_names[x]

	if stat_total == 0 and not rank.startswith("Absolute beginner"):
		await ctx.send("problem with rank name")
		return

	stat_level = stat_total - stat_count


	if stat_level > 5:
		est_stat_text = "More than 200m"
	elif stat_level > 4:
		est_stat_text = "20m to 250m"
	elif stat_level > 3:
		est_stat_text = "2m to 35m"
	elif stat_level > 2:
		est_stat_text = "200k to 2.5m"
	elif stat_level > 1:
		est_stat_text = "20k to 250k"
	elif stat_level > 0:
		est_stat_text = "2k to 25k"
	else:
		est_stat_text = "Less than 2.5k"

	title = "Estimated stats for " + name + "[" + str(torn_id) + "]"

	embed = discord.Embed(title=title, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/profiles.php?XID="+str(torn_id), 
		description= est_stat_text)

	embed.add_field(name="User Activity", value=activity_field,inline=False)
	msg = await ctx.send(embed=embed)


@bot.command(name='oc', help='Returns organised crime information for Discord user name (eg @Accy - requires Torn ID registered with Bot) or any Torn ID.  If no parameter provided it will use your own Discord name (Torn ID needs to be registered')
async def oc(ctx, member: typing.Union[discord.Member,int,str] = "NA"):
	

	if member == "NA":
		member = ctx.author
	
	if type(member) == discord.Member:
		#await ctx.send("Member")
		#torn_id = getid(member)
		torn_id = await get_user_data(member,"torn_id")
		#await ctx.send("torn_id: " + torn_id)

	elif type(member) == int:
		#await ctx.send("user id")
		torn_id = str(member)
		#await ctx.send("torn_id: " + torn_id)

	elif type(member) == str:
		#await ctx.send("String provided")
		if member.lower() == "list":
			#await ctx.send("'**List**'' is not yet implemented - coming soon!")
			await oc_list(ctx)
			return
		else:
			await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy), torn id (e.g. 2586638) or 'list' (not implemented yet) ")
			return

	await oc_work(ctx,torn_id)

	return


async def oc_work(ctx, torn_id):
	v_apiType = 'faction'
	v_apiSelection = 'crimes'
	
	APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	allcrimes = selection["crimes"]
	currentcrimes = {}
	crime_name = 'NOT SET'
	my_crime_id = 0

	for crime in allcrimes:
		if allcrimes[crime]["time_completed"] == 0:
			currentcrimes[crime] = allcrimes[crime]

	found_participant = False

	for crime in currentcrimes:
			
		for participants in currentcrimes[crime]["participants"]:
			for pid in participants:
	
				if pid == torn_id:
					my_crime = crime
					found_participant = True
	
	if found_participant == False:
		await ctx.send("No crimes found for Torn player ID: **" + torn_id + "**.")
		return
	description_text = ""
	

	red_crime = discord.Colour(0xe74c3c)
	blue_crime = discord.Colour(0x5dd3fa)
	green_crime = discord.Colour(0x2ecc71)
	crime_colour = blue_crime

	
	crime_title = ""

	allok = True
	participants_list_text = ""
	for participants in currentcrimes[my_crime]["participants"]:
		for pid in participants:
			participants_list_text = participants_list_text + "[" + get_user_name_from_id(pid) + " (" + str(pid) + ")" + "](https://www.torn.com/profiles.php?XID=" + str(pid) + ")" 
			participants_list_text = participants_list_text + " - " + participants[pid]["description"] + "\n"
			if participants[pid]["state"] != "Okay":
				allok = False

	crime_title = crime_title + currentcrimes[my_crime]["crime_name"]

	if currentcrimes[my_crime]["initiated"] == 0 and currentcrimes[my_crime]["time_left"] == 0:
		#overdue
		crime_colour = green_crime
		if allok:
			description_text = description_text + "This crime is now ready. Please initiate crime and replan the next one."	
		else:
			description_text = description_text + "This crime is now ready. Can all participants please return to Torn so the crime can be initiated."	
			crime_colour = red_crime
		crime_title = crime_title + " (Ready)"
	

	embed = discord.Embed(title = crime_title,
		colour=crime_colour, 
		url="https://www.torn.com/factions.php?step=your#/tab=crimes",
		description=description_text
		)

	embed.add_field(name="Participants", value=participants_list_text,inline=False)

	embed.add_field(name="Time Started", value=datetime.utcfromtimestamp(currentcrimes[my_crime]["time_started"]).strftime("%H:%M (%d-%b)"),inline=True)
	embed.add_field(name="Time Ready", value=datetime.utcfromtimestamp(currentcrimes[my_crime]["time_ready"]).strftime("%H:%M (%d-%b)"),inline=True)

	if not(currentcrimes[my_crime]["initiated"] == 0 and currentcrimes[my_crime]["time_left"] == 0):


		time_left = ""
		xnow = datetime.utcnow()
		xthen = datetime.utcfromtimestamp(currentcrimes[my_crime]["time_ready"])
		xdiff = xthen - xnow
		xdays = xdiff.days
		xseconds = xdiff.seconds
		xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
		xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
		xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)
		


		if xdiff.days > 0:
			time_left = time_left + str(xdays) + "d "

		time_left = time_left + str(xhours) + "h "
		time_left = time_left + str(xmins) + "m"
		
		embed.add_field(name="Time remaining", value=time_left)

		#embed.add_field(name="Time Left", value=datetime.utcfromtimestamp(currentcrimes[my_crime]["time_left"]),inline=True)
	embed.add_field(name="Planned By", value="[" + get_user_name_from_id(currentcrimes[my_crime]["planned_by"]) + "](https://www.torn.com/profiles.php?XID=" + str(currentcrimes[my_crime]["planned_by"]) + ")",inline=True)


	await ctx.send(embed=embed)
	return



async def oc_list(ctx):
	v_apiType = 'faction'
	v_apiSelection = 'crimes'
	APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	selection = r.json() # translates that response into a dict variable
	allcrimes = selection["crimes"]
	currentcrimes = {}
	crime_name = 'NOT SET'
	my_crime_id = 0

	for crime in allcrimes:
		if allcrimes[crime]["time_completed"] == 0:
			currentcrimes[crime] = allcrimes[crime]

	found_participant = False

	ready_list = {}
	not_ready_list = {}
	not_ready_sort = {}

	for crime in currentcrimes:
		time_left_text = "("
		
		if currentcrimes[crime]["initiated"] == 0 and currentcrimes[crime]["time_left"] != 0:

			time_left = ""
			xnow = datetime.utcnow()
			xthen = datetime.utcfromtimestamp(currentcrimes[crime]["time_ready"])
			xdiff = xthen - xnow
			xdays = xdiff.days
			xseconds = xdiff.seconds
			xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
			xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
			xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)


		#response = response + "\n" + currentcrimes[crime]["crime_name"] + " ("

			if xdays > 0:
				time_left_text = time_left_text + str(xdays) + "d "
			time_left_text = time_left_text + str(xhours) + "h "
			time_left_text = time_left_text + str(xmins) + "m left)"

			
			not_ready_list[crime] = {"crime_name":currentcrimes[crime]["crime_name"], "time_left": currentcrimes[crime]["time_left"], "status": time_left_text}
			not_ready_sort[crime] = currentcrimes[crime]["time_left"]
			

		elif currentcrimes[crime]["initiated"] == 0 and currentcrimes[crime]["time_left"] == 0:
			allok = True
			participants_list_text = ""	
			
			for participants in currentcrimes[crime]["participants"]:
				for pid in participants:
					
					participants_list_text = participants_list_text + "[" + get_user_name_from_id(pid) + " (" + str(pid) + ")" + "](https://www.torn.com/profiles.php?XID=" + str(pid) + ")" 
					participants_list_text = participants_list_text + " - " + participants[pid]["description"] + "\n"
					if participants[pid]["state"] != "Okay":
						allok = False
					if allok:
						ready_list[crime] = {"crime_name":currentcrimes[crime]["crime_name"], "time_left": currentcrimes[crime]["time_left"], "status": "Ready", "participants": participants_list_text}
					else:
						ready_list[crime] = {"crime_name":currentcrimes[crime]["crime_name"], "time_left": currentcrimes[crime]["time_left"], "status": "Not ready", "participants": participants_list_text}
					

	red_crime = discord.Colour(0xe74c3c)
	blue_crime = discord.Colour(0x5dd3fa)
	green_crime = discord.Colour(0x2ecc71)
	crime_colour = blue_crime
	

	if len(ready_list) > 0:

		for readycrime in ready_list:

			crime_title = ready_list[readycrime]["crime_name"] + " (" + ready_list[readycrime]["status"] + ")" 

			if ready_list[readycrime]["status"] == "Ready":
				crime_colour = green_crime
			else:
				crime_colour = red_crime

			description_text = ready_list[readycrime]["participants"]	


			overdue_text = ""
			xnow = datetime.utcnow()
			xthen = datetime.utcfromtimestamp(currentcrimes[readycrime]["time_ready"])
			xdiff = xnow - xthen 
			xdays = xdiff.days
			xseconds = xdiff.seconds
			xhours = divmod(divmod(xdiff.seconds, 60)[0],60)[0]
			xmins = divmod(xseconds - (xhours * 60 * 60),60)[0]
			xsecs = xseconds - (xhours * 60 * 60) - (xmins * 60)
		
			if xdays > 0:
				overdue_text = overdue_text + str(xdays) + "d "
			overdue_text = overdue_text + str(xhours) + "h "
			overdue_text = overdue_text + str(xmins) + "m overdue"				

			embed = discord.Embed(title = crime_title,
				colour=crime_colour, 
				url="https://www.torn.com/factions.php?step=your#/tab=crimes",
				description=description_text
				)
			embed.set_footer(text=overdue_text)

			await ctx.send(embed=embed)


	if len(not_ready_list) > 0:

		sortlist = sorted(not_ready_sort.items(), key=lambda x:x[1])
		sortlist = dict(sortlist)
		

		notreadyoc_desc = ""

		for notreadycrime in sortlist:
						
			notreadyoc_desc = notreadyoc_desc + "\n" + not_ready_list[notreadycrime]["crime_name"] + " " + not_ready_list[notreadycrime]["status"]


		embed = discord.Embed(title='Organised Crime List (not ready to initiate)',
                       url='https://www.torn.com/factions.php?step=your#/tab=crimes',
                       description=notreadyoc_desc)
		embed.set_footer(text="Total OCs in progress: " + str(len(not_ready_sort)))

		await ctx.send(embed=embed)

	return




@bot.command(name='setmgtchannel', hidden = True)
async def setmgtchannel(ctx, mychannel: discord.TextChannel = "NA"):
	if mychannel == "NA":
		await ctx.send("Channel not found: Please enter a valid text channel using #....")
	server_id = str(ctx.guild.id)
	if mychannel in ctx.guild.text_channels:


		if os.path.isfile("./channels.json"):
			# File already exists
			with open("./channels.json","r") as inf:		
				channel_dict = json.load(inf)
				
				if server_id in channel_dict:
					channel_dict[server_id].update({"mgt": mychannel.id})
				else:
					channel_dict[server_id] = {"mgt": mychannel.id}
			
		else:
		#	file does not exist - new dictionary
			channel_dict = {server_id: {"mgt":mychannel.id}}

		with open("./channels.json", "w") as data_file:
			json.dump(channel_dict, data_file, indent=2)
		await ctx.send(mychannel.name + ' is now set as the Ocker Bot manager channel')
	return



@bot.command(name='setchannel', hidden = True)
async def setchannel(ctx, mychannel: discord.TextChannel = "NA"):
	if mychannel == "NA":
		await ctx.send("Channel not found: Please enter a valid text channel using #....")
	server_id = str(ctx.guild.id)
	if mychannel in ctx.guild.text_channels:


		if os.path.isfile("./channels.json"):
			# File already exists
			with open("./channels.json","r") as inf:		
				channel_dict = json.load(inf)
				
				if server_id in channel_dict:
					channel_dict[server_id].update({"main": mychannel.id})
				else:
					channel_dict[server_id] = {"main": mychannel.id}
			
		else:
		#	file does not exist - new dictionary
			channel_dict = {server_id: {"main":mychannel.id}}

		with open("./channels.json", "w") as data_file:
			json.dump(channel_dict, data_file, indent=2)
		await ctx.send(mychannel.name + ' is now set as the Ocker Bot channel')
	return



@setchannel.error
async def setchan_error(ctx, error):
    if isinstance(error, commands.ChannelNotFound):
        await ctx.send("Channel not found: Please enter a valid text channel using #....")

	

@bot.command(name='allowedchannels', hidden = True)
async def allowedchannels(ctx):
	server_id = str(ctx.guild.id)
	if os.path.isfile("./channels.json"):
		# File already exists
		with open("./channels.json","r") as inf:		
			channel_dict = json.load(inf)
		
			if server_id in channel_dict:
				# Server id and file exist
				await ctx.send('The following are a list of allowed channels:')
				channel_list = channel_dict[server_id]
				for channel_id in channel_list:
					channel = ctx.guild.get_channel(channel_id)
					if channel:
						channel_name = channel.name
						await ctx.send(channel_name)
			else:
				# Server id does not exist - but file does
				await ctx.send('There are no channels in your allowed list therefore you can use any channel')
	else:
		#file does not exist
		await ctx.send('There are no channels in your allowed list therefore you can use any channel')
	return

	await ctx.send('You do not have the correct role for this command.')



@bot.command(name='stock', aliases = ["stocks"], help='List all stocks available (with not parameter) or with stock details if stock ID is provided (eg !stock TSB)')
async def stock(ctx, *args):

	v_apiType = "torn"
	v_apiSelection = "stocks"
	

	exact = False
	stock_name = " ".join(args)

	after_every = "every"
	after_list = "TCB:WLT:SYS:ISTC:TCM:TCP:ELT:MSG:IIL:TGP:WSU:YAZ"

	if stock_name.lower() == "!stock":
		response = "Recursion error ...... please refrain from AAAAaaaagghhhh........"
		await ctx.send(response)
		response = "....Recursion error ...... please refrain from AAAAaaaagghhhh........"
		await ctx.send(response)
		response = "........Recursion error ...... please refrain from AAAAaaaagghhhh........"
		await ctx.send(response)
		response = "............Recursion error ...... please refrain from AAAAaaaagghhhh........"
		await ctx.send(response)
		response = "................Recursion error ...... please refrain from AAAAaaaagghhhh........"
		await ctx.send(response)
		return


	APIURL = bot.v_apiAddress+v_apiType+'/?selections='+v_apiSelection+'&key='+bot.v_apiKey
	
	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	data = r.json() # translates that response into a dict variable
	selection = data["stocks"]
	short_list = {}


	for stock in selection:
		if stock_name.lower() == selection[stock]["acronym"].lower():

			if selection[stock]["acronym"] in after_list:
				after_every = "after"
		

			response = "Exact matching short name for your search text (*{0}*).".format(stock_name)
			await ctx.send(response)
			
			embed = discord.Embed(title=selection[stock]["acronym"] + ": " + selection[stock]["name"], 
					colour=discord.Colour(0x5dd3fa), 
					url="https://www.torn.com/stockexchange.php",
					description="**" + selection[stock]["name"] + "** provides **" + selection[stock]["benefit"]["description"] 
						+ "** "
						+ after_every 
						+ " **" 
						+ str(selection[stock]["benefit"]["frequency"]) 
						+ " days** when holding at least **" 
						+ str("{:,}".format(selection[stock]["benefit"]["requirement"]))
						+ "** shares currently valued at **$" 
						+ str("{:,.2f}".format(selection[stock]["benefit"]["requirement"] * selection[stock]["current_price"]))
						+ "** (unit price: **$" 
						+ str("{:,.2f}".format(selection[stock]["current_price"]))
						+ "**)"
					)
				
			embed.set_thumbnail(url="https://www.torn.com/images/v2/stock-market/logos/" + selection[stock]["acronym"] + ".png")
			
			await ctx.send(embed=embed)

			return



	for stock in selection:
		if stock_name.lower() in selection[stock]["name"].lower():
			if stock_name.lower() == selection[stock]["name"].lower():
				exact = True
				exact_list = {}
				
				response = selection[stock]["name"]
				await ctx.send(response)

				exact_list[stock] = selection[stock]


			else:
				short_list[stock] = selection[stock]


	if exact == True:
		response = "Exact matching stock for your search text (*{0}*).".format(stock_name)
		await ctx.send(response)

		for stock in exact_list:
			if selection[stock]["acronym"] in after_list:
				after_every = "after"
		
			embed = discord.Embed(title=selection[stock]["acronym"] + ": " + selection[stock]["name"], 
					colour=discord.Colour(0x5dd3fa), 
					url="https://www.torn.com/stockexchange.php",
					description="**" + selection[stock]["name"] + "** provides **" + selection[stock]["benefit"]["description"] 
						+ "** "
						+ after_every 
						+ " **" 
						+ str(selection[stock]["benefit"]["frequency"]) 
						+ " days** when holding at least **" 
						+ str("{:,}".format(selection[stock]["benefit"]["requirement"]))
						+ "** shares currently valued at **$" 
						+ str("{:,.2f}".format(selection[stock]["benefit"]["requirement"] * selection[stock]["current_price"]))
						+ "** (unit price: **$" 
						+ str("{:,.2f}".format(selection[stock]["current_price"]))
						+ "**)"
					)

			embed.set_thumbnail(url="https://www.torn.com/images/v2/stock-market/logos/" + selection[stock]["acronym"] + ".png")
			
			await ctx.send(embed=embed)

		if len(short_list) > 0:

			response = "Partial matches for search text (*{0}*).".format(stock_name)
			await ctx.send(response)

			response = ">>> ```"
			for sl_stock in short_list:

				response = response  + "\n" + short_list[sl_stock]["acronym"] + ": " + short_list[sl_stock]["name"] + " ($" + str(short_list[sl_stock]["current_price"]) + ")"      

			response = (response + "```")
			await ctx.send(response)

	
	else:
		if len(short_list) == 0:

			response = "Nothing matching your search text (*{0}*).".format(stock_name)
			await ctx.send(response)
		

		## one match (not exact)
		elif len(short_list) == 1:

			response = "Single match for your search text (*{0}*).".format(stock_name)
			await ctx.send(response)

			for stock in short_list:

				if selection[stock]["acronym"] in after_list:
					after_every = "after"
		
				embed = discord.Embed(title=selection[stock]["acronym"] + ": " + selection[stock]["name"], 
					colour=discord.Colour(0x5dd3fa), 
					url="https://www.torn.com/stockexchange.php",
					description="**" + selection[stock]["name"] + "** provides **" + selection[stock]["benefit"]["description"] 
						+ "** "
						+ after_every 
						+ " **" 
						+ str(selection[stock]["benefit"]["frequency"]) 
						+ " days** when holding at least **" 
						+ str("{:,}".format(selection[stock]["benefit"]["requirement"]))
						+ "** shares currently valued at **$" 
						+ str("{:,.2f}".format(selection[stock]["benefit"]["requirement"] * selection[stock]["current_price"]))
						+ "** (unit price: **$" 
						+ str("{:,.2f}".format(selection[stock]["current_price"]))
						+ "**)"
					)
					
				embed.set_thumbnail(url="https://www.torn.com/images/v2/stock-market/logos/" + selection[stock]["acronym"] + ".png")

				await ctx.send(embed=embed)

		else:
			if len(args) == 0:
				response = "List of all stocks."
			else:
				response = "List of matches for your search text (*{0}*).".format(stock_name)
			await ctx.send(response)

			response = ">>> ```"
			for sl_stock in short_list:

				response = response  + "\n" + short_list[sl_stock]["acronym"] + ": " + short_list[sl_stock]["name"] + " ($" + str(short_list[sl_stock]["current_price"]) + ")"      

			response = (response + "```")
			await ctx.send(response)

	return



@bot.command(name='item', help='Responds with data for item name provided')
async def item(ctx, *args):
	
	if len(args) == 0:
		response = "Please provide the name of (or part of) an item for example '!item hammer'."
		await ctx.send(response)
		return

	exact = False
	item_name = " ".join(args)

	if "hack" in item_name.lower():
		response = "You have entered the secret keyword (*{0}*) - congratulations!  \n However I will now have to kill you. \n Death squad arrival in 30 seconds, please stay calm.".format(item_name)
		await ctx.send(response)
		return		

	fc_list = await fc_stocks_by_item()

	if fc_list == "Error":
		return


	v_apiType = 'torn'
	v_apiSelection = 'items'

	APIURL = bot.v_apiAddress+v_apiType+'/?selections='+v_apiSelection+'&key='+bot.v_apiKey

	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	data = r.json() # translates that response into a dict variable
	selection = data["items"]
	short_list = {}


	for item in selection:
		if item_name.lower() in selection[item]["name"].lower():
			if item_name.lower() == selection[item]["name"].lower():
				exact = True
				exact_list = {}
				exact_list[item] = selection[item]["name"]
			else:
				short_list[item] = selection[item]["name"]


	if exact == True:
		footer_text = ""
		response = "Exact matching item for your search text (*{0}*).".format(item_name)
		await ctx.send(response)

		for sl_item in exact_list:

			desc_text = selection[sl_item]["description"]
			stripped_desc_text = strip_tags(desc_text)
			
			embed = discord.Embed(title="[" + str(sl_item) + "] " + selection[sl_item]["name"], 
					colour=discord.Colour(0x5dd3fa), 
					description= stripped_desc_text)
				
			embed.set_thumbnail(url=selection[sl_item]["image"])
			embed.add_field(name="Type", value= selection[sl_item]["type"])
			
			if selection[sl_item]["effect"] != "":
				embed.add_field(name="Effect", value = selection[sl_item]["effect"])

			if selection[sl_item]["weapon_type"] != "" and selection[sl_item]["weapon_type"] is not None:
				embed.add_field(name="Weapon Type", value = selection[sl_item]["weapon_type"])

			embed.add_field(name="Market Value", value = "$" + str("{:,.0f}".format(selection[sl_item]["market_value"])))
			
			if selection[sl_item]["name"] in fc_list:
				footer_text = "Item also available abroad from:"
				for loc in sorted(fc_list[selection[sl_item]["name"]]):
					footer_text = footer_text + "\n" + loc + " (" 
					footer_text = footer_text + str(fc_list[selection[sl_item]["name"]][loc]["quantity"]) 
					footer_text = footer_text + " @ $" + str("{:,.0f}".format(fc_list[selection[sl_item]["name"]][loc]["cost"])) + ")"
					footer_text = footer_text + " - Last updated: " + datetime.utcfromtimestamp(fc_list[selection[sl_item]["name"]][loc]["update"]).strftime("%H:%M")
			embed.set_footer(text=footer_text)

			await ctx.send(embed=embed)

		if len(short_list) > 0:

			footer_text = ""
			some_fc = False
			response = "Partial matches for search text (*{0}*).".format(item_name)
			await ctx.send(response)

			response = ">>> ```"
			sortlist = sorted(short_list.items(), key=lambda x:x[1])
			sortdict = dict(sortlist)


			for sl_item in sortdict:

				response = response  + "\n[" + str(sl_item) + "] " + sortdict[sl_item]      
				if sortdict[sl_item] in fc_list:
					response = response + "*"
					some_fc = True
			if some_fc:
				response = response + "\n\n(*Stock sold abroad)"
			
			response = (response + "```")
			await ctx.send(response)

	
	else:
		footer_text = ""
		if len(short_list) == 0:

			response = "Nothing matching your search text (*{0}*).".format(item_name)
			await ctx.send(response)
		

		## one match (not exact)
		elif len(short_list) == 1:
			footer_text = ""
			response = "Single match for your search text (*{0}*).".format(item_name)
			await ctx.send(response)

			for sl_item in short_list:

				desc_text = selection[sl_item]["description"]
				stripped_desc_text = strip_tags(desc_text)
	
				embed = discord.Embed(title="[" + str(sl_item) + "] " + selection[sl_item]["name"], 
						colour=discord.Colour(0x5dd3fa), 
						description= stripped_desc_text)
					
				embed.set_thumbnail(url=selection[sl_item]["image"])
				embed.add_field(name="Type", value= selection[sl_item]["type"])
				
				if selection[sl_item]["effect"] != "":
					embed.add_field(name="Effect", value = selection[sl_item]["effect"])

				if selection[sl_item]["weapon_type"] != "" and selection[sl_item]["weapon_type"] is not None:
					embed.add_field(name="Weapon Type", value = selection[sl_item]["weapon_type"])

				embed.add_field(name="Market Value", value = "$" + str("{:,.0f}".format(selection[sl_item]["market_value"])))

				if selection[sl_item]["name"] in fc_list:
					footer_text = "Item also available abroad from:"
					for loc in fc_list[selection[sl_item]["name"]]:
						footer_text = footer_text + "\n" + loc + " (" 
						footer_text = footer_text + str(fc_list[selection[sl_item]["name"]][loc]["quantity"]) 
						footer_text = footer_text + " @ $" + str("{:,.0f}".format(fc_list[selection[sl_item]["name"]][loc]["cost"])) + ")"
						footer_text = footer_text + " - Last updated: " + datetime.utcfromtimestamp(fc_list[selection[sl_item]["name"]][loc]["update"]).strftime("%H:%M")
				embed.set_footer(text=footer_text)

				await ctx.send(embed=embed)

		## more than 1 match (not exact)
		else:
			
			response = "List of matches for your search text (*{0}*).".format(item_name)
			await ctx.send(response)

			some_fc = False
			response = ">>> ```"
			#for sl_item in sorted(short_list):

			sortlist = sorted(short_list.items(), key=lambda x:x[1])
			sortdict = dict(sortlist)


			for sl_item in sortdict:

				response = response  + "\n[" + str(sl_item) + "] " + sortdict[sl_item]      
				if sortdict[sl_item] in fc_list:
					response = response + "*"
					some_fc = True

			if some_fc:
				response = response + "\n\n(*Stock sold abroad)"
			response = (response + "```")
			await ctx.send(response)
			
	return



@bot.command(name='itemid', help='Responds with data for item id provided')
async def itemid(ctx, item_id):
	v_apiID = item_id
	APIURL = bot.v_apiAddress+v_apiType+'/'+v_apiID+'?selections='+v_apiSelection+'&key='+bot.v_apiKey
	response = APIURL
	await ctx.send(response)

	r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	data = r.json() # translates that response into a dict variable
	selection = data["items"]
	v1 = selection[v_apiID]
	v_name = v1["name"]
	v_description = v1["description"]
	response = v_name + ": " + v_description
	await ctx.send(response)
	


@bot.command(name='removeid', aliases = ["remid"], hidden = True)
async def removeid(ctx, tornid:int):
	member = ctx.author
	discord_id = str(member.id)
	discord_name = member.name
	discord_member = str(member)
	discord_display_name = member.display_name
	discord_avatar_url = str(member.avatar_url)
	torn_id = tornid
	torn_api = ""

	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			#dict = eval(inf.read())
			dict = json.load(inf)
		if discord_id in dict:
			response = "Torn ID Updated"
			dict[discord_id].update({'torn_id' : str(torn_id)})
		else:
			response = "Torn ID Added"
			dict[discord_id] = {'torn_id' : str(torn_id)}
	else:
		dict = {discord_id: {'torn_id' : str(torn_id)}}
		response = "torn id added (new file)"

	with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)

	await ctx.send(response)




@bot.command(name='checkuser', aliases = ["chk", "ch", "cu"], help='Check on user setup')
async def checkuser(ctx, member: typing.Union[discord.Member,str] = "NA"):
		
	red_col = discord.Colour(0xe74c3c)
	blue_col = discord.Colour(0x5dd3fa)
	green_col = discord.Colour(0x2ecc71)
	emb_colour = red_col


	if member == "NA":
		member = ctx.author
	
	if type(member) == discord.Member:

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				dict = json.load(inf)
			
			description = "**Torn ID**" + "\n"


			if str(member.id) not in dict:
				description = description + member.display_name + " has not been setup with Ocker yet."
			else:
				torn_id = dict[str(member.id)].get("torn_id","missing")
				user_api = dict[str(member.id)].get("torn_api","missing")
				
				if torn_id == "missing":
					description = description + member.display_name + " has not been setup with Ocker yet."
				else:

					user_name = get_user_name_from_id(torn_id)

					if "error" in user_name:
						description = description + "Discord user " + member.display_name + " is associated with an invalid torn user ID " + str(torn_id) + "\n"
										
					else:
						description = description + "Discord user " + member.display_name + " is associated with torn user [" + user_name + " [" + str(torn_id) + "]](https://www.torn.com/profiles.php?XID="+str(torn_id) + ")" + "\n"
	
						description = description + "\n" + "**Torn API**" + "\n"
						if user_api == "missing":
							description = description + member.display_name + " has not added their API to Ocker yet." + "\n"
							emb_colour = blue_col
							
						else:
							v_apiType = "user"
							v_apiSelection = "bars"
					
							APIURL = bot.v_apiAddress+v_apiType+"/"+str(torn_id)+'?selections='+v_apiSelection+'&key='+ user_api
							r = requests.get(APIURL) # queries "apiurl" and returns `response from Torn
							v1 = r.json() # translates that response into a dict variable
							if "error" in v1:

								description = description + "The API for " + member.display_name + " is generating an error - if user changed API in torn it needs to be updated with Ocker." + "\n"
								emb_colour = blue_col
							else:
								description = description + "API is valid for discord user " + member.display_name + "\n"
								emb_colour = green_col
				
			embed = discord.Embed(title="Checking Discord User setup with Ocker", 
				colour=emb_colour, 
				description=description)
			await ctx.send(embed=embed)
			return
				
		else:
			await ctx.send("There is a problem with the file - speak to @Accy")
			return
		
	elif type(member) == str:
		await ctx.send("I am not sure what you mean by **" + member + "**.  Valid parameters are discord name (e.g. @Accy) or blank for your own account")
		return

	else:
		await ctx.send("Something weird")
		return


	return



@bot.command(name='addid', help='Register your Torn ID for bot commands')
async def addid(ctx, tornid:int):
	member = ctx.author
	discord_id = str(member.id)
	discord_name = member.name
	discord_member = str(member)
	discord_display_name = member.display_name
	discord_avatar_url = str(member.avatar_url)
	torn_id = tornid
	torn_api = ""

	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			#dict = eval(inf.read())
			dict = json.load(inf)
		if discord_id in dict:
			response = "Torn ID Updated"
			dict[discord_id].update({'torn_id' : str(torn_id)})
		else:
			response = "Torn ID Added"
			dict[discord_id] = {'torn_id' : str(torn_id)}
	else:
		dict = {discord_id: {'torn_id' : str(torn_id)}}
		response = "torn id added (new file)"

	with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)

	await ctx.send(response)


@bot.command(name='addapi', help='DM Ocker for this command.  Register your Torn API for bot commands.  Requires Torn ID registered first')
async def addapi(ctx, tornapi="NA"):

	if str(ctx.message.channel.type) != "private":
		await ctx.message.delete()
		await ctx.send("Please DM Ocker with !addapi KEY")
		return
	elif tornapi == "NA":
		await ctx.send("Please provide an API key.")
		return
	else:
		await ctx.send("Adding api code ........")
	
		member = ctx.author
		discord_id = str(member.id)
		torn_id = ""
		torn_api = tornapi

		if os.path.isfile("./users.json"):
			with open("./users.json","r") as inf:
				#dict = eval(inf.read())
				dict = json.load(inf)
			if discord_id in dict:
				response = "Torn API Added/Updated"
				dict[discord_id].update({'torn_api' : torn_api})
			else:
				raise NoDiscordID("no discord")
		else:
			raise NoFile("no api")

		with open("./users.json", "w") as data_file:
					json.dump(dict, data_file, indent=2)

		await ctx.send(response)
		return



#not in use
@bot.command(name='lock_eta', hidden = True)
async def lock_eta(ctx):
	member = ctx.author
	discord_id = str(member.id)
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			#dict = eval(inf.read())
			dict = json.load(inf)
		if discord_id in dict:
			response = "ETA Locked"
			dict[discord_id].update({'eta_lock':True})
			
			#json1 = json.dumps(dict)
			#f = open("./users.json","w")
			#f.write(json1)
			#f.close()

			with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)
		else:
			response = "Please add your torn ID first (!addid) and your torn API (!addapi)"
	else:
		response = "Please add your torn ID first (!addid) and your torn API (!addapi) - no file"
	await ctx.send(response)
	return




#not in use
@bot.command(name='unlock_eta', hidden = True)
async def unlock_eta(ctx):
	member = ctx.author
	discord_id = str(member.id)
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)
		if discord_id in dict:
			response = "ETA Unlocked"
			dict[discord_id].update({'eta_lock':False})
			
			with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)
		else:
			response = "Please add your torn ID first (!addid) and your torn API (!addapi)"
	else:
		response = "Please add your torn ID first (!addid) and your torn API (!addapi) - no file"
	await ctx.send(response)
	return

#not in use
@bot.command(name='lock_stats', hidden = True)
async def lock_stats(ctx):
	member = ctx.author
	discord_id = str(member.id)
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)
		if discord_id in dict:
			response = "Stats Locked"
			dict[discord_id].update({'stats_lock':True})
			
			with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)
		else:
			response = "Please add your torn ID first (!addid) and your torn API (!addapi)"
	else:
		response = "Please add your torn ID first (!addid) and your torn API (!addapi) - no file"
	await ctx.send(response)
	return

#not in use
@bot.command(name='unlock_stats', hidden = True)
async def unlock_stats(ctx):
	member = ctx.author
	discord_id = str(member.id)
	if os.path.isfile("./users.json"):
		with open("./users.json","r") as inf:
			dict = json.load(inf)
		if discord_id in dict:
			response = "Stats Unlocked"
			dict[discord_id].update({'eta_lock':False})
			
			with open("./users.json", "w") as data_file:
				json.dump(dict, data_file, indent=2)
		else:
			response = "Please add your torn ID first (!addid) and your torn API (!addapi)"
	else:
		response = "Please add your torn ID first (!addid) and your torn API (!addapi) - no file"
	await ctx.send(response)
	return



@bot.command(name='eta', help='Responds with users ETA for travel, hospital or jail.  Requires Torn ID and Torn API registered')
async def eta(ctx, member: discord.Member = "NA"):


	if member == "NA":
		member = ctx.author

	torn_id = await get_user_data(member, "torn_id")

	embed = await eta_work(torn_id)

	await ctx.send(embed=embed)


async def eta_work(torn_id):

	v_apiSelection = "travel"
	v_apiType = "user"

	torn_api = await get_user_data_from_id(torn_id, "torn_api")
	discord_id = await get_user_data_from_id(torn_id, "disco_id")
	if "ERROR" in discord_id:
		return("ERROR: No user")
#	print("eta_work: discord_id: " + discord_id)

	member = bot.get_user(int(discord_id))


	APIURL = bot.v_apiAddress+v_apiType+'/'+str(torn_id)+'?selections='+'profile'+'&key='+torn_api
	s = requests.get(APIURL) # queries "apiurl" and returns response from Torn
	s1 = s.json() # translates that response into a dict variable
	if "error" in s1:
		return("ERROR: There is an issue with the api key")
					
	s2 = s1['status']
	state = s2['state']
	description = s2['description']
	details = s2['details']
	until = s2['until']
	now = datetime.now()

	if state == 'Hospital':
		if 'href' in details:
		
			action = re.search('(.*?)(?=\<)',details).group()
			player_name = re.search('(?<=\>)(.*?)(?=\<)',details).group()
			player_link = re.search('(?<=\")(.*?)(?=\")',details).group()
			full_text = action + "[" + player_name + "](" + player_link + ")"
			#full_text = details
		
		else:
			full_text = details
		
		embed = discord.Embed(title=":hospital: In Hospital", 
			colour=discord.Colour(0xff0000), 
			url="https://www.torn.com/profiles.php?XID="+str(torn_id), 
			description=description)
		embed.set_thumbnail(url=	member.avatar_url)
		embed.add_field(name="Event", value=full_text)
		embed.add_field(name="Release time", value=(datetime.utcfromtimestamp(until).strftime("%H:%M"))) #datetime.utcnow().strftime("%H:%M:%S %d %B %Y")
		#await ctx.send(embed=embed)
		return(embed)


	if state == 'Abroad':

		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			return("ERROR: There is an issue with the api key")

		traveldata = v1['travel']

		destination = traveldata['destination']
		timestamp = traveldata['timestamp']
		departed = traveldata['departed']
		secondsleft = traveldata["time_left"]

		embed = discord.Embed(title=":beach: Landed in " + description, 
		colour=discord.Colour(0xFFA500), 
		url="https://www.torn.com/profiles.php?XID="+str(torn_id))
		embed.set_thumbnail(url=	member.avatar_url)
		embed.add_field(name="Arrived: ", value=datetime.utcfromtimestamp(timestamp).strftime("%H:%M"))
	
		#await ctx.send(embed=embed)
		return(embed)

	if state == 'Traveling':
		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			return("ERROR: There is an issue with the api key")

		traveldata = v1['travel']

		destination = traveldata['destination']
		timestamp = traveldata['timestamp']
		departed = traveldata['departed']
		secondsleft = traveldata["time_left"]
		arrival = datetime.utcnow() + timedelta(seconds=int(secondsleft))
		timefromnow = arrival - datetime.utcnow()

		arrival_days = divmod(secondsleft, 86400)        # Get days (without [0]!)
		arrival_hours = divmod(arrival_days[1], 3600)               # Use remainder of days to calc hours
		arrival_minutes = divmod(arrival_hours[1], 60)                # Use remainder of hours to calc minutes
		arrival_seconds = divmod(arrival_minutes[1], 1)               # Use remainder of minutes to calc seconds

		arrival_text = "("
		if arrival_days[0] > 0:
			if arrival_days[0] == 1:
				arrival_text = arrival_text + str(arrival_days[0]) + " Day "
			else:
				arrival_text = arrival_text + str(arrival_days[0]) + " Days "
		if arrival_hours[0] > 0:
			if arrival_hours[0] == 1:
				arrival_text = arrival_text + str(arrival_hours[0]) + " Hour "
			else:
				arrival_text = arrival_text + str(arrival_hours[0]) + " Hours "
		if arrival_minutes[0] > 0:
			if arrival_minutes[0] == 1:
				arrival_text = arrival_text + str(arrival_minutes[0	]) + " Minute"
			else:
				arrival_text = arrival_text + str(arrival_minutes[0	]) + " Minutes"
		arrival_text = arrival_text + ")"
		if arrival_text == "()":
			arrival_text = "(imminent)"

		embed = discord.Embed(title=":airplane: " + description, 
		colour=discord.Colour(0x5dd3fa), 
		url="https://www.torn.com/profiles.php?XID="+str(torn_id))
		embed.set_thumbnail(url=	member.avatar_url)
		embed.add_field(name="Estimate Arrival", value=datetime.utcfromtimestamp(timestamp).strftime("%H:%M") + " " + arrival_text)
								
		#await ctx.send(embed=embed)
		return(embed)



	if state == 'Okay':

		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			return("ERROR: There is an issue with the api key")


		traveldata = v1['travel']

		destination = traveldata['destination']
		timestamp = traveldata['timestamp']
		departed = traveldata['departed']
		secondsleft = traveldata["time_left"]

		embed = discord.Embed(title=":house: Landed in Torn", 
		colour=discord.Colour(0x46FF33), 
		url="https://www.torn.com/profiles.php?XID="+str(torn_id))
		embed.set_thumbnail(url=	member.avatar_url)
		embed.add_field(name="Arrived in Torn", value=datetime.utcfromtimestamp(timestamp).strftime("%H:%M"))
	
		#await ctx.send(embed=embed)
		return(embed)

	if state == 'Jail':

		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			return("ERROR: There is an issue with the api key")

		state = s2['state']
		description = s2['description']
		details = s2['details']

		embed = discord.Embed(title=":woman_police_officer: In Jail", 
		colour=discord.Colour(0xff0000), 
		url="https://www.torn.com/profiles.php?XID="+str(torn_id),
		description = description)
		embed.set_thumbnail(url=	member.avatar_url)
		embed.add_field(name="details", value=details)

		#await ctx.send(embed=embed)
		return(embed)
	
	return
	


def getdictfromfile(dictfile):
	if os.path.isfile("./" + dictfile):
		with open("./" + dictfile,"r") as inf:
			dict = json.load(inf)
	else:
		dict = {"Error": "Cannot find file: " + dictfile}
	response = dict
	return(response)


@bot.command(name='workstats', aliases=['ws'], help='Responds with Work Stats.  Requires Torn ID and Torn API registered.')
async def workstats(ctx, member: discord.Member = "NA"):
	readonly = True
	countstattype = 0
	now = datetime.now()

	if member == "NA":
		member = ctx.author
	if member == ctx.author:
		readonly = False

	
	discord_id = str(member.id)
	torn_id = ""
	torn_api = ""

	v_apiSelection = "workstats"
	v_apiType = "user"


	if readonly:
		if os.path.isfile("./workstats.json"):
			with open("./workstats.json","r") as inf:
				#statdict = eval(inf.read())
				statdict = json.load(inf)

			if discord_id in statdict:

				v_ro_manuallabor  = statdict[discord_id]["manuallabor"]
				v_ro_intelligence = statdict[discord_id]["intelligence"]
				v_ro_endurance    = statdict[discord_id]["endurance"]
				v_ro_timestamp    = statdict[discord_id]["timestamp"]
				torntime          = datetime.utcfromtimestamp(v_ro_timestamp).strftime("%H:%M:%S %d %B %Y")

				maxl = 15
				maxe = 16 + maxl
				response = (">>> ```" +
					"\n" + ("{:<16s}").format("Manual Labor:")     + ("{:"+str(maxl)+",d}").format(v_ro_manuallabor)      +
					"\n" + ("{:<16s}").format("Intelligence:")     + ("{:"+str(maxl)+",d}").format(v_ro_intelligence)     +
					"\n" + ("{:<16s}").format("Endurance:")        + ("{:"+str(maxl)+",d}").format(v_ro_endurance)        +
					"```")
				await ctx.send(response)
				response = (">>> ```" +
					"\n" + "This is the stored work stats for this user" +
					"\n" + "Last updated: " + torntime + "```")
				
				await ctx.send(response)
				return
			else:
				response = "No stored work stats for this user"
				await ctx.send(response)
				return
		else:
			#no file but we don't care - just returning no stats for user
			response = "No stored work stats for this user"
			await ctx.send(response)
			return
	else:

		torn_id = await get_user_data(member,"torn_id")
		torn_api = await get_user_data(member, "torn_api")
		timestamp = datetime.timestamp(now)

		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise APIIssue("workstats")
		else:
			v_manuallabor = v1["manual_labor"]
			v_intelligence = v1["intelligence"]
			v_endurance = v1["endurance"]
			maxl = 15
			maxe = 16 + maxl
			response = (">>> ```" +
				"\n" + ("{:<16s}").format("Manual Labor:")  + ("{:"+str(maxl)+",d}").format(v_manuallabor)  +
				"\n" + ("{:<16s}").format("Intelligence:")  + ("{:"+str(maxl)+",d}").format(v_intelligence) +
				"\n" + ("{:<16s}").format("Endurance:") 	+ ("{:"+str(maxl)+",d}").format(v_endurance) 	+
				"```")
			await ctx.send(response)
			if os.path.isfile("./workstats.json"):
				with open("./workstats.json","r") as inf:
					#statdict = eval(inf.read())
					statdict = json.load(inf)

				if discord_id in statdict:


					v_old_manuallabor  = statdict[discord_id]["manuallabor"]
					v_old_intelligence = statdict[discord_id]["intelligence"]
					v_old_endurance    = statdict[discord_id]["endurance"]
					v_old_timestamp    = statdict[discord_id]["timestamp"]
					torntime           = datetime.utcfromtimestamp(v_old_timestamp).strftime("%H:%M:%S %d %B %Y")


					v_diff_manuallabor  = int(v_manuallabor)  - int(v_old_manuallabor)
					v_diff_intelligence = int(v_intelligence) - int(v_old_intelligence)
					v_diff_endurance    = int(v_endurance)    - int(v_old_endurance)
					
					v_diff_manuallabor_pc  = v_diff_manuallabor  / v_old_manuallabor
					v_diff_intelligence_pc = v_diff_intelligence / v_old_intelligence
					v_diff_endurance_pc    = v_diff_endurance    / v_old_endurance
					v_diff_total           = v_diff_manuallabor + v_diff_intelligence + v_diff_endurance

					
					if v_diff_total == 0:
						response = "> ```No change since last update (" + torntime + ")```"
						await ctx.send(response)
						return
					else:
						response = ">>> ```"
						if v_diff_manuallabor > 0:
							countstattype = countstattype + 1
							response = response + "\n" + "Manual Labor increased by " + "{:,d}".format(v_diff_manuallabor) + " points (" + "{:.2%}".format(v_diff_manuallabor_pc) + ")"
						if v_diff_intelligence > 0:
							countstattype = countstattype + 1
							response = response + "\n" +"Intelligence increased by " + "{:,d}".format(v_diff_intelligence) + " points (" + "{:.2%}".format(v_diff_intelligence_pc) + ")"
						if v_diff_endurance > 0:
							countstattype = countstattype + 1
							response = response + "\n" + "Endurance increased by " + "{:,d}".format(v_diff_endurance) + " points (" + "{:.2%}".format(v_diff_endurance_pc) + ")"
							
						response = response + "\n" + "Last updated: " + torntime + "```"
						await ctx.send(response)
				
					#user exists so we update
					statdict[discord_id].update({'manuallabor' : v_manuallabor, 'intelligence' : v_intelligence, 'endurance' : v_endurance, 'timestamp' : timestamp})
				else:
					#user doesn't exist so we create user
					statdict[discord_id] = {'manuallabor' : v_manuallabor, 'intelligence' : v_intelligence, 'endurance' : v_endurance, 'timestamp' : timestamp}
			else:
				#file doesn't exist so we create it
				statdict = {discord_id: {'manuallabor' : v_manuallabor, 'intelligence' : v_intelligence, 'endurance' : v_endurance, 'timestamp' : timestamp}}
				
			with open("./workstats.json", "w") as data_file:
				json.dump(statdict, data_file, indent=2)
			
			#json1 = json.dumps(statdict)
			#f = open("./workstats.json","w")
			#f.write(json1)
			#f.close()

			response = "Work Stats updated!"
			await ctx.send(response)

	return

@bot.command(name='stats', aliases=['s'], help='Responds with Stats. Requires Torn ID and Torn API registered.')
async def stats(ctx, member: discord.Member = "NA"):
	readonly = True
	countstattype = 0
	now = datetime.now()

	
	
	if member == "NA":
		member = ctx.author
	if member == ctx.author:
		readonly = False

	
	discord_id = str(member.id)
	torn_id = ""
	torn_api = ""

	v_apiSelection = "battlestats"
	v_apiType = "user"


	if readonly:
		if os.path.isfile("./stats.json"):
			with open("./stats.json","r") as inf:
				#statdict = eval(inf.read())
				statdict = json.load(inf)

			if discord_id in statdict:

				v_ro_strength = statdict[discord_id]["strength"]
				v_ro_speed = statdict[discord_id]["speed"]
				v_ro_dexterity = statdict[discord_id]["dexterity"]
				v_ro_defense = statdict[discord_id]["defense"]
				v_ro_total = statdict[discord_id]["total"]
				v_ro_timestamp = statdict[discord_id]["timestamp"]
				torntime = datetime.utcfromtimestamp(v_ro_timestamp).strftime("%H:%M:%S %d %B %Y")

				maxl = len(format(v_ro_total,',d')) + 15
				maxe = 16 + maxl
				response = (">>> ```" +
					"\n" + ("{:<16s}").format("Strength:")  + ("{:"+str(maxl)+",d}").format(v_ro_strength)  +
					"\n" + ("{:<16s}").format("Speed:")     + ("{:"+str(maxl)+",d}").format(v_ro_speed)     +
					"\n" + ("{:<16s}").format("Dexterity:") + ("{:"+str(maxl)+",d}").format(v_ro_dexterity) +
					"\n" + ("{:<16s}").format("Defense:")   + ("{:"+str(maxl)+",d}").format(v_ro_defense)   +
					"\n" + "=" * maxe +
					"\n" + ("{:<16s}").format("Total:")   + ("{:"+str(maxl)+",d}").format(v_ro_total)       +
					"```")
				await ctx.send(response)
				response = (">>> ```" +
					"\n" + "This is the stored stats for this user" +
					"\n" + "Last updated: " + torntime + "```")
				
				await ctx.send(response)
				return
			else:
				response = "No stored stats for this user"
				await ctx.send(response)
				return
		else:
			#file is missing - we don't care
			response = "No stored stats for this user"
			await ctx.send(response)
			return
	else:

		torn_id = await get_user_data(member, "torn_id")
		torn_api = await get_user_data(member, "torn_api")
		timestamp = datetime.timestamp(now)

		APIURL = bot.v_apiAddress+v_apiType+'/'+'?selections='+v_apiSelection+'&key='+torn_api
		r = requests.get(APIURL) # queries "apiurl" and returns response from Torn
		v1 = r.json() # translates that response into a dict variable
		if "error" in v1:
			raise APIIssue("stats")
		else:
			v_strength = v1["strength"]
			v_speed = v1["speed"]
			v_dexterity = v1["dexterity"]
			v_defense = v1["defense"]
			v_total = v1["total"]
			maxl = len(format(v_total,',d')) + 15
			maxe = 16 + maxl
			response = (">>> ```" +
				"\n" + ("{:<16s}").format("Strength:")  + ("{:"+str(maxl)+",d}").format(v_strength)  +
				"\n" + ("{:<16s}").format("Speed:")     + ("{:"+str(maxl)+",d}").format(v_speed)     +
				"\n" + ("{:<16s}").format("Dexterity:") + ("{:"+str(maxl)+",d}").format(v_dexterity) +
				"\n" + ("{:<16s}").format("Defense:")   + ("{:"+str(maxl)+",d}").format(v_defense)   +
				"\n" + "=" * maxe +
				"\n" + ("{:<16s}").format("Total:")   + ("{:"+str(maxl)+",d}").format(v_total)       +
				"```")
			await ctx.send(response)
			if os.path.isfile("./stats.json"):
				with open("./stats.json","r") as inf:
					#statdict = eval(inf.read())
					statdict = json.load(inf)

				if discord_id in statdict:


					v_old_strength = statdict[discord_id]["strength"]
					v_old_speed = statdict[discord_id]["speed"]
					v_old_dexterity = statdict[discord_id]["dexterity"]
					v_old_defense = statdict[discord_id]["defense"]
					v_old_total = statdict[discord_id]["total"]
					v_old_timestamp = statdict[discord_id]["timestamp"]
					v_old_timestamp = statdict[discord_id]["timestamp"]
					torntime = datetime.utcfromtimestamp(v_old_timestamp).strftime("%H:%M:%S %d %B %Y")


					v_diff_strength = int(v_strength) - int(v_old_strength)
					v_diff_speed = int(v_speed) - int(v_old_speed)
					v_diff_dexterity = int(v_dexterity) - int(v_old_dexterity)
					v_diff_defense = int(v_defense) - int(v_old_defense)
					v_diff_total = int(v_total) - int(v_old_total)

					v_diff_strength_pc = v_diff_strength / v_old_strength
					v_diff_speed_pc = v_diff_speed / v_old_speed
					v_diff_dexterity_pc = v_diff_dexterity / v_old_dexterity
					v_diff_defense_pc = v_diff_defense / v_old_defense
					v_diff_total_pc = v_diff_total / v_old_total


					
					if v_diff_total == 0:
						response = "> ```No change since last update (" + torntime + ")```"
						await ctx.send(response)
						return
					else:
						response = ">>> ```"
						if v_diff_strength > 0:
							countstattype = countstattype + 1
							response = response + "\n" + "Strength increased by " + "{:,d}".format(v_diff_strength) + " points (" + "{:.2%}".format(v_diff_strength_pc) + ")"
						if v_diff_speed > 0:
							countstattype = countstattype + 1
							response = response + "\n" +"Speed increased by " + "{:,d}".format(v_diff_speed) + " points (" + "{:.2%}".format(v_diff_speed_pc) + ")"
						if v_diff_dexterity > 0:
							countstattype = countstattype + 1
							response = response + "\n" + "Dexterity increased by " + "{:,d}".format(v_diff_dexterity) + " points (" + "{:.2%}".format(v_diff_dexterity_pc) + ")"
						if v_diff_defense > 0:
							countstattype = countstattype + 1
							response = response + "\n" +"Defense increased by " + "{:,d}".format(v_diff_defense) + " points (" + "{:.2%}".format(v_diff_defense_pc) + ")"
						if v_diff_total > 0:
							if countstattype > 1:
								response = response + "\n" +"Total increased by " + "{:,d}".format(v_diff_total) + " points (" + "{:.2%}".format(v_diff_total_pc) + ")"
							
						response = response + "\n" + "Last updated: " + torntime + "```"
						await ctx.send(response)
				



					statdict[discord_id].update({'strength' : v_strength, 'speed' : v_speed, 'dexterity' : v_dexterity, 'defense' : v_defense, 'total' : v_total, 'timestamp' : timestamp})
				else:
					statdict[discord_id] = {'strength' : v_strength, 'speed' : v_speed, 'dexterity' : v_dexterity, 'defense' : v_defense, 'total' : v_total, 'timestamp' : timestamp}
			else:
				statdict = {discord_id: {'strength' : v_strength, 'speed' : v_speed, 'dexterity' : v_dexterity, 'defense' : v_defense, 'total' : v_total, 'timestamp' : timestamp}}
				
			with open("./stats.json", "w") as data_file:
				json.dump(statdict, data_file, indent=2)

			#json1 = json.dumps(statdict)
			#f = open("./stats.json","w")
			#f.write(json1)
			#f.close()

			response = "Stats updated!"
			await ctx.send(response)

	return


bot.run(TOKEN)
