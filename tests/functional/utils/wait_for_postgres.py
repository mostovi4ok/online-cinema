import backoff
import psycopg

from core.settings import test_settings


@backoff.on_exception(backoff.expo, psycopg.OperationalError, max_tries=10)
def wait_for_postgres() -> None:
    with psycopg.connect(**test_settings.auth_postgres_dsn) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1")

    with psycopg.connect(**test_settings.profile_postgres_dsn) as conn, conn.cursor() as cursor:
        cursor.execute("SELECT 1")


if __name__ == "__main__":
    wait_for_postgres()
