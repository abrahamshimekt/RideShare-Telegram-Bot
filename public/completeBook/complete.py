
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.connection.radis_storage import redis_conn
from public.api.api_token import token
from aiogram.types import (
    Message,

)


@form_router.message(Form.RideComplete)
async def process_complete(message: Message, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    await message.answer("Thank you for riding with us! We hope to see you again soon.", reply_markup=menu)
    book_id = message.text.split("\n")[0].split(":")[1].strip()
    book_key = f"book:{book_id}"
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    book = redis_conn.hgetall(book_key)
    passenger_id = book["passenger_id"]
    redis_conn.hset(book_key, 'status', 'completed')
    await bot.send_message(chat_id=passenger_id, text="Your ride has been completed. Thank you for riding with us!")

