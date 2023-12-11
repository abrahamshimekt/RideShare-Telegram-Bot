
from aiogram import  F
from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.connection.radis_storage import redis_conn

from aiogram.fsm.context import FSMContext

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,

)

@form_router.message(Form.Menu_Driver, F.text.casefold() == "active books")
async def list_books(message: Message, state: FSMContext):
    books = redis_conn.keys("book:*")
    menu = get_menu_Driver_markup()
    id = message.from_user.id
    user_key = f"user:{id}"
    user_data = redis_conn.hgetall(user_key)

    if user_data.get('status') == "not available":
        await state.set_state(Form.Menu_Driver)
        await message.answer("Please set your status to available first.", reply_markup=menu)
    elif len(books) == 0:
        await state.set_state(Form.Menu_Driver)
        await message.answer("There are no books at the moment.", reply_markup=menu)
    else:
        Keys = []
        for book in books:
            book_data = redis_conn.hgetall(book)
            button = KeyboardButton(text=f"Book Id: {book_data['book_id']}\nLocation: {book_data['location']}\nDestination: {book_data['destination']}")
            if book_data['status'] == "accepted" and book_data['driver_id'] == str(message.from_user.id):
                Keys.append(button)
        keyBoard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[Keys])
        if len(Keys) == 0:
            await message.answer("There are no active books at the moment.")
        else:
            await message.answer("Here are the list of active books waiting for you:", reply_markup=keyBoard)
            await state.set_state(Form.RideComplete)