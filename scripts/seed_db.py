from chalicelib.bot_service import BotDB

DB_NAME = "burrito_points"
DB_ENDPOINT_URL = "http://localhost:8000"

if __name__ == "__main__":
    db = BotDB(DB_NAME, **{'endpoint_url': DB_ENDPOINT_URL})
    db.add_points_to_users(sender="U025RUT3QQM", recipients=["U01AP4BM8SD"], channel="G01Q4U75KAP", points=2)
    print(f"{DB_NAME} seeded successfully!")
