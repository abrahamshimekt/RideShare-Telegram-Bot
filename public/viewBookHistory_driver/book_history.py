import asyncio
from datetime import datetime, timedelta
import logging
import random
import sys
import os

from aiogram import F
from aiogram.fsm.context import FSMContext
from public.connection.radis_storage import redis_conn
from public.router.form_router import form_router
from public.form.form import Form
from aiogram.types import (
    KeyboardButton,
    Message,
   
)

from public.menu.menu import get_menu_Driver_markup



@form_router.message(Form.Menu_Driver, F.text.casefold() == "view book history")
async def view_book_history(message: Message, state: FSMContext):
    books = redis_conn.keys("book:*")
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    if len(books) == 0:
        await message.answer("There are no books at the moment.",reply_markup=menu)
    else:
        Keys = []
        
        for book in books:
            book_data = redis_conn.hgetall(book)
            button = KeyboardButton(text=f"Book Id: {book_data['book_id']}\nLocation: {book_data['location']}\nDestination: {book_data['destination']}")
            if book_data['driver_id'] == str(message.from_user.id) and book_data['status'] == "completed":
                Keys.append(button)
        
        if len(Keys) == 0:
            await message.answer("There are no books at the moment.")
        else:
            await message.answer("Here are the list of books you have completed:")
            for key in Keys:
                await message.answer(key.text + "\n")

        
        await message.answer("======================", reply_markup=menu)