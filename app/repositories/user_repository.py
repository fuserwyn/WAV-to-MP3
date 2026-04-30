from psycopg import connect


class UserRepository:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    def init_db(self) -> None:
        with connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        first_seen_at TIMESTAMPTZ DEFAULT NOW(),
                        last_seen_at TIMESTAMPTZ DEFAULT NOW(),
                        conversions_count INTEGER DEFAULT 0
                    )
                    """
                )
            conn.commit()

    def upsert_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        with connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (user_id, username, first_name, last_name)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT(user_id) DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        last_seen_at = NOW()
                    """,
                    (user_id, username, first_name, last_name),
                )
            conn.commit()

    def increment_conversions(self, user_id: int) -> None:
        with connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET conversions_count = conversions_count + 1,
                        last_seen_at = NOW()
                    WHERE user_id = %s
                    """,
                    (user_id,),
                )
            conn.commit()

    def fetch_stats(self, limit: int = 20) -> tuple[list[tuple], int, int]:
        with connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, username, first_name, last_name, conversions_count, last_seen_at
                    FROM users
                    ORDER BY last_seen_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

                cur.execute(
                    "SELECT COUNT(*), COALESCE(SUM(conversions_count), 0) FROM users"
                )
                totals = cur.fetchone()

        total_users = totals[0] if totals else 0
        total_conversions = totals[1] if totals else 0
        return rows, total_users, total_conversions
