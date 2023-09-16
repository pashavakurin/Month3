from aiogram import executor
from config import dp
from handlers import start, callback, fsm_form, chat_action
from database import sql_commands


async def onstart_up(_):
    db = sql_commands.Database()
    db.sql_create_tables()


start.register_start_handlers(dp=dp)
callback.register_callback_handlers(dp=dp)
fsm_form.register_fsm_form_handlers(dp=dp)
chat_action.register_chat_actions_handlers(dp=dp)

if __name__ == "__main__":
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=onstart_up
    )