
from aiogram import Bot
from aiogram.enums import ParseMode
from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.connection.radis_storage import redis_conn
from public.api.api_token import *
from aiogram.fsm.context import FSMContext
from aiogram.types import (
   
    CallbackQuery
)


@form_router.callback_query(lambda c: c.data.startswith("accept:"))
async def instant_book(callback_query: CallbackQuery, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    booking_id = callback_query.data.split(":")[1]
    book_key = f"book:{booking_id}"
    booking_details = redis_conn.hgetall(book_key)
    if booking_details['status'] == 'accepted':
        await callback_query.message.answer("Ride already accepted by other driver.", reply_markup=menu)
    else:
        await callback_query.message.answer("You have accepted the ride!", reply_markup=menu)
        bot = Bot(token=token, parse_mode=ParseMode.HTML)
        id = callback_query.from_user.id
        pass_id = booking_details['passenger_id']
        redis_conn.hset(book_key, 'status', 'accepted')
        redis_conn.hset(book_key, 'driver_id', id)
        await bot.send_message(chat_id=pass_id, text="Your ride has been accepted. Please wait for the driver to arrive.")