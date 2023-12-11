
from aiogram import F

from aiogram.fsm.context import FSMContext
from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from public.connection.radis_storage import redis_conn
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
   
)

@form_router.message(Form.Menu_Driver, F.text.casefold() == "set status")
async def set_status(message: Message, state: FSMContext):
    menu_Driver = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="Available")],
                    [KeyboardButton(text="Not Available")]
                ])
    await message.answer("Please set your status:", reply_markup=menu_Driver)
    await state.set_state(Form.DriverStatus)


@form_router.message(Form.DriverStatus, F.text.casefold() == "available")
async def set_status(message: Message, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    await message.answer("Your status has been set to available.", reply_markup=menu)
    id = message.from_user.id
    user_key = f"user:{id}"
    redis_conn.hset(user_key, "status", "available")

@form_router.message(Form.DriverStatus, F.text.casefold() == "not available")
async def set_status(message: Message, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    await message.answer("Your status has been set to not available.", reply_markup=menu)
    id = message.from_user.id
    user_key = f"user:{id}"
    redis_conn.hset(user_key, "status", "not available")