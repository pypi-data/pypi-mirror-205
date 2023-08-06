from typing import Any, Dict, List, Optional
import requests

from the_lord_of_the_rings_sdk.exceptions import APIException
from the_lord_of_the_rings_sdk.utils import get_auth_header
from the_lord_of_the_rings_sdk.resources import MovieResource


class Client:
	def __init__(self, base_url: str, api_key: str) -> None:
		self.base_url = base_url
		self.api_key = api_key
		self.headers = get_auth_header(api_key)
		self.movie = MovieResource(self)

	def _get(self, endpoint: str) -> List:

		try:
			response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers)
			if response.status_code == 200:
				return response.json()["docs"]
			else:
				raise APIException(
					f"Error getting data from {endpoint}. Status code: {response.status_code}. Message: {response.json()['message']}"
				)

		except requests.exceptions.Timeout as e:
			raise APIException(f"Request timeout: {repr(e)}")

		except requests.exceptions.TooManyRedirects as e:
			raise APIException(f"Too Many Redirects: {repr(e)}")

		except requests.exceptions.RequestException as e:
			raise APIException(f"Request Exception: {repr(e)}")

	def get_movie(self, movie_id: Optional[str] = None) -> List[Dict[str, Any]]:
		if movie_id is not None:
			endpoint = f"movie/{movie_id}"
		else:
			endpoint = "movie"
		return self._get(endpoint)
