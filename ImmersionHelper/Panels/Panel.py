from discord import Embed, Interaction, Member
from discord.ui import Button, View, Modal, TextInput
from asyncio import create_task
from Character import Character
from Player import Player
from Panels.GamePanel import GamePanel

class Panel:
	def __init__(Self, Interaction:Interaction, User:Member, ImmersionHelperReference):
		Self.User = User
		Self.ImmersionHelper = ImmersionHelperReference
		Self.Player:Player = Self.ImmersionHelper.Players[User.name]
		create_task(Self.Send_Panel(Interaction))

	async def Send_Panel(Self, Interaction:Interaction):
		PanelView = View(timeout=144000)
		PanelEmbed = Embed(title="Welcome to Immersion Helper!")

		# Row 0 is the Select for selecting which game you'll be interacting with
		# Row 0 is the Select for selecting which character you'll be interacting with
		# Row 2 is a ButtonRow
		# Row 3 i s a ButtonRow

		if Self.Player.Data["Name"] in Self.ImmersionHelper.Creators.keys():
			GamesButton = Button(label="Games", row=1)
			GamesButton.callback = lambda Interaction: Self.Send_Game_Panel(Interaction)
			PanelView.add_item(GamesButton)

		CharactersButton = Button(label="Characters", row=1)
		CharactersButton.callback = lambda Interaction: Self.Send_Character_Panel(Interaction)
		PanelView.add_item(CharactersButton)

		await Interaction.message.delete()
		await Interaction.channel.send(view=PanelView, embed=PanelEmbed)


	async def Send_Game_Panel(Self, Interaction): GamePanel(Interaction, Self.User, Self.ImmersionHelper, Self)


	async def Send_Character_Panel(Self, Interaction:Interaction):
		CharacterView = View(timeout=144000)
		CharacterEmbed = Embed(title="Characters")

		CreateCharacterButton = Button(label="Create Character", row=1)
		CreateCharacterButton.callback = lambda Interaction: Self.Character_Name_Modal(Interaction)
		CharacterView.add_item(CreateCharacterButton)

		HomeButton = Button(label="Home", row=4)
		HomeButton.callback = lambda Interaction: Self.Send_Panel(Interaction)
		CharacterView.add_item(HomeButton)

		await Interaction.response.edit_message(view=CharacterView, embed=CharacterEmbed)


	async def Character_Name_Modal(Self, Interaction:Interaction):
		NameModal = Modal(title="Character Name", timeout=300, custom_id="NameModal")
		NameModal.on_submit = lambda Interaction: Self.Create_Character(Interaction, NameInput.value)

		NameInput = TextInput(label="What is your character's name?")
		NameModal.add_item(NameInput)

		await Interaction.response.send_modal(NameModal)


	async def Create_Character(Self, Interaction:Interaction, Name):
		NewCharacter = Character(Name)
		Self.Player.Characters.update({Name:NewCharacter})

		NewCharacterView = View(timeout=144000)
		NewCharacterEmbed = Embed(title="You've created a new character!")

		CharacterDescription = "\n".join(f"{Key}:{Value}" for Key, Value in NewCharacter.Data.items())

		NewCharacterEmbed.add_field(name=Name, value=CharacterDescription)

		HomeButton = Button(label="Home", row=0)
		HomeButton.callback = lambda Interaction: Self.Send_Panel(Interaction)
		NewCharacterView.add_item(HomeButton)
		
		await Interaction.response.edit_message(view=NewCharacterView, embed=NewCharacterEmbed)