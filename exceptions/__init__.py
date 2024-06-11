class DuplicateNodeNameException(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class NodeTypeNotFoundException(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)