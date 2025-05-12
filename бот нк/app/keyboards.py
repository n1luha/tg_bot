from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_quiz_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Поехали!', callback_data='start_quiz')]
    ])

def answer_options_kb(question_id: int):
    builder = InlineKeyboardBuilder()
    for i in range(1, 4):
        builder.add(InlineKeyboardButton(text=f'Вариант {i}', callback_data=f'answer_{question_id}_{i}'))
    return builder.adjust(1).as_markup()

def show_rating_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать рейтинг", callback_data="show_rating")]
    ])
