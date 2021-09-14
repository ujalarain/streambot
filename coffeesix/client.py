import asyncio
import random

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram.raw.functions.phone import CreateGroupCall

from pytgcalls import GroupCallFactory
from pytgcalls.exceptions import GroupCallNotFoundError

from coffeesix.config import config
from coffeesix.functions import stream_video_via_link

user = Client(
    config.SESSION,
    config.API_ID,
    config.API_HASH
)


class Player:
    def __init__(self):
        self.call = GroupCallFactory(user)
        self._client = {}

    async def start_stream(self, chat_id, query, message: Message):
        call = self.call.get_group_call()
        self._client[chat_id] = call
        y = await message.reply(f"processing...please wait")
        downloaded_video = stream_video_via_link(query)
        try:
            await self._client[chat_id].join(chat_id)
            await y.edit(f"Playing {query} in this chat")
            await self._client[chat_id].start_video(downloaded_video, repeat=False)
        except FloodWait as Fwx:
            await message.reply(f"Getting floodwait {Fwx.x} second, bot is sleeping")
            await asyncio.sleep(int(Fwx.x))
            await self._client[chat_id].join(chat_id)
            await y.edit(f"Playing {query} in this chat")
            await self._client[chat_id].start_video(downloaded_video, repeat=False)
        except GroupCallNotFoundError:
            try:
                await user.send(CreateGroupCall(
                    peer=await user.resolve_peer(chat_id),
                    random_id=random.randint(10000, 999999999)
                ))
                await self._client[chat_id].join(chat_id)
                await y.edit(f"Playing {query} in this chat")
                await self._client[chat_id].start_video(downloaded_video, repeat=False)
            except Exception as Ex:
                await y.edit(str(Ex))
        except Exception as ex:
            await y.edit(str(ex))

    async def stop_stream(self, message: Message):
        chat_id = message.chat.id
        await self._client[chat_id].stop()
        await message.reply("Bot successfully leave from the call")


player = Player()
