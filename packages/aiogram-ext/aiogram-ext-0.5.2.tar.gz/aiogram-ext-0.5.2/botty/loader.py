import logging
from asyncio import new_event_loop

from aiohttp.web import Application

from .bot import Bot
from .config import BOT_TOKEN, MONGO, APP_URL
from .deps import MongoStorage
from .dispatcher import Dispatcher

storage = MongoStorage(
    db_name=MONGO.DB,
    host=MONGO.HOST,
    username=MONGO.USER,
    password=MONGO.PASSWORD,
)

loop = new_event_loop()
bot = Bot(BOT_TOKEN, loop)
dp = Dispatcher(bot, storage, loop)
logger = logging.getLogger()
app = Application(loop=loop)

Dispatcher.set_current(dp)


def run():
    dp.run_server(APP_URL, app)
