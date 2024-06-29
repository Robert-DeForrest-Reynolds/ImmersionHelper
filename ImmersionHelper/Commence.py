from discord import Game as DiscordGame
from discord import Intents
from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from discord import Interaction, Member
from discord.ext.commands import Bot, Context
from sys import argv
from Panels.Panel import Panel
from Player import Player
from Creator import Creator

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


	async def Save_Character(Self, Username, GivenCharacter):...


	async def Save_Object(Self, Username, GivenObject):...


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


@IH.Bot.command(aliases=["ih"])
async def Main_Event(InitialContext:Context) -> None:
	User = InitialContext.message.author
	Panel(InitialContext, User, IH)


IH.Bot.run(IH.Token)