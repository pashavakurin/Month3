import sqlite3

from aiogram import types, Dispatcher
from config import bot, ADMIN_ID, BOT_PIC, ANIMATION_PIC
from const import START_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import start_keyboard


async def start_button(message: types.Message):
    Database().sql_insert_user_command(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    print(message)
    # with open(BOT_PIC, 'rb') as photo:
    #     await bot.send_photo(
    #         chat_id=message.chat.id,
    #         photo=photo,
    #         caption=START_TEXT.format(
    #             username=message.from_user.username
    #         ),
    #         parse_mode=types.ParseMode.MARKDOWN,
    #         reply_markup=await start_keyboard()
    #     )

    with open(ANIMATION_PIC, 'rb') as animation:
        await bot.send_animation(
            chat_id=message.chat.id,
            animation=animation,
            caption=START_TEXT.format(
                username=message.from_user.username
            ),
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await start_keyboard()
        )


async def secret_word(message: types.Message):
    if message.chat.id == ADMIN_ID:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Hello master'
        )
    else:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You have no right'
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=["start"])
    dp.register_message_handler(secret_word,
                                lambda word: "dorei" in word.text)