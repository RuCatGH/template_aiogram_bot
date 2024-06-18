
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Hello world')
