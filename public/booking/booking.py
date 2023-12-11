from aiogram import Bot, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from public.menu.menu import get_instant_alert_markup, get_menu_Passenger_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.controllers.get_all_drivers import *
from public.controllers.get_all_passengers import *
from public.controllers.estimate_distance import *
from public.api.api_token import token
from public.connection.radis_storage import redis_conn
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton
)


@form_router.message(Form.Menu_Passenger, F.text.casefold() == "book ride")
async def book(message: Message, state: FSMContext):
    await state.set_state(Form.BookLocation)
    await message.answer("Please specify your location:")

@form_router.message(Form.BookLocation)
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location = message.text.strip())
    await state.set_state(Form.BookDestination)
    await message.answer("Please specify your destination:")


@form_router.message(Form.BookDestination)
async def process_destination(message: Message, state: FSMContext):
    await state.update_data(destination=message.text.strip())
    menu_confirm= InlineKeyboardBuilder()
    menu_confirm.add(InlineKeyboardButton(text="Confirm", callback_data="confirm"))
    menu_confirm.add(InlineKeyboardButton(text="Cancel", callback_data="cancel"))
    menu_confirm = menu_confirm.as_markup()
    await message.answer("Please confirm your booking:", reply_markup=menu_confirm)
    

@form_router.callback_query(lambda c: c.data in ["confirm", "cancel"])
async def process_callback_button(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        await callback_query.message.answer("Your booking has been confirmed!")
        await state.set_state(Form.Menu_Passenger)
        menu = get_menu_Passenger_markup()
        res = await estimate_time_distance()
        await callback_query.message.answer(f"Estimated distance: {res[0]}")
        await callback_query.message.answer(f"Estimated arrival time: {res[1]}", reply_markup=menu)

        data = await state.get_data()
        store_key = "metric"
        store = redis_conn.hgetall(store_key)
        last_book_id = int(store.get("last_book_id", 0))
        last_book_id += 1
        book_key = f"book:{last_book_id}"

        redis_conn.hset(book_key, mapping = {
                "location": data["location"],
                "destination": data["destination"],
                "book_id": last_book_id,
                "status": "pending",
                "passenger_id": callback_query.from_user.id,
                "driver_id": 0
                })
        redis_conn.hset(store_key, mapping={'last_book_id': last_book_id})

        drivers = await get_all_drivers()
        bot = Bot(token=token, parse_mode=ParseMode.HTML)
        for driver_id in drivers:
            await bot.send_message(chat_id=driver_id, text="New ride alert! Someone has booked a ride.", reply_markup=get_instant_alert_markup(last_book_id))
    else:
        await state.set_state(Form.Menu_Passenger)
        menu = get_menu_Passenger_markup()
        await callback_query.message.answer("Your booking has been cancelled!", reply_markup=menu)
  

@form_router.message(Form.Menu_Passenger, F.text.casefold() == "cancel book")
async def process_cancel(message: Message, state: FSMContext):
    u_id = message.from_user.id
    books = redis_conn.keys("book:*")
    menu = get_menu_Passenger_markup()
    await state.set_state(Form.Menu_Passenger)
    if len(books) == 0:
        await message.answer("You didn't have any books.", reply_markup=menu)
    else:
        found = False
        bok = ''
        for bk in books:
            book_data = redis_conn.hgetall(bk)
            if book_data.get('passenger_id') == str(u_id) and (book_data.get('status') == 'pending' or book_data.get('status') == 'accepted'):
                if book_data.get('status') == 'accepted':
                    bot = Bot(token=token, parse_mode=ParseMode.HTML)
                    await bot.send_message(chat_id=book_data.get('driver_id'), text="Your ride has been cancelled. please check your active books.")
                found = True
                bok = bk
                break

        if not found:
            await message.answer("You didn't have any active or pending books.", reply_markup=menu)
        else:
            redis_conn.delete(bok)
            await message.answer("Your booking has been cancelled!", reply_markup=menu)