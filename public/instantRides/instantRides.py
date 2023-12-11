from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.connection.radis_storage import redis_conn
from public.api.api_token import token
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,

)



@form_router.message(Form.RideAccept)
async def process_accept(message: Message, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    id = message.from_user.id
    await message.answer("You have accepted the ride!", reply_markup=menu)
    book_id = message.text.split("\n")[0].split(":")[1].strip()
    book_key = f"book:{book_id}"
    print("book key", book_key)
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    book = redis_conn.hgetall(book_key)
    pass_id = book['passenger_id']
    redis_conn.hset(book_key, 'status', 'accepted')
    redis_conn.hset(book_key, 'driver_id', id)
    await bot.send_message(chat_id=pass_id, text="Your ride has been accepted. Please wait for the driver to arrive.")