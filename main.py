import telebot
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
from collections import deque


# ======================
# تنظیمات
# ======================

BOT_TOKEN = "8946269599:AAFUk-sEkKl53apo-5XzXe0IKkDJQgtzyMY"

CHANNEL_ID = "@YOUR_CHANNEL"

SITE = "https://mangaup.ir/"


bot = telebot.TeleBot(BOT_TOKEN)

translator = GoogleTranslator(
    source="auto",
    target="fa"
)


sent_items = deque(maxlen=500)



# ======================
# گرفتن اطلاعات سایت
# ======================

def get_manga():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    try:

        r = requests.get(
            SITE,
            headers=headers,
            timeout=15
        )


        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )


        results = []


        # پیدا کردن کارت های مانگا

        for item in soup.find_all("article"):

            title = item.get_text(
                strip=True
            )


            img = item.find("img")


            if img:

                image = (
                    img.get("src")
                    or
                    img.get("data-src")
                )


                if title and image:

                    results.append(
                        {
                            "title":title,
                            "image":image
                        }
                    )


        return results


    except Exception as e:

        print(e)

        return []




# ======================
# ارسال به تلگرام
# ======================

def send_news():

    while True:


        mangas = get_manga()



        for manga in mangas:


            title = manga["title"]


            if title in sent_items:
                continue



            try:


                fa_title = translator.translate(
                    title
                )


                caption = f"""

📚 <b>{fa_title}</b>


🌐 منبع:
{SITE}

"""


                bot.send_photo(

                    CHANNEL_ID,

                    manga["image"],

                    caption=caption,

                    parse_mode="HTML"

                )



                sent_items.append(title)



                print(
                    "Sent:",
                    title
                )



                # هر یک دقیقه

                time.sleep(60)



            except Exception as e:

                print(e)




# ======================

if __name__ == "__main__":

    print(
        "Manga Bot Running..."
    )

    send_news()