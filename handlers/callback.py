import re
import sqlite3

from aiogram import types, Dispatcher
from config import bot
from const import START_TEXT, PROFILE_CAPTION_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import (
    question_first_keyboard,
    like_dislike_keyboard,
    edit_delete_keyboard, register_keyboard,
)
import random


async def start_questionnaire_call(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Male or Female",
        reply_markup=await question_first_keyboard()
    )


async def male_answer_call(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Yes you are Male ?",
    )


async def female_answer_call(call: types.CallbackQuery):
    print(call)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Yes you are female"
    )


async def my_profile_call(call: types.CallbackQuery):
    print(call)
    user = Database().sql_select_user_form_command(
        telegram_id=call.from_user.id
    )
    if user:
        with open(user[0]["photo"], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=PROFILE_CAPTION_TEXT.format(
                    nickname=user[0]['nickname'],
                    bio=user[0]['bio'],
                    age=user[0]['age'],
                    occupation=user[0]['occupation'],
                    married=user[0]['married'],
                ),
                reply_markup=await edit_delete_keyboard()
            )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Oh you have not registered in our system\n"
                 "Do you want to register ? 😈",
            reply_markup=await register_keyboard()
        )


async def random_profiles_call(call: types.CallbackQuery):
    user_forms = Database().sql_select_all_user_form_command()
    random_profile = random.choice(user_forms)
    with open(random_profile["photo"], 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=PROFILE_CAPTION_TEXT.format(
                nickname=random_profile['nickname'],
                bio=random_profile['bio'],
                age=random_profile['age'],
                occupation=random_profile['occupation'],
                married=random_profile['married'],
            ),
            reply_markup=await like_dislike_keyboard(
                telegram_id=random_profile['telegram_id']
            )

        )


async def like_detect_call(call: types.CallbackQuery):
    liked_user_form_id = re.sub("_like_", "", call.data)
    print(liked_user_form_id)
    try:
        Database().sql_insert_like_command(
            liker=call.from_user.id,
            liked=liked_user_form_id,
        )
    except sqlite3.IntegrityError as e:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You already liked this form"
        )
        await random_profiles_call(call=call)
        return
    await bot.send_message(
        chat_id=liked_user_form_id,
        text="Your form someone liked 👍🏻"
    )
    await random_profiles_call(call=call)


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_questionnaire_call,
                                       lambda call: call.data == "start_questionnaire")
    dp.register_callback_query_handler(male_answer_call,
                                       lambda call: call.data == "male_answer")
    dp.register_callback_query_handler(female_answer_call,
                                       lambda call: call.data == "female_answer")
    dp.register_callback_query_handler(my_profile_call,
                                       lambda call: call.data == "my_profile")
    dp.register_callback_query_handler(random_profiles_call,
                                       lambda call: call.data == "random_profile")
    dp.register_callback_query_handler(like_detect_call,
                                       lambda call: "_like_" in call.data)
