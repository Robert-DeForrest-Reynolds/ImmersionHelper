from discord import Interaction, Member, Embed
from discord.ui import View, Button
from Player import Player
from asyncio import create_task
from Game import Game

class GamePanel:
	def __init__(Self, Interaction:Interaction, User:Member, ImmersionHelperReference, HomePanel):
		Self.User = User
		Self.ImmersionHelper = ImmersionHelperReference
		Self.HomePanel = HomePanel
		Self.Player:Player = Self.ImmersionHelper.Players[User.name]
		create_task(Self.Send_Game_Panel(Interaction))


	async def Create_Game(Self, Interaction):
		NewGame = Game()


	async def Send_Game_Panel(Self, Interaction:Interaction):
		GameView = View(timeout=144000)
		GameEmbed = Embed(title="Games")

		CreateGameButton = Button(label="Create Game", row=1)
		CreateGameButton.callback = lambda Interaction: Self.Create_Game(Interaction)
		GameView.add_item(CreateGameButton)

		HomeButton = Button(label="Home", row=4)
		HomeButton.callback = lambda Interaction: Self.HomePanel.Send_Panel(Interaction)
		GameView.add_item(HomeButton)

		await Interaction.response.edit_message(view=GameView, embed=GameEmbed)