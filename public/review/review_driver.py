from aiogram import  F
from aiogram.fsm.context import FSMContext
from public.form.form import Form
from public.router.form_router import form_router
from public.controllers.get_all_passengers import *
from public.controllers.get_all_drivers import *
from public.connection.radis_storage import redis_conn
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
  
)

from public.menu.menu import get_menu_Driver_markup, get_menu_Passenger_markup, get_rating_markup

@form_router.message(Form.Menu_Passenger, F.text.casefold() == "review")
async def review(message: Message, state: FSMContext):
    drivers = await get_all_drivers()
    Key = []
    for driver_id in drivers:
        user_key = f"user:{driver_id}"
        user_data = redis_conn.hgetall(user_key)
        Key.append(KeyboardButton(text=f"Driver Id: {driver_id}\nName: {user_data['name']}\nPhone: {user_data['phone']}"))
    
    if len(Key) == 0:
        menu = get_menu_Passenger_markup()
        await state.set_state(Form.Menu_Passenger)
        await message.answer("There are no drivers at the moment.", reply_markup=menu)
    else:
        keyBoard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[Key])
        await message.answer("Please choose a driver to review:", reply_markup=keyBoard)
        await state.set_state(Form.DriverReview)
    
@form_router.message(Form.Menu_Driver, F.text.casefold() == "review")
async def review(message: Message, state: FSMContext):
    passengers = await get_all_passengers()
    Key = []
    for passenger_id in passengers:
        user_key = f"user:{passenger_id}"
        user_data = redis_conn.hgetall(user_key)
        Key.append(KeyboardButton(text=f"Passenger Id: {passenger_id}\nName: {user_data['name']}\nPhone: {user_data['phone']}"))
    
    if len(Key) == 0:
        menu = get_menu_Driver_markup()
        await state.set_state(Form.Menu_Driver)
        await message.answer("There are no passengers at the moment.", reply_markup=menu)
    else:
        keyBoard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[Key])
        await message.answer("Please choose a passenger to review:", reply_markup=keyBoard)
        await state.set_state(Form.PassengerReview)


@form_router.message(Form.DriverReview)
async def process_review(message: Message, state: FSMContext):
    rating = get_rating_markup()
    reviewee_id = message.text.split("\n")[0].split(":")[1].strip()
    await state.update_data(reviewee = reviewee_id)
    if redis_conn.exists(f"rating:{message.from_user.id}:{reviewee_id}"):
        menu = ''
        user_key = f'user:{message.from_user.id}'
        user_data = redis_conn.hgetall(user_key)
        await state.clear()
        
        if user_data.get('role') == "driver":
            menu = get_menu_Driver_markup()
            await state.set_state(Form.Menu_Driver)
        else:
            menu = get_menu_Passenger_markup()
            await state.set_state(Form.Menu_Passenger)

        await message.answer("You have already reviewed this user.", reply_markup=menu)
    else:
        await message.answer("Please rate the driver from 1-5:", reply_markup=rating)
        await state.set_state(Form.Rating)


@form_router.message(Form.PassengerReview)
async def process_review(message: Message, state: FSMContext):
    rating = get_rating_markup()
    reviewee_id = message.text.split("\n")[0].split(":")[1].strip()
    await state.update_data(reviewee = reviewee_id)
    if redis_conn.exists(f"rating:{message.from_user.id}:{reviewee_id}"):
        menu = ''
        user_key = f'user:{message.from_user.id}'
        user_data = redis_conn.hgetall(user_key)
        await state.clear()
        
        if user_data.get('role') == "driver":
            menu = get_menu_Driver_markup()
            await state.set_state(Form.Menu_Driver)
        else:
            menu = get_menu_Passenger_markup()
            await state.set_state(Form.Menu_Passenger)

        await message.answer("You have already reviewed this user.", reply_markup=menu)
    await message.answer("Please rate the passenger from 1-5:", reply_markup=rating)
    await state.set_state(Form.Rating)


@form_router.message(Form.Rating)
async def process_rating(message: Message, state: FSMContext):
    reviewer_id = message.from_user.id
    data = await state.get_data()
    reviewee_id = data['reviewee']
    rating_key = f"rating:{reviewer_id}:{reviewee_id}"
    menu = ''
    user_key = f'user:{reviewer_id}'
    user_data = redis_conn.hgetall(user_key)
    await state.clear()
    
    if user_data.get('role') == "driver":
        menu = get_menu_Driver_markup()
        await state.set_state(Form.Menu_Driver)
    else:
        menu = get_menu_Passenger_markup()
        await state.set_state(Form.Menu_Passenger)

    await message.answer("Thank you for your feedback!", reply_markup=menu)
    redis_conn.hset(rating_key, "rating", message.text.strip())