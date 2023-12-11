from public.menu.menu import get_menu_Driver_markup, get_menu_Passenger_markup
from public.router.form_router import form_router
from public.connection.radis_storage import redis_conn
from public.form.form import Form

from aiogram import  F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton
)


def get_edit_profile_markup():
    menu = InlineKeyboardBuilder()
    menu.add(InlineKeyboardButton(text="Full name", callback_data="full name"))
    menu.add(InlineKeyboardButton(text="Role", callback_data="role"))
    menu = menu.as_markup()
    return menu


@form_router.message(Form.Menu_Passenger, F.text.casefold() == "edit profile")
async def edit_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_key = f"user:{user_id}"
    
    if redis_conn.exists(user_key):
        await message.answer("You are about to edit your profile. Please choose what you want to edit:",
                             reply_markup=get_edit_profile_markup())
    else:
        await message.answer("You need to register first. Use /start to register.")


@form_router.message(Form.Menu_Driver, F.text.casefold() == "edit profile")
async def edit_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_key = f"user:{user_id}"
    
    if redis_conn.exists(user_key):
        await message.answer("You are about to edit your profile. Please choose what you want to edit:",
                             reply_markup=get_edit_profile_markup())
    else:
        await message.answer("You need to register first. Use /start to register.")


@form_router.callback_query(lambda c: c.data in ["full name", "role"])
async def process_profile(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "full name":
        await callback_query.message.answer("please provide your full name.")
        await state.set_state(Form.EditFullname)
    elif callback_query.data == "role":
        role = ''
        U_id = callback_query.from_user.id
        user_key = f"user:{U_id}"
        user_data = redis_conn.hgetall(user_key)
        if user_data.get('role') == "driver":
            role = "passenger"
        else:
            role = "driver"
        redis_conn.hset(user_key, "role", role)
        await state.clear()
        books = redis_conn.keys("book:*")
        if books:
            for book in books:
                book_data = redis_conn.hgetall(book)
                print(book_data)
                if book_data.get('passenger_id') == str(U_id) or book_data.get('driver_id') == str(U_id):
                    print('deleting book')
                    redis_conn.delete(book)
        menu = ''
        if redis_conn.hget(user_key, "role") == "driver":
            await state.set_state(Form.Menu_Driver)
            menu = get_menu_Driver_markup()
        else:
            await state.set_state(Form.Menu_Passenger)
            menu = get_menu_Passenger_markup()
        await callback_query.message.answer(f"Your role has been updated to {role}. Your previous books history has been deleted.", reply_markup=menu)


@form_router.message(Form.EditFullname)
async def process_Contact_info(message: Message, state: FSMContext):
    Contact_info = message.text.strip()
    U_id = message.from_user.id
    user_key = f"user:{U_id}"
    redis_conn.hset(user_key, "name", Contact_info)
    await state.clear()
    menu = ''
    if redis_conn.hget(user_key, "role") == "driver":
        await state.set_state(Form.Menu_Driver)
        menu = get_menu_Driver_markup()
    else:
        await state.set_state(Form.Menu_Passenger)
        menu = get_menu_Passenger_markup()
    await message.answer("Your full name has been updated.", reply_markup=menu)