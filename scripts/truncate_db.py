from chalicelib.bot_service import BotDB

DB_NAME = "burrito_points"
DB_ENDPOINT_URL = "http://localhost:8000"

if __name__ == "__main__":
    db = BotDB(DB_NAME, **{'endpoint_url': DB_ENDPOINT_URL})
    db.truncate_table()
    print(f"{DB_NAME} truncated successfully!")
