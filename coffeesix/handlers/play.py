from coffeesix.client import player
from pyrogram import Client
from pyrogram.types import Message
from coffeesix.functions import command


@Client.on_message(command("stream"))
async def start_stream(_, message: Message):
    query = " ".join(message.command[1:])
    reply = message.reply_to_message
    chat_id = message.chat.id
    if query:
        await player.start_stream(chat_id, query, message)
    elif reply:
        if reply.video or reply.document:
            await message.reply("This feature is under development, contact @shohih_abdul2 for more information")
        else:
            await message.reply("Reply to video or document.\nNote: This feature is under development")
    else:
        await message.reply("Pass the query after /stream command!")


@Client.on_message(command("end"))
async def end_stream(_, message: Message):
    await player.stop_stream(message)
