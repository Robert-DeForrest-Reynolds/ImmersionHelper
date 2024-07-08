from discord import Embed, Member
from discord.ui import Button, View, Modal, TextInput
from discord.ext.commands import Context
from asyncio import create_task
from Character import Character
from Player import Player
from Panels.GamePanel import GamePanel
from Panels.CharacterPanel import CharacterPanel

class Panel:
	def __init__(Self, Context:Context, User:Member, ImmersionHelperReference):
		Self.User = User
		Self.ImmersionHelper = ImmersionHelperReference
		Self.Player:Player = Self.ImmersionHelper.Players[User.name]
		create_task(Self.Send_Panel(Context))


	async def Send_Panel(Self, Context:Context):
		PanelView = View(timeout=144000)
		PanelEmbed = Embed(title="Welcome to Immersion Helper!")

		print(Context)
		if Context.invoked_with == "help":
			PanelEmbed.add_field(name="\u200b", value="I'm helpful")

		print(Self.Player.Data["Name"])
		if Self.Player.Data["Name"] in Self.ImmersionHelper.Creators.keys():
			GamesButton = Button(label="Games", row=1)
			GamesButton.callback = lambda Context: Self.Send_Game_Panel(Context)
			PanelView.add_item(GamesButton)

		CharactersButton = Button(label="Characters", row=1)
		CharactersButton.callback = lambda Context: Self.Send_Character_Panel(Context)
		PanelView.add_item(CharactersButton)

		await Context.message.delete()
		await Context.channel.send(view=PanelView, embed=PanelEmbed)


	async def Send_Game_Panel(Self, Context): GamePanel(Context, Self.User, Self.ImmersionHelper, Self)


	async def Send_Character_Panel(Self, Context): CharacterPanel(Context, Self.User, Self.ImmersionHelper, Self)