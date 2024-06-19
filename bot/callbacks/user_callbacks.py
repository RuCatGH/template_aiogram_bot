from aiogram import Router, types, F
from aiogram import Bot
from aiogram.fsm.context import FSMContext


router = Router()


@router.callback_query()
async def callbacks_start(callback: types.CallbackQuery, bot: Bot) -> None:
    await callback.answer()
