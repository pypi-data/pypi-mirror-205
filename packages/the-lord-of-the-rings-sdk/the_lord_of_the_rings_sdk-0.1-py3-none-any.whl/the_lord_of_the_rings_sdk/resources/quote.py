from typing import List

from ..models import Quote


class QuoteResource:
	def __init__(self, client) -> None:
		self.client = client

	def get_quotes(self) -> List[Quote]:
		data = self.client.get_quote()
		return [Quote(item) for item in data]

	def get_quote_by_id(self, quote_id: str) -> Quote:
		data = self.client.get_quote(quote_id)
		return Quote(data[0])

	def create_quote(self, quote_data):
		pass
