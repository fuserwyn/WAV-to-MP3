from app.repositories.user_repository import UserRepository


class UserModel:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def init_db(self) -> None:
        self.user_repository.init_db()

    def upsert_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        self.user_repository.upsert_user(user_id, username, first_name, last_name)

    def increment_conversions(self, user_id: int) -> None:
        self.user_repository.increment_conversions(user_id)

    def fetch_stats(self, limit: int = 20) -> tuple[list[tuple], int, int]:
        return self.user_repository.fetch_stats(limit)
