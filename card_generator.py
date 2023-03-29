from PIL import Image, ImageDraw
from requests import get
from surrealdb import HTTPClient
from io import BytesIO
import asyncio



from Kannagi import logger

log = logger.Logger(__name__, logger.LogLevel.DEBUG)

connection = HTTPClient("http://localhost:8000", username="root", password="root", namespace="Kannagi", database="KannagiDB")

star = Image.open("./assets/star.png").rotate(90)
frame_top = Image.open("./assets/frame_top.png")
frame_top_right = Image.open("./assets/frame_top_right.png")
frame_top_left = Image.open("./assets/frame_top_left.png")
frame_bottom = Image.open("./assets/frame_bottom.png")
frame_bottom_right = Image.open("./assets/frame_bottom_right.png")
frame_bottom_left = Image.open("./assets/frame_bottom_left.png")
frame_left = Image.open("./assets/frame_left.png")
frame_right = Image.open("./assets/frame_right.png")

async def main():
    cards = await connection.execute("SELECT id, image, name FROM characters;")
    for card in cards:
        image_req = get(card["image"])
        if not image_req:
            return
        image = Image.open(BytesIO(image_req.content))
        
        canvas = Image.new("RGB", (image.width+50, image.height+20), 7566195)
        canvas.paste(image, (40, 10))
        mult = 2
        resized = canvas.resize((canvas.width*mult, canvas.height*mult))
        drawable = ImageDraw.Draw(resized)
        drawable.polygon(((38*mult, (image.height-6)*mult), (56*mult, (image.height+12)*mult), (38*mult, (image.height+12)*mult)), (115, 115, 115, 255), (115, 115, 115, 255))
        drawable.polygon((((image.width+23)*mult, 9*mult), ((image.width+41)*mult, 9*mult), ((image.width+41)*mult, (image.height+15)*mult), ((image.width+38)*mult), 26*mult), (115, 115, 115, 255), (115, 115, 115, 255))
        final = resized.resize((canvas.width, canvas.height))

        final.save(f"./tools/out/{card['id'].split(':')[1]}_0.png")
        for i in range(6):
            final.paste(star, (4, 14 + i*32), star)
            final.save(f"./tools/out/{card['id'].split(':')[1]}_{i+1}.png")
        log.debug(f"Finished card {card['name']}")
        # return

asyncio.run(main())