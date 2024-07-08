from discord import Embed, Member, SelectOption
from discord.ui import Button, View, Modal, TextInput, Select
from discord.ext.commands import Context
from asyncio import create_task
from Character import Character
from Player import Player


class CharacterPanel:
	def __init__(Self, Context:Context, User:Member, ImmersionHelperReference, HomePanel):
		Self.User = User
		Self.ImmersionHelper = ImmersionHelperReference
		Self.HomePanel = HomePanel
		Self.Player:Player = Self.ImmersionHelper.Players[User.name]
		Self.SelectedCharacter = None
		create_task(Self.Send_Character_Panel(Context))


	async def Send_Character_Panel(Self, Context:Context):
		CharacterView = View(timeout=144000)
		CharacterEmbed = Embed(title="Characters")
		CharacterDescription = ""

		if len(Self.Player.Characters.keys()) == 1:
			PlayerCharacter = [PlayerCharacter for PlayerCharacter in Self.Player.Characters.values()][0]
			CharacterEmbed = Embed(title="You've created a new character!")
			CharacterDescription = "\n".join(f"{Key}: {Value}" for Key, Value in PlayerCharacter.Data.items())
			CharacterEmbed.add_field(name=f'**PlayerCharacter.Data["Name"]**', value=CharacterDescription)

		if len(Self.Player.Characters.keys()) > 1:
			CharacterChoice = Select(placeholder="Select a Character",
									 options=[SelectOption(label=C) for C in Self.Player.Characters], # C = Characters
									 row=2,
									 custom_id=f"ActivityChoice")
			CharacterChoice.callback = lambda Context: Self.Select_Character(Context, Context.data["values"][0])
			CharacterView.add_item(CharacterChoice)
		
		if Self.SelectedCharacter != None:
			CharacterEmbed = Embed(title="You've created a new character!")
			if Self.Player.DefaultCharacter == Self.SelectedCharacter.Data["Name"]:
				CharacterDescription += "**Default**\n"
			if Self.SelectedCharacter.Alias != None:
				CharacterDescription += f"Alias:{Self.SelectedCharacter.Alias}\n"
			for Key, Value in Self.SelectedCharacter.Data.items():
				if Key not in ["Name"]:
					CharacterDescription += f"{Key}: {Value}\n"
			CharacterEmbed.add_field(name=Self.SelectedCharacter.Data["Name"], value=CharacterDescription)

			MakeDefaultButton = Button(label="Make default", row=1)
			MakeDefaultButton.callback = lambda Context: Self.Set_Character_Default(Context, Self.SelectedCharacter.Data["Name"])
			CharacterView.add_item(MakeDefaultButton)

			GiveAliasButton = Button(label="Set Alias", row=1)
			GiveAliasButton.callback = lambda Context: Self.Get_Alias(Context)
			CharacterView.add_item(GiveAliasButton)

			GiveIconButton = Button(label="Set Icon", row=1)
			GiveIconButton.callback = lambda Context: Self.Get_Icon_URL(Context)
			CharacterView.add_item(GiveIconButton)

		CreateCharacterButton = Button(label="Create Character", row=1)
		CreateCharacterButton.callback = lambda Context: Self.Character_Name_Modal(Context)
		CharacterView.add_item(CreateCharacterButton)

		HomeButton = Button(label="Home", row=4)
		HomeButton.callback = lambda Context: Self.HomePanel.Send_Panel(Context)
		CharacterView.add_item(HomeButton)

		await Context.message.edit(view=CharacterView, embed=CharacterEmbed)


	async def Get_Alias(Self, Context:Context):
		AliasModal = Modal(title="Character Alias", timeout=300, custom_id="AliasModal")
		AliasModal.on_submit = lambda Context: Self.Set_Alias(Context, AliasInput.value)

		AliasInput = TextInput(label=f"Enter alias for {Self.SelectedCharacter.Data['Name']}")
		AliasModal.add_item(AliasInput)

		await Context.response.send_modal(AliasModal)


	async def Get_Icon_URL(Self, Context:Context):
		IconURLModal = Modal(title="Character Alias", timeout=300, custom_id="URLModal")
		IconURLModal.on_submit = lambda Context: Self.Set_Icon_URL(Context, URLInput.value)

		URLInput = TextInput(label=f"Enter URL for {Self.SelectedCharacter.Data['Name']}'s icon")
		IconURLModal.add_item(URLInput)

		await Context.response.send_modal(IconURLModal)


	async def Set_Alias(Self, Context, Alias):
		Self.SelectedCharacter.Alias = Alias
		Self.Player.Aliases.update({Alias:Self.SelectedCharacter})
		await Self.ImmersionHelper.Save_Aliases(Self.Player.Data["Name"])
		print(Alias, Self.Player.Aliases)
		await Self.Send_Character_Panel(Context)


	async def Set_Icon_URL(Self, Context, URL):
		Self.SelectedCharacter.Data["Icon"] = URL
		await Self.ImmersionHelper.Save_Characters(Self.Player.Data["Name"])
		await Self.Send_Character_Panel(Context)


	async def Set_Character_Default(Self, Context, CharacterName):
		Self.Player.DefaultCharacter = CharacterName
		await Self.ImmersionHelper.Save_Characters(Self.Player.Data["Name"])
		await Self.Send_Character_Panel(Context)


	async def Select_Character(Self, Context, CharacterName):
		Self.SelectedCharacter = Self.Player.Characters[CharacterName]
		await Self.Send_Character_Panel(Context)


	async def Character_Name_Modal(Self, Context:Context):
		NameModal = Modal(title="Character Name", timeout=300, custom_id="NameModal")
		NameModal.on_submit = lambda Context: Self.Create_Character(Context, NameInput.value)

		NameInput = TextInput(label="What is your character's name?")
		NameModal.add_item(NameInput)

		await Context.response.send_modal(NameModal)


	async def Create_Character(Self, Context:Context, Name):
		NewCharacter = Character(Name)
		Self.Player.Characters.update({Name:NewCharacter})
		if len(Self.Player.Characters.keys()) == 1: Self.Player.DefaultCharacter = NewCharacter.Data["Name"]
		await Self.ImmersionHelper.Save_Characters(Self.Player.Data["Name"], NewCharacter)

		NewCharacterView = View(timeout=144000)
		NewCharacterEmbed = Embed(title="You've created a new character!")

		CharacterDescription = "\n".join(f"{Key}: {Value}" for Key, Value in NewCharacter.Data.items())

		NewCharacterEmbed.add_field(name=Name, value=CharacterDescription)

		HomeButton = Button(label="Home", row=0)
		HomeButton.callback = lambda Context: Self.HomePanel.Send_Panel(Context)
		NewCharacterView.add_item(HomeButton)
		
		await Context.response.edit_message(view=NewCharacterView, embed=NewCharacterEmbed)