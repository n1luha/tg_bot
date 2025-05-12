import asyncio
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class QuizState(StatesGroup):
    waiting_for_name = State()
    question_index = State()
    score = State()
    questions = State()
    message_id = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    from_user_id = message.from_user.id
    already_played = await rq.has_played(from_user_id)

    if already_played:
        await message.answer("❗️Ты уже проходил(а) викторину.\nСпасибо за участие!")
        return

    await rq.set_user(from_user_id)
    await state.clear()
    await message.answer(
        "Привет!\nРады видеть тебя на нашем мероприятии🎥.\n\n"
        "Чтобы разнообразить досуг, во время Ночи Кино будет проходить викторина.\n"
        "На каждый вопрос выделяется 20 секунд! Если в течение этого времени ответа не последует, вопрос исчезнет без начисления баллов.\n"
        "Р.S: Победители получат приятный бонус!.\n\n"
        "Перед началом напиши боту:\n\n"
        "🎞 Фамилия\n🎞 Имя\n🎞 Институт\n\n"
        "📌 Пример:\nКультмассов Культмасс, ФизМех"
    )
    await state.set_state(QuizState.waiting_for_name)

@router.message(QuizState.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Имя не может быть пустым. Попробуй еще раз:")
        return

    await state.update_data(user_name=name)
    await message.answer(
        "Отлично! Теперь нажми кнопку, чтобы начать викторину 👇",
        reply_markup=kb.start_quiz_kb()
    )

@router.callback_query(F.data == 'start_quiz')
async def start_quiz(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass

    questions = await rq.get_all_questions()
    await state.update_data(question_index=0, score=0, questions=questions)
    await send_question(bot, callback.message.chat.id, state)

async def send_question(bot: Bot, user_id: int, state: FSMContext):
    data = await state.get_data()
    questions = data['questions']
    index = data['question_index']

    if index >= len(questions):
        await rq.save_result(
            tg_id=user_id,
            first_name=data.get("user_name", "Без имени"),
            score=data['score'],
            total=len(questions)
        )
        await state.clear()
        await bot.send_message(
            user_id,
            "🎉 Викторина пройдена!\nСпасибо за участие 🤝",
            reply_markup=kb.show_rating_kb()
        )
        return

    q = questions[index]
    question_text = (
        f"Вопрос {index+1}:\n{q.text}\n\n"
        f"1. {q.option_1}\n2. {q.option_2}\n3. {q.option_3}\n\n"
        "⏱ Осталось времени: 20 секунд"
    )

    send_with_photo = False
    photo_path = None

    if index == 4:
        photo_path = "static/5.webp"
        send_with_photo = True
    elif index == 9:
        photo_path = "static/10.webp"
        send_with_photo = True
    elif index == 14:
        photo_path = "static/15.webp"
        send_with_photo = True

    if send_with_photo and photo_path:
        try:
            photo = FSInputFile(photo_path)
            msg = await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=question_text,
                reply_markup=kb.answer_options_kb(q.id)
            )
            await state.update_data(is_photo_message=True)
        except Exception as e:
            print(f"Не удалось отправить фото ({photo_path}), отправляем текстовое сообщение: {e}")
            msg = await bot.send_message(
                user_id,
                question_text,
                reply_markup=kb.answer_options_kb(q.id)
            )
            await state.update_data(is_photo_message=False)
    else:
        msg = await bot.send_message(
            user_id,
            question_text,
            reply_markup=kb.answer_options_kb(q.id)
        )
        await state.update_data(is_photo_message=False)

    await state.update_data(message_id=msg.message_id)
    asyncio.create_task(update_timer(bot, user_id, msg.message_id, state))

async def update_timer(bot: Bot, user_id: int, message_id: int, state: FSMContext):
    for remaining in range(19, 0, -1):
        await asyncio.sleep(1)

        current_data = await state.get_data()
        if current_data.get("message_id") != message_id:
            return

        try:
            q = current_data['questions'][current_data['question_index']]
            updated_text = (
                f"Вопрос {current_data['question_index']+1}:\n{q.text}\n\n"
                f"1. {q.option_1}\n2. {q.option_2}\n3. {q.option_3}\n\n"
                f"⏱ Осталось времени: {remaining} секунд"
            )

            if current_data.get('is_photo_message', False):
                # Для сообщений с фото редактируем подпись
                await bot.edit_message_caption(
                    chat_id=user_id,
                    message_id=message_id,
                    caption=updated_text,
                    reply_markup=kb.answer_options_kb(q.id)
                )
            else:
                # Для обычных сообщений редактируем текст
                await bot.edit_message_text(
                    chat_id=user_id,
                    message_id=message_id,
                    text=updated_text,
                    reply_markup=kb.answer_options_kb(q.id)
                )
        except Exception as e:
            print(f"Ошибка при обновлении таймера: {e}")
            # Если не удалось обновить, пропускаем итерацию

    current = await state.get_data()
    if current.get("message_id") == message_id:
        try:
            await bot.delete_message(user_id, message_id)
        except:
            pass
        await callback_answer_timeout(bot, user_id, state)

async def callback_answer_timeout(bot: Bot, user_id: int, state: FSMContext):
    data = await state.get_data()
    index = data['question_index']
    await state.update_data(question_index=index + 1)
    await send_question(bot, user_id, state)

@router.callback_query(F.data.startswith('answer_'))
async def answer_question(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split('_')
    q_id = int(data[1])
    chosen = int(data[2])

    context = await state.get_data()
    questions = context['questions']
    index = context['question_index']
    score = context['score']
    is_photo_message = context.get('is_photo_message', False)

    question = next((q for q in questions if q.id == q_id), None)
    if not question:
        await callback.answer("Вопрос не найден.")
        return

    if question.correct_option == chosen:
        score += 1

    await state.update_data(message_id=None)
    await callback.message.edit_reply_markup()

    if index < len(questions) - 1:
        try:
            if is_photo_message:
                await callback.message.edit_caption(
                    caption="Ответ принят! Ожидай следующий вопрос..."
                )
            else:
                await callback.message.edit_text(
                    "Ответ принят! Ожидай следующий вопрос..."
                )
        except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
            await callback.message.answer("Ответ принят! Ожидай следующий вопрос...")

    await asyncio.sleep(1)

    try:
        await callback.message.delete()
    except:
        pass

    await state.update_data(question_index=index + 1, score=score)
    await send_question(bot, callback.message.chat.id, state)

@router.callback_query(F.data == "show_rating")
async def show_rating(callback: CallbackQuery):
    await callback.answer()
    results = await rq.get_top_results()

    if not results:
        await callback.message.answer("Рейтинг пока пуст.")
        return

    text = "🏆 Топ-3 участника викторины:\n\n"
    for i, r in enumerate(results, start=1):
        name = r.first_name or "Аноним"
        text += f"{i}) {name} — {r.score} из {r.total}\n"

    await callback.message.answer(text)
