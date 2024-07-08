from discord import Game as DiscordGame
from discord import Intents
from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from discord import Interaction, Member, Embed
from discord.ext.commands import Bot, Context
from sys import argv
from Panels.Panel import Panel
from Player import Player
from Character import Character
from Creator import Creator
from discord import Webhook
from os.path import exists, join, isdir, isfile
from os import mkdir, listdir

class ImmersionHelper:
	def __init__(Self) -> None:
		# Setup
		Self.Token = argv[1]
		intents = Intents.all()
		intents.message_content = True
		
		Self.Bot = Bot(command_prefix='.', intents=intents, help_command=None, description='description', case_insensitive=True)
		
		Self.CreatorNames = [
			"themaddm2",
			"robertdeforrest",
		]

		Self.Members = {}
		Self.Games = {}
		Self.Creators = {}
		Self.Players = {}

		# Logging
		getLogger('discord.http').setLevel(INFO)
		Self.ImmersionHelperLogger:Logger = getLogger('discord')
		Self.ImmersionHelperLogger.setLevel(DEBUG)
		Handler = RotatingFileHandler(
			filename='ImmersionHelper.log',
			encoding='utf-8',
			maxBytes=32 * 1024 * 1024,  # 32 MiB
			backupCount=5,  # Rotate through 5 files
		)
		DateTimeFormat = '%Y-%m-%d %H:%M:%S'
		ImmersionHelperFormatter = Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', DateTimeFormat, style='{')
		Handler.setFormatter(ImmersionHelperFormatter)
		Self.ImmersionHelperLogger.addHandler(Handler)
		Self.ImmersionHelperLogger.info("Logger is setup")

		
	async def Save_New_Creator(Self, Username):...


	async def Save_Game(Self, Username, GivenGame):...


	async def Save_Characters(Self, Username):
		P:Player = Self.Players[Username]
		CharacterData = ""
		for Character in P.Characters.values():
			CharacterData += "~".join([Value for Value in Character.Data.values()])
			if P.DefaultCharacter == Character.Data["Name"]:
				CharacterData += "~Default"
			CharacterData += "\n"
		with open(join("Data", Username, 'characters.txt'), 'w') as SaveFile:
			SaveFile.write(CharacterData)

	async def Save_Aliases(Self, Username):
		with open(join("Data", Username, 'aliases.txt'), 'w') as SaveFile:
			SaveFile.write("~".join([f'{Name}:{Object.Data["Name"]}' for Name, Object in Self.Players[Username].Aliases.items()]))

	async def Save_Object(Self, Username, GivenObject):...


	def Load_Characters(Self, PlayerName, CharactersData):
		for CharacterData in CharactersData:
			CharacterData = CharacterData.split("~")
			P:Player = Self.Players[PlayerName]
			LoadedCharacter = Character(CharacterData[0])
			if len(CharacterData) == 3:
				P.DefaultCharacter = LoadedCharacter.Data["Name"]
			P.Characters.update({LoadedCharacter.Data["Name"]:LoadedCharacter})


	def Load_Aliases(Self, PlayerName, AliasesData):
		Aliases = AliasesData.split("~")
		P:Player = Self.Players[PlayerName]
		for AliasData in Aliases:
			Data = AliasData.split(":")
			Alias = Data[0]
			ObjectName = Data[1]
			print(P.Characters)
			P.Aliases.update({Alias:P.Characters[ObjectName]})
			P.Characters[ObjectName].Alias = Alias

	def Load_Player_Data(Self):
		for PlayerDirectory in listdir("Data"):
			CharacterData = None
			AliasData = None
			if isfile(join("Data", PlayerDirectory)): continue
			for DataFile in listdir(join("Data", PlayerDirectory)):
				if DataFile == "characters.txt":
					with open(join("Data", PlayerDirectory, "characters.txt"), 'r') as DataFile:
						CharacterData = DataFile.readlines()
				if DataFile == "aliases.txt":
					with open(join("Data", PlayerDirectory, "aliases.txt"), 'r') as DataFile:
						AliasData = DataFile.readlines()[0]
			if CharacterData != None: Self.Load_Characters(PlayerDirectory, CharacterData)
			if AliasData != None: Self.Load_Aliases(PlayerDirectory, AliasData)


global IH
IH = ImmersionHelper()


@IH.Bot.event
async def on_ready() -> None:
	Message = f"{IH.Bot.user} has connected to Discord!"
	print(Message)
	IH.ImmersionHelperLogger.log(20, Message)
	await IH.Bot.change_presence(activity=DiscordGame('.ih'))

	for Guild in IH.Bot.guilds:
		for Member in Guild.members:
			if Member.name not in IH.Members.keys() and not Member.bot:
				IH.Members.update({Member.name:Member})
				IH.Players.update({Member.name:Player(Member)})
				
				if Member.name in IH.CreatorNames:
					IH.Creators.update({Member.name:Creator(Member)})
				if not exists(join("Data", Member.name)): mkdir(join("Data", Member.name))


	IH.Load_Player_Data()
	print(IH.Creators)


@IH.Bot.command(aliases=["ih", "help"])
async def Main_Event(InitialContext:Context, *Arguments) -> None:
	User = InitialContext.message.author
	if len(Arguments) > 0:
		if len(Arguments) == 1:
			if len(IH.Players[User.name].Characters) <= 0:
				await InitialContext.message.delete()
				await InitialContext.channel.send(content="You do not have any characters.")
			else:
				await InitialContext.message.delete()
				Webhook = await InitialContext.channel.create_webhook(name="DefaultCharacter")
				DefaultCharacter = IH.Players[User.name].Characters[IH.Players[User.name].DefaultCharacter]

				if DefaultCharacter.Data["Icon"] == "None": 
					await Webhook.send(str(Arguments[0]), username=DefaultCharacter.Data["Name"], avatar_url="https://static.wikia.nocookie.net/all-worlds-alliance/images/2/29/Hawk_anime_full_appearance_2.png/revision/latest?cb=20200309064015")
				else:
					await Webhook.send(str(Arguments[0]), username=DefaultCharacter.Data["Name"], avatar_url=DefaultCharacter.Data["Icon"])
		elif len(Arguments) == 2:
			print("I'm flagged dialogue")
			print(IH.Players[User.name].Aliases)
			print(Arguments[0])
			if Arguments[0] in IH.Players[User.name].Aliases.keys():
				UsedCharacter = IH.Players[User.name].Aliases[Arguments[0]]
				Webhook = await InitialContext.channel.create_webhook(name="Alias Character")
				await InitialContext.message.delete()

				if UsedCharacter.Data["Icon"] == "None": 
					await Webhook.send(str(Arguments[1]), username=UsedCharacter.Data["Name"], avatar_url="https://static.wikia.nocookie.net/all-worlds-alliance/images/2/29/Hawk_anime_full_appearance_2.png/revision/latest?cb=20200309064015")
				else:
					await Webhook.send(str(Arguments[1]), username=UsedCharacter.Data["Name"], avatar_url=UsedCharacter.Data["Icon"])

		Webhooks = await InitialContext.channel.webhooks()
		for W in Webhooks:
			await W.delete()
	else:
		Panel(InitialContext, User, IH)


IH.Bot.run(IH.Token)