from main import redis_conn
from main import form_router
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from public.form.form import  Form
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
   
)

from public.menu.menu import get_menu_Driver_markup, get_menu_Passenger_markup


@form_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_key = f"user:{user_id}"

    if not redis_conn.exists(user_key):
        menu_Passenger = ReplyKeyboardMarkup(resize_keyboard=True,
            keyboard=[[KeyboardButton(text="Register")]])
        await state.set_state(Form.Register)
        await message.answer("Welcome to the Ride Hailing bot!", reply_markup=menu_Passenger)
    else:
        menu_Passenger = get_menu_Passenger_markup()
        menu_Driver = get_menu_Driver_markup()

        user_data = redis_conn.hgetall(user_key)

        if user_data.get('role') == "driver":
            await message.answer(f"Welcome back, {user_data['name']}! What would you like to do today?", reply_markup=menu_Driver)
            await state.set_state(Form.Menu_Driver)
        else:
            await message.answer(f"Welcome back, {user_data['name']}! What would you like to do today?", reply_markup=menu_Passenger)
            await state.set_state(Form.Menu_Passenger)

@form_router.message(Form.Register, F.text.casefold() == "register")
async def process_Contact_info(message: Message, state: FSMContext):
    await state.set_state(Form.Contact_info)
    Contact = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[[KeyboardButton(text="Share Contact", request_contact=True)]])
    await message.answer("please share you contact info:", reply_markup=Contact)


@form_router.message(Form.Contact_info)
async def process_Contact_info(message: Message, state: FSMContext):
    name = phone = ''
    if message.contact and message.contact.phone_number:
        if message.contact.first_name:
            name = message.contact.first_name
        if message.contact.last_name:
            name += " " + message.contact.last_name
        phone = message.contact.phone_number

    await state.update_data(name=name, phone=phone)
    await state.set_state(Form.Role)
    menu_Passenger = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="Driver")],
                    [KeyboardButton(text="Passenger")]
                ])
    await message.answer("Great! Lastly, please specify your role..", reply_markup=menu_Passenger)

    
@form_router.message(Form.Role, F.text.casefold() == "driver")
async def process_role(message: Message, state: FSMContext):
    await state.update_data(role='driver')
    user_data = await state.get_data()

    await register_user(message.from_user.id, user_data)
    await state.clear()
    await message.answer("Registration successful! You can now use the /start command to access the bot features.")


@form_router.message(Form.Role, F.text.casefold() == "passenger")
async def process_role(message: Message, state: FSMContext):
    await state.update_data(role='passenger')
    user_data = await state.get_data()

    await register_user(message.from_user.id, user_data)
    await state.clear()
    await message.answer("Registration successful! You can now use the /start command to access the bot features.")


async def register_user(id, data):
    user_key = f"user:{id}"
    name = data['name']
    phone = data['phone']
    role = data['role']
    redis_conn.hset(user_key, mapping= {
        'id': id,
        "name": name,
        "phone": phone,
        "role": role,
        "status": "available"
        })





    