import datetime

from config import bot, GROUP_ID
from aiogram import types, Dispatcher

from database.sql_commands import Database


async def echo_ban(message: types.Message):
    ban_words = ['fuck', 'bitch', 'damn', "DAMN"]

    if message.chat.id == GROUP_ID:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ''):
                ban_user = Database().sql_select_ban_user_command(
                    telegram_id=message.from_user.id
                )
                if ban_user[0]['count'] >= 3:
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text=message.text
                    )
                elif ban_user:
                    print(ban_user)
                    Database().sql_update_ban_user_count_command(
                        telegram_id=message.from_user.id
                    )
                else:
                    Database().sql_insert_ban_user_command(
                        telegram_id=message.from_user.id
                    )
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Hey dont use curse words or "
                         "i gonna ban you forever"
                )
                # await bot.ban_chat_member(
                #     chat_id=message.chat.id,
                #     user_id=message.from_user.id,
                #     until_date=datetime.datetime.now() + datetime.timedelta(minutes=1)
                # )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_ban)