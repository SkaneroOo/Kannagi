from surrealdb import HTTPClient
import asyncio
from random import randint

connection = HTTPClient("http://localhost:8000", username="root", password="root", namespace="Kannagi", database="KannagiDB")

async def main():
    for i in range(10_000_000):
        await connection.execute(f"INSERT INTO inventory (card_id, owner) VALUES ({randint(1, 200000)}, profiles:{randint(10000000, 100000000000)});")
        if i%10000 == 0:
            print("Inserted %d items" % i)
            input()


asyncio.run(main())