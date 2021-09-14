import os

from pyrogram import Client, idle
from coffeesix.client import user
from coffeesix.config import config
from coffeesix import bot_username


bot = Client(
    ":memory:",
    int(config.API_ID),
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="coffeesix.handlers")
)

if not os.path.exists("raw_dir"):
    os.mkdir("raw_dir")
if not os.path.exists("downloads"):
    os.mkdir("downloads")


async def get_uname():
    global bot_username
    x = await bot.get_me()
    bot_username += x.username

user.start()
bot.start()
bot.run(get_uname())
print(bot_username)
print("----Bot Running----\nHappy Testing ^-^")

idle()
