from config import bot
from aiogram import types, Dispatcher

from const import REFERENCE_MENU_TEXT
from database.sql_commands import Database
from keyboards.inline_buttons import reference_menu_keyboard
import os
import binascii
from aiogram.utils.deep_linking import _create_link


async def reference_menu_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.from_user.id,
        text=REFERENCE_MENU_TEXT,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=await reference_menu_keyboard()
    )


async def reference_list_owner(call: types.CallbackQuery):
    reference_list = Database().sql_select_list_referral_by_owner_id_command(
        owner=call.from_user.id
    )
    data = []
    if reference_list:
        for user in reference_list:
            data.append(f"[{user['referral_id']}](tg://user?id={user['referral_id']})")
        text = '\n'.join(data)
        await bot.send_message(
            chat_id=call.from_user.id,
            text=text,
            parse_mode=types.ParseMode.MARKDOWN
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You have no referrals",
            parse_mode=types.ParseMode.MARKDOWN
        )


async def reference_link_generation(call: types.CallbackQuery):
    token = binascii.hexlify(os.urandom(8)).decode()
    link = await _create_link(link_type="start", payload=token)
    user = Database().sql_select_user_command(
        telegram_id=call.from_user.id
    )
    if not user[0]['link']:
        Database().sql_update_user_link_generation_command(
            link=link,
            telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"This is your referral link\n"
                 f"{link}"
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"This is your referral link from DB\n"
                 f"{user[0]['link']}"
        )


def register_reference_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(reference_menu_call, lambda call: call.data == "referral_menu")
    dp.register_callback_query_handler(reference_link_generation, lambda call: call.data == "reference_link")
    dp.register_callback_query_handler(reference_list_owner, lambda call: call.data == "reference_list")
