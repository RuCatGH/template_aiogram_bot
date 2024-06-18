import json

from aiogram import Router, types, F
from aiogram import Bot
from aiogram.fsm.context import FSMContext

from bot.keyboards.user import builder_kb, get_exchanges_buttons, menu_kb
from storage.requests.user import get_user
from storage.models import async_session
from storage.requests.crypto import get_exchanges
from bot.fsm.user_fsm import UserSpreadSettings


router = Router()


@router.callback_query(F.data == "settings_exchanges_callback")
async def callbacks_settings_exchanges(callback: types.CallbackQuery, bot: Bot) -> None:
    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)
        user_exchanges = json.loads(user.exchanges)['exchanges']

        default_exchanges = [exchange.name for exchange in await get_exchanges(session)]

        exchanges_kb = get_exchanges_buttons(default_exchanges, user_exchanges)
    await bot.send_message(text="Текущие биржи:", chat_id=callback.from_user.id, reply_markup=builder_kb(exchanges_kb))
    await callback.answer()


@router.callback_query(F.data.contains('settings_selected'))
async def calbacks_settings_exchange_deletion(callback: types.CallbackQuery, bot: Bot) -> None:
    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)

        user_exchanges = json.loads(user.exchanges)['exchanges']
        user_exchanges.remove(callback.data.split('_')[2])

        default_exchanges = [exchange.name for exchange in await get_exchanges(session)]

        exchanges_kb = get_exchanges_buttons(default_exchanges, user_exchanges)

        user.exchanges = json.dumps({'exchanges': user_exchanges})
        await session.commit()
    await bot.edit_message_text(message_id=callback.message.message_id, text="Текущие биржи:", chat_id=callback.from_user.id, reply_markup=builder_kb(exchanges_kb))
    await callback.answer()


@router.callback_query(F.data.contains('settings_unselected'))
async def calbacks_settings_exchange_deletion(callback: types.CallbackQuery, bot: Bot) -> None:
    async with async_session() as session:
        user = await get_user(session, callback.from_user.id)

        user_exchanges = json.loads(user.exchanges)['exchanges']

        user_exchanges.append(callback.data.split('_')[2])

        default_exchanges = [exchange.name for exchange in await get_exchanges(session)]

        exchanges_kb = get_exchanges_buttons(default_exchanges, user_exchanges)

        user.exchanges = json.dumps({'exchanges': user_exchanges})
        await session.commit()
    await bot.edit_message_text(message_id=callback.message.message_id, text="Текущие биржи:", chat_id=callback.from_user.id, reply_markup=builder_kb(exchanges_kb))
    await callback.answer()


@router.callback_query(F.data == "settings_spread_callback")
async def callbacks_settings_exchanges(callback: types.CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await state.set_state(UserSpreadSettings.choosing_spread)

    await bot.send_message(text="💰 Введите желаемый спред (%)", chat_id=callback.from_user.id, reply_markup=menu_kb)
    await callback.answer()