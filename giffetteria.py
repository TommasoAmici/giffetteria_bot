from bs4 import BeautifulSoup
from requests import get
import telegram
from telegram.ext import Updater, CommandHandler, InlineQueryHandler
import random
import re
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultGif, ParseMode, InputTextMessageContent


bot_token = ""


def make_soup(url):
    page = get(url)
    if page.status_code != 200:
        return None
    return BeautifulSoup(page.text, "html.parser")


def sanitize_query(args):
    # sanitizes query
    query = " ".join(args)
    non_alpha = re.compile("[\W_]+", re.UNICODE)
    return non_alpha.sub(" ", query).strip()


def giffetteria(bot, update, args):
    # get args from message
    if args:
        query = sanitize_query(args)
    else:
        query = ""
    gif_urls = []
    soup = make_soup("http://giffetteria.it/?s=" + query)
    # get all gif links from page
    for gif_link in soup.find_all("img", attrs={"class": "gl-lazy"}):
        gif_urls.append(gif_link.get("data-gif"))
    try:
        random_gif = random.choice(gif_urls)
    except:
        random_gif = "http://giffetteria.it/archivio/signoresignori13.gif"
        bot.send_message(chat_id=update.message.chat_id,
                     text="Nessuna GIF trovata in archivio, prova con un'altra parola chiave...", parse_mode="markdown")
    bot.send_document(chat_id=update.message.chat_id, document=random_gif)


# finds gifs in page i, given query
# returns gifs and thumbnails
def find_gifs(i, query, gif_urls, gif_thumbs):
    try:
        soup = make_soup("http://giffetteria.it/page/{}/?s={}".format(i, query))
    except:
        return [], []
    # get all gif links from page
    for gif_link in soup.find_all("img", attrs={"class": "gl-lazy"}):
        gif_urls.append(gif_link.get("data-gif"))
        gif_thumbs.append(gif_link.get("data-thumb"))
    return gif_urls, gif_thumbs


def inlinequery(bot, update):
    """Handle the inline query. And looks for gifs"""
    query = update.inline_query.query
    gif_urls = []
    gif_thumbs = []
    for i in range(1,6):
        gif_urls, gif_thumbs = find_gifs(i, query, gif_urls, gif_thumbs) 
        # send gifs to inline results
        results = []
        for j in range(len(gif_urls)):
            results.append(InlineQueryResultGif(
                           id=uuid4(),
                           gif_url=gif_urls[j],
                           thumb_url=gif_thumbs[j]))
        bot.answer_inline_query(update.inline_query.id, results)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Cerca GIF inline `@giffetteriabot` o ricevi una GIF casuale `/giffetteria query`", parse_mode="markdown")


update = Updater(token=bot_token)
dp = update.dispatcher
dp.add_handler(CommandHandler('giffetteria', giffetteria, pass_args=True))
dp.add_handler(CommandHandler(["start", "help", "aiuto"], start))
dp.add_handler(InlineQueryHandler(inlinequery))
update.start_polling()
update.idle()
