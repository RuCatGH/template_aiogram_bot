from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Меню", callback_data="future_fund_callback")
        ],
    ]
)
