from Kannagi.Database import Database
import requests
import time

connection = Database("localhost", user="root", passwd="12345678")
API_URL = 'https://graphql.anilist.co'

query_characters = """
query ($Page: Int, $PerPage: Int) {
  Page(perPage: $PerPage, page: $Page) {
    characters(sort: FAVOURITES_DESC) {
      id,
      name {
        full
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
        }
      }
    }
  }
}
"""

def scrape_top_popular():
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
    for page in range(start, end+1):
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
                        data = connection.execute(f"SELECT * FROM media where id={m['id']}")
                        if data:
                            continue
                        if m["id"] not in medias:
                            medias[m["id"]] = m
                    time.sleep(0.4)
        else:
            pass
    for m in medias.values():
        # if m["title"]["romaji"]:
        #     m["title"]["romaji"] = m["title"]["romaji"].replace("'", "\\'")
        # if m["title"]["english"]:
        #     m["title"]["english"] = m["title"]["english"].replace("'", "\\'")
        connection.execute("INSERT INTO media (id, title_ro, title_en) VALUES (%s, %s, %s);", m["id"], m["title"]["romaji"], m["title"]["english"], commit=True)
        print(f"Inserted media: {m['title']['romaji']}")
    for c in characters:
        data = connection.execute(f"SELECT * FROM characters WHERE id={m['id']}")
        if data:
            continue
        connection.execute("INSERT INTO characters (id, name) VALUES (%s, %s);", c["id"], c["name"]["full"], commit=True)
        for mid in c["media"]:
            connection.execute("INSERT INTO characters_has_media (characters_id, media_id) VALUES (%s, %s);", c["id"], mid, commit=True)
        print(f"Inserted character:{c['name']['full']}")


    # print(len(medias))
    # print(medias)
    

def scrape_db():
    while True:
        print("Choose what to do:\n1. Scrape top popular characters\n2. Exit")
        try:
            choice = int(input())
        except ValueError:
            pass
        else:
            if choice == 1:
                scrape_top_popular()
            elif choice == 2:
                return

def main():
    # data = connection.execute("INFO FOR DB;")
    # print(data)
    while True:
        print("Choose what to do:\n1. Scrape AniList API\n2. Exit")
        try:
            choice = int(input())
        except ValueError:
            pass
        else:
            if choice == 1:
                scrape_db()
            elif choice == 2:
                return

if __name__ == "__main__":
    main()