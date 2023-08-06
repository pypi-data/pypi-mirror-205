from typing import Dict


class BaseModel:
	def __init__(self, data: Dict) -> None:
		self.id = data.get("_id")


class Movie(BaseModel):
	def __init__(self, data: Dict) -> None:
		super().__init__(data)
		self.title = data.get("name")
		self.runtime = data.get("runtimeInMinutes")
		self.budget = data.get("budgetInMillions")
		self.revenue = data.get("boxOfficeRevenueInMillions")
		self.award_nominations = data.get("academyAwardNominations")
		self.award_wins = data.get("academyAwardWins")
		self.rotten_tomato_score = data.get("rottenTomatoesScore")

	def __str__(self) -> str:
		return f"id: {self.id}, title: {self.title}"
