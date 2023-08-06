import os
import unittest
import requests

from unittest import mock
from the_lord_of_the_rings_sdk.client import Client
from the_lord_of_the_rings_sdk.models import Movie
from the_lord_of_the_rings_sdk.exceptions import APIException

API_BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")


class TestSDK(unittest.TestCase):
	def setUp(self):
		self.client = Client(API_BASE_URL, API_KEY)

	def test_get_movies(self):
		movies = self.client.movie.get_movies()
		self.assertIsNotNone(movies)
		self.assertGreater(len(movies), 0)
		self.assertIsInstance(movies[0], Movie)

	def test_get_movie_by_id(self):
		movie_id = "5cd95395de30eff6ebccde5c"
		movie = self.client.movie.get_movie_by_id(movie_id)
		self.assertIsNotNone(movie)
		self.assertIsInstance(movie, Movie)
		self.assertEqual(movie.id, movie_id)

	def test_get_movie_not_found(self):
		movie_id = "invalid_id"
		with self.assertRaises(APIException):
			self.client.movie.get_movie_by_id(movie_id)

	def mocked_requests_get(*args, **kwargs):
		class MockResponse:
			def __init__(self, json_data, status_code):
				self.json_data = json_data
				self.status_code = status_code

			def json(self):
				return self.json_data

		if args[0] == "https://the-one-api.dev/v2/movie":
			raise requests.exceptions.Timeout()
		elif args[0] == "https://the-one-api.dev/v2/movie/1":
			raise requests.exceptions.TooManyRedirects()
		elif args[0] == "https://the-one-api.dev/v2/movie/2":
			raise requests.exceptions.RequestException()
		elif args[0] == "https://the-one-api.dev/v2/movie/3":
			return MockResponse({"message": "Internal server error"}, 500)

		return MockResponse(None, 404)

	@mock.patch("requests.get", side_effect=mocked_requests_get)
	def test_get_timeout(self, mock_get):
		with self.assertRaises(APIException) as context:
			self.client._get(endpoint="movie")
		self.assertEqual(str(context.exception), "APIException: Request timeout: Timeout()")

	@mock.patch("requests.get", side_effect=mocked_requests_get)
	def test_get_too_many_redirects(self, mock_get):
		with self.assertRaises(APIException) as context:
			self.client._get(endpoint="movie/1")
		self.assertEqual(
			str(context.exception), "APIException: Too Many Redirects: TooManyRedirects()"
		)

	@mock.patch("requests.get", side_effect=mocked_requests_get)
	def test_get_request_exception(self, mock_get):
		with self.assertRaises(APIException) as context:
			self.client._get(endpoint="movie/2")
		self.assertEqual(
			str(context.exception), "APIException: Request Exception: RequestException()"
		)

	@mock.patch("requests.get", side_effect=mocked_requests_get)
	def test_get_http_error(self, mock_get):
		with self.assertRaises(APIException) as context:
			self.client._get(endpoint="movie/3")
		self.assertEqual(
			str(context.exception),
			"APIException: Error getting data from movie/3. Status code: 500. Message: Internal server error",
		)


if __name__ == "__main__":
	unittest.main()
