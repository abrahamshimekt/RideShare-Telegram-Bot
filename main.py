import asyncio
from datetime import datetime, timedelta
import logging
import random
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from public.router.form_router import form_router
from public.connection.radis_storage import redis_conn
from public.signup.register import *
from public.acceptinstantRides.acceptrides import *
from public.activeBookings.activebookings import *
from public.allBookings import *
from public.booking.booking import *
from public.book_history_passenger.book_history import *
from public.cancelRides.cancel import *
from public.completeBook.complete import *
from public.driveStatus.driver_status import *
from public.profile.editProfile import *
from public.review.review_driver import *
from public.instantRides.instantRides import *
from public.menu.menu import *
from public.viewBookHistory_driver.book_history import *
from public.api.api_token import token


async def main():
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    dp.include_router(form_router)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())