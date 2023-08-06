from typing import List

from the_lord_of_the_rings_sdk.models import Movie


class MovieResource:
	def __init__(self, client) -> None:
		self.client = client

	def get_movies(self) -> List[Movie]:
		data = self.client.get_movie()
		return [Movie(item) for item in data]

	def get_movie_by_id(self, movie_id: str) -> Movie:
		data = self.client.get_movie(movie_id)
		return Movie(data[0])

	def create_movie(self, movie_data):
		pass
