from aiogram.fsm.context import FSMContext
from public.menu.menu import get_menu_Driver_markup
from public.router.form_router import form_router
from public.form.form import Form
from aiogram.types import (

    CallbackQuery,

)

@form_router.callback_query(lambda c: c.data.startswith("cancel_instant"))
async def instant_book(callback_query: CallbackQuery, state: FSMContext):
    menu = get_menu_Driver_markup()
    await state.set_state(Form.Menu_Driver)
    await callback_query.message.answer("Great call, No need to rush!", reply_markup=menu)