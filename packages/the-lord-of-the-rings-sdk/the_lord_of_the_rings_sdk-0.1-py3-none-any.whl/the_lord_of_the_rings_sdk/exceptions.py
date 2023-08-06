class APIException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

	def __str__(self) -> str:
		return f"{self.__class__.__name__}: {self.message}"
