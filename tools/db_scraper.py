from surrealdb import HTTPClient
import asyncio
import requests
import time

connection = HTTPClient("http://localhost:8000", username="root", password="root", namespace="Kannagi", database="KannagiDB")
API_URL = 'https://graphql.anilist.co'

query_characters = """
query ($Page: Int, $PerPage: Int) {
  Page(perPage: $PerPage, page: $Page) {
    characters(sort: FAVOURITES_DESC) {
      id,
      name {
        full
      },
      image {
        large
      }
    }
  }
}
"""

query_series = """
query ($Page: Int, $CharacterId: Int) {
  Character(id: $CharacterId) {
    media(sort: POPULARITY_DESC, page: $Page, perPage: 50) {
      pageInfo {
        hasNextPage
      }
      nodes {
        id,
        title {
          romaji,
          english
        },
        type
      }
    }
  }
}
"""

async def scrape_top_popular():
    print("How many characters per page (1-50):")
    try:
        count = int(input())
    except ValueError:
        pass
    print("Which page(s) to scrape:")
    pages = input()
    try:
        if "-" in pages:
            start, end = [int(p) for p in pages.split("-")[:2]]
        else:
            start = end = int(pages)
    except ValueError:
        pass
    print("Scrape media data? (y/n)")
    choice = input()
    medias = {}
    characters = []
    for page in range(start, end):
        characters_page = requests.post(API_URL, json={'query': query_characters, 'variables': {"Page": page, "PerPage": count}}).json()["data"]["Page"]["characters"]
        print(f"Got {len(characters_page)} characters")
        characters.extend(characters_page)
        if choice == "y":
            for character in characters_page:
                character["media"] = []
                i = 1
                while i:
                    media = requests.post(API_URL, json={'query': query_series, 'variables': {"Page": i, "CharacterId": character["id"]}}).json()["data"]["Character"]["media"]
                    i = i + 1 if media["pageInfo"]["hasNextPage"] else 0
                    media_page = media["nodes"]
                    for m in media_page:
                        character["media"].append(m["id"])
                        data = await connection.execute(f"SELECT * FROM medias:{m['id']}")
                        if data:
                            continue
                        if m["id"] not in medias:
                            medias[m["id"]] = m
                    time.sleep(0.4)
        else:
            pass
    for m in medias.values():
        if m["title"]["romaji"]:
            m["title"]["romaji"] = m["title"]["romaji"].replace("'", "\\'")
        if m["title"]["english"]:
            m["title"]["english"] = m["title"]["english"].replace("'", "\\'")
        await connection.execute("INSERT INTO medias (id, title_ro, title_en, type) VALUES (%s, '%s', '%s', '%s');COMMIT;" % (m["id"], m["title"]["romaji"], m["title"]["english"], m["type"]))
        print(f"Inserted media:{m['title']['romaji']}")
    for c in characters:
        data = await connection.execute(f"SELECT * FROM characters:{m['id']}")
        if data:
            continue
        try:
            await connection.execute("""INSERT INTO characters {
                id: %s, 
                name: '%s', 
                image: '%s', 
                media: [%s]
                };
                COMMIT;""" % (c["id"], c["name"]["full"].replace("'", "\\'"), c["image"]["large"], "medias:" + ",medias:".join([str(d) for d in c["media"]])))
        except:
            print("INSERT INTO characters (id, name, image, media) VALUES (%s, '%s', '%s', [%s]);COMMIT;" % (c["id"], c["name"]["full"].replace("'", "\\'"), c["image"], "medias:" + ", medias:".join([str(d) for d in c["media"]])))
        print(f"Inserted character:{c['name']['full']}")


    # print(len(medias))
    # print(medias)
    

async def scrape_db():
    while True:
        print("Choose what to do:\n1. Scrape top popular characters\n2. Exit")
        try:
            choice = int(input())
        except ValueError:
            pass
        else:
            if choice == 1:
                await scrape_top_popular()
            elif choice == 2:
                return

async def main():
    data = await connection.execute("INFO FOR DB;")
    print(data)
    while True:
        print("Choose what to do:\n1. Scrape AniList API\n2. Exit")
        try:
            choice = int(input())
        except ValueError:
            pass
        else:
            if choice == 1:
                await scrape_db()
            elif choice == 2:
                await connection.disconnect()
                return

asyncio.run(main())