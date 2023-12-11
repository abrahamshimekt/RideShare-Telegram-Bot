from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton
)

def get_menu_Passenger_markup():
    menu_Passenger = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="Book Ride")],
                    [KeyboardButton(text="Cancel Book")],
                    [KeyboardButton(text="View Book History")],
                    [KeyboardButton(text="Edit Profile")],
                    [KeyboardButton(text="Review")]
                ])
    return menu_Passenger

def get_menu_Driver_markup():
    menu_Driver = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="List Books")],
                    [KeyboardButton(text="Active Books")],
                    [KeyboardButton(text="Set Status")],
                    [KeyboardButton(text="View Book History")],
                    [KeyboardButton(text="Edit Profile")],
                    [KeyboardButton(text="Review")]
                ])
    return menu_Driver

def get_rating_markup():
    rating = ReplyKeyboardMarkup(resize_keyboard=True,
        keyboard=[
                    [KeyboardButton(text="1")],
                    [KeyboardButton(text="2")],
                    [KeyboardButton(text="3")],
                    [KeyboardButton(text="4")],
                    [KeyboardButton(text="5")]
                ]) 
    return rating

def get_instant_alert_markup(book_id):
    menu = InlineKeyboardBuilder()
    menu.add(InlineKeyboardButton(text="Accept", callback_data=f"accept:{book_id}"))
    menu.add(InlineKeyboardButton(text="Cancel", callback_data="cancel_instant"))
    menu = menu.as_markup()
    return menu