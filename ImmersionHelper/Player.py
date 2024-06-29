class Player:
	def __init__(Self, MemberReference) -> None:
		Self.Data = {
			"MemberReference":MemberReference,
			"Name":MemberReference.name,
			"ID":MemberReference.id,
		}
		Self.Games = {}
		Self.Characters = {}