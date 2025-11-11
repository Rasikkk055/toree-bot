from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# === 🔑 ВСТАВЬ СВОЙ ТОКЕН НИЖЕ ===
TOKEN = "8558518321:AAHpkQXLDKNSiNN6kHdhgCo3m-p6O7SteBY"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ——— Память имён пользователей ———
user_names = {}

# === Состояния ===
class UserState(StatesGroup):
    name = State()

class QuizState(StatesGroup):
    question = State()
    score = State()
    index = State()

# === Главное меню ===
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("📍 Локации", "❓ FAQ")
main_menu.add("📞 Контакты менеджеров", "📢 Новости и акции")
main_menu.add("🧠 Тесты ПДД")

# === Локации ===
loc_menu = ReplyKeyboardMarkup(resize_keyboard=True)
loc_menu.add("Г. Петропавловск", "Г. Астана")
loc_menu.add("Г. Караганда", "Г. Алматы")
loc_menu.add("Г. Степногорск", "Г. Кокшетау")
loc_menu.add("⬅️ Назад")

locations = {
    "Г. Петропавловск": "📍 Адрес города Петропавловск: https://go.2gis.com/ZSran",
    "Г. Астана": "📍 Адрес города Астана: https://go.2gis.com/k5CCG",
    "Г. Караганда": "📍 Адрес города Караганда: https://go.2gis.com/CmN6Z",
    "Г. Алматы": "📍 Адрес города Алматы: https://go.2gis.com/y5G86",
    "Г. Степногорск": "📍 Адрес города Степногорск: https://go.2gis.com/iSqvH",
    "Г. Кокшетау": "📍 Адрес города Кокшетау: https://go.2gis.com/MUsCn"
}

# === Контакты ===
contact_menu = ReplyKeyboardMarkup(resize_keyboard=True)
contact_menu.add("Г. Петропавловск 📞", "Г. Кокшетау 📞")
contact_menu.add("Г. Караганда 📞", "Г. Алматы 📞")
contact_menu.add("Г. Степногорск 📞", "Г. Астана 📞")
contact_menu.add("⬅️ Назад")

contacts = {
    "Г. Петропавловск 📞": "👤 Менеджер Расул\n📍 Петропавловск\n📱 +7 708 820 7632",
    "Г. Кокшетау 📞": "👤 Менеджер Диана\n📍 Кокшетау\n📱 +7 747 693 02 60",
    "Г. Караганда 📞": "👤 Менеджер Шынар\n📍 Караганда\n📱 +7 705 322 09 21",
    "Г. Алматы 📞": "👤 Менеджер Жания\n📍 Алматы\n📱 +7 776 322 0920",
    "Г. Степногорск 📞": "👤 Менеджер Людмила\n📍 Степногорск\n📱 +7 705 596 7310",
    "Г. Астана 📞": "👤 Менеджер Дастан\n📍 Астана\n📱 +7 777 615 8557"
}

# === FAQ ===
faq_text = """
🚗 **Обучение**
1️⃣ С какого возраста можно обучаться?  
➡️ С 17–18 лет.

2️⃣ Сколько длится обучение?  
➡️ От 2,5 месяцев.

3️⃣ Какие категории есть?  
➡️ A, A1, B, C1, C, D, E.

4️⃣ Есть ли онлайн-обучение?  
➡️ Да, у нас есть онлайн-обучение.

5️⃣ Можно ли обучаться сразу на две категории?  
➡️ Да, можно.

💰 **Стоимость и оплата**
1️⃣ Сколько стоит обучение?  
➡️ Зависит от категории — уточните у менеджера.

2️⃣ Можно ли оплатить в рассрочку?  
➡️ Да, есть Kaspi Red и Kaspi рассрочка.

3️⃣ Входит ли книга ПДД и тесты?  
➡️ Да, включены.

📋 **Документы и экзамены**
1️⃣ Какие документы нужны?  
➡️ Только удостоверение личности.

2️⃣ Где пройти медосмотр?  
➡️ В нашем офисе.

3️⃣ Что делать, если не сдал с первого раза?  
➡️ Не расстраивайтесь — со второго раза всё получится! 😊
"""

# === Новости ===
news_text = """📢 *Новости и акции автошколы*  
На данный момент специальных акций или скидок нет.  
Следите за обновлениями — новые предложения появляются регулярно! 🚗💨"""

# === Тест ПДД ===
pdd_questions = [
    ("⚠️ Что обозначает знак 'Пешеходный переход'?", ["Опасный участок дороги", "Пешеходный переход", "Парковка запрещена"], 1),
    ("⚠️ Что означает знак 'Дети'?", ["Ограничение скорости", "Движение запрещено", "Будьте внимательны — дети"], 2),
    ("⚠️ Какой знак предупреждает о железнодорожном переезде без шлагбаума?", ["Скользкая дорога", "Переезд без шлагбаума", "Стоянка запрещена"], 1),
    ("🚫 Что означает знак 'Въезд запрещён'?", ["Ограничение скорости", "Движение запрещено", "Въезд запрещён"], 2),
    ("🚫 Что означает знак 'Стоянка запрещена'?", ["Стоянка запрещена", "Движение запрещено", "Пешеходный переход"], 0),
    ("🚫 Знак 'Обгон запрещён' означает:", ["Можно обгонять", "Обгон запрещён", "Стоянка разрешена"], 1),
    ("🔵 Что означает знак 'Движение прямо'?", ["Разворот разрешён", "Движение только прямо", "Пешеходный переход"], 1),
    ("🔵 Что обозначает знак 'Поворот направо'?", ["Поворот направо обязателен", "Разворот запрещён", "Стоянка разрешена"], 0),
    ("🔵 Что означает знак 'Круговое движение'?", ["Объезд препятствия", "Движение по кругу", "Движение запрещено"], 1),
    ("ℹ️ Что означает знак 'Зона отдыха'?", ["Зона отдыха", "Опасный участок", "Сужение дороги"], 0),
    ("ℹ️ Что обозначает знак 'АЗС'?", ["Пункт питания", "Автозаправочная станция", "Туалет"], 1),
    ("ℹ️ Что означает знак 'Место стоянки'?", ["Запрещено останавливаться", "Место для парковки", "Пешеходная зона"], 1)
]

# === Команда /start ===
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    user_id = msg.from_user.id

    if user_id in user_names:
        name = user_names[user_id]
        await msg.answer(f"👋 Привет снова, {name}!\nРад видеть вас в автошколе «ТӨРЕ» 🚗", reply_markup=main_menu)
    else:
        await msg.answer(
            "👋 Здравствуйте, мой дорогой клиент!\n"
            "Я бот автошколы **«ТӨРЕ»** 🤖\n"
            "Подскажите, пожалуйста, как могу к вам обращаться? 🙂",
            parse_mode="Markdown"
        )
        await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_name(msg: types.Message, state: FSMContext):
    name = msg.text
    user_id = msg.from_user.id
    user_names[user_id] = name
    await msg.answer(f"Приятно познакомиться, {name}! 👋\nТеперь выберите нужный раздел ниже 👇", reply_markup=main_menu)
    await state.finish()

# === Обработчики меню ===
@dp.message_handler(lambda m: m.text == "📍 Локации")
async def show_locations(msg: types.Message):
    await msg.answer("Выберите ваш город:", reply_markup=loc_menu)

@dp.message_handler(lambda m: m.text in locations)
async def send_location(msg: types.Message):
    await msg.answer(locations[msg.text])

@dp.message_handler(lambda m: m.text == "❓ FAQ")
async def show_faq(msg: types.Message):
    await msg.answer(faq_text, parse_mode="Markdown")

@dp.message_handler(lambda m: m.text == "📞 Контакты менеджеров")
async def show_contacts(msg: types.Message):
    await msg.answer("Выберите город:", reply_markup=contact_menu)

@dp.message_handler(lambda m: m.text in contacts)
async def send_contact(msg: types.Message):
    await msg.answer(contacts[msg.text])

@dp.message_handler(lambda m: m.text == "📢 Новости и акции")
async def show_news(msg: types.Message):
    await msg.answer(news_text, parse_mode="Markdown")

# === Тест ПДД ===
@dp.message_handler(lambda m: m.text == "🧠 Тесты ПДД")
async def start_quiz(msg: types.Message, state: FSMContext):
    await state.update_data(score=0, index=0)
    await send_question(msg, state)

async def send_question(msg, state):
    data = await state.get_data()
    index = data.get("index", 0)

    if index < len(pdd_questions):
        q, options, correct = pdd_questions[index]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for opt in options:
            keyboard.add(opt)
        await msg.answer(q, reply_markup=keyboard)
        await QuizState.question.set()
    else:
        score = data.get("score", 0)
        total = len(pdd_questions)
        percent = int((score / total) * 100)
        result_text = f"✅ Вы ответили правильно на {score} из {total} вопросов ({percent}%).\n"

        if percent >= 80:
            result_text += "Отличный результат! 💪"
        elif percent >= 50:
            result_text += "Хорошо, но можно лучше 🙂"
        else:
            result_text += "Нужно немного подтянуть теорию 🚗"

        again_menu = ReplyKeyboardMarkup(resize_keyboard=True)
        again_menu.add("🔁 Пройти тест заново", "🏠 Главное меню")
        await msg.answer(result_text, reply_markup=again_menu)
        await state.finish()

@dp.message_handler(lambda m: m.text == "🔁 Пройти тест заново")
async def repeat_quiz(msg: types.Message, state: FSMContext):
    await start_quiz(msg, state)

@dp.message_handler(lambda m: m.text == "🏠 Главное меню")
async def back_to_menu(msg: types.Message):
    await msg.answer("Возвращаю вас в главное меню:", reply_markup=main_menu)

@dp.message_handler(state=QuizState.question)
async def process_answer(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    index = data.get("index", 0)
    score = data.get("score", 0)
    q, options, correct = pdd_questions[index]

    if msg.text == options[correct]:
        await msg.answer("✅ Правильно!")
        score += 1
    else:
        await msg.answer(f"❌ Неправильно. Правильный ответ: {options[correct]}")

    await state.update_data(score=score, index=index + 1)
    await send_question(msg, state)

@dp.message_handler(lambda m: m.text == "⬅️ Назад")
async def go_back(msg: types.Message):
    await msg.answer("Главное меню:", reply_markup=main_menu)

# === Запуск ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
