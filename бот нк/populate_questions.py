import asyncio
from sqlalchemy import text
from app.database.models import async_session, Question

questions_data = [
    {
        "text": "Сколько лет главный герой потерял на планете с искаженным временем в фильме 'Интерстеллар'?",
        "option_1": "10 лет",
        "option_2": "23 года",
        "option_3": "7 лет",
        "correct_option": 2,
    },
    {
        "text": "Сколько пальцев осталось у главного героя в 'Зеленой миле'?",
        "option_1": "8",
        "option_2": "7",
        "option_3": "6",
        "correct_option": 1,
    },
    {
        "text": "Какой страной правил Алладин?",
        "option_1": "Аграба",
        "option_2": "Фарс",
        "option_3": "Ираклион",
        "correct_option": 1,
    },
    {
        "text": "Общая продолжительность всех фильмов о Гарри Поттере?",
        "option_1": "20 часов 47 минут",
        "option_2": "21 час 43 минуты",
        "option_3": "22 часа 17 минут",
        "correct_option": 1,
    },
    {
        "text": "Из какого фильма этот кадр?",
        "option_1": "Волк с Уолл-стрит",
        "option_2": "Начало",
        "option_3": "Великий Гэтсби",
        "correct_option": 2,
    },
    {
        "text": "Сколько принцесс в Диснее?",
        "option_1": "8",
        "option_2": "10",
        "option_3": "12",
        "correct_option": 3,
    },
    {
        "text": "В какую страну отправился Форрест Гамп в составе сборной США по настольному теннису?",
        "option_1": "Вьетнам",
        "option_2": "Китай",
        "option_3": "Швеция",
        "correct_option": 2,
    },
    {
        "text": "В какой стране снимали 'Бората'?",
        "option_1": "Румыния",
        "option_2": "Казахстан",
        "option_3": "Россия",
        "correct_option": 1,
    },
    {
        "text": "Какой фильм был снят в черно-белом цвете, несмотря на существование технологий для цветной съемки?",
        "option_1": "Список Шиндлера",
        "option_2": "Зеленая миля",
        "option_3": "Молчание ягнят",
        "correct_option": 1,
    },
    {
        "text": "Из какого фильма этот кадр?",
        "option_1": "8 миля",
        "option_2": "Крепкий орешек",
        "option_3": "Одержимость",
        "correct_option": 3,
    },
    {
        "text": "Как называется вымышленная страна, где происходит действие в «Холодном сердце»?",
        "option_1": "Эренделл",
        "option_2": "Флори",
        "option_3": "Гримм",
        "correct_option": 1,
    },
    {
        "text": "Какой предмет есть в каждой сцене «Бойцовского клуба»?",
        "option_1": "Банка Coca-cola",
        "option_2": "Бутылка Pepsi",
        "option_3": "Стаканчик Starbucks",
        "correct_option": 3,
    },
    {
        "text": "Сколько номинаций на Оскар было у фильма 'Титаник'?",
        "option_1": "11",
        "option_2": "14",
        "option_3": "15",
        "correct_option": 2,
    },
    {
        "text": "Сколько колец было создано в трилогии 'Властелин колец'?",
        "option_1": "9",
        "option_2": "3",
        "option_3": "20",
        "correct_option": 3,
    },
    {
        "text": "Из какого фильма этот кадр?",
        "option_1": "Звёздные войны. Эпизод III: Месть ситхов",
        "option_2": "Звёздные войны. Эпизод IV: Новая надежда",
        "option_3": "Звёздные войны. Эпизод V: Империя наносит ответный удар",
        "correct_option": 2,
    },
]

async def populate():
    async with async_session() as session:
        await session.execute(text("DELETE FROM questions;"))

        for q in questions_data:
            session.add(Question(
                text=q["text"],
                option_1=q["option_1"],
                option_2=q["option_2"],
                option_3=q["option_3"],
                correct_option=q["correct_option"],
                image_path=q.get("image_path")
            ))
        await session.commit()
    print("✅ Вопросы обновлены.")

if __name__ == "__main__":
    asyncio.run(populate())
