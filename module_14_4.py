                               # Задача "Продуктовая база":

# В самом начале запускайте ранее написанную функцию get_all_products.

from crud_functions import get_all_products
product = get_all_products()


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())



kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(KeyboardButton('Рассчитать'),KeyboardButton('Информация'))
kb.row(KeyboardButton('Купить'))



ki = InlineKeyboardMarkup()
i_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
ki.add(i_button1,i_button2)




ki_buy = InlineKeyboardMarkup()
for i in range(1, 5):
    buy_button = InlineKeyboardButton(text=f'Product{i}', callback_data='product_buying')
    ki_buy.add(buy_button)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет. Я бот, помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def  main_menu(message):
    await message.answer(text='Выберите опцию', reply_markup=ki)


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')


# Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов
# функцию get_all_products. Полученные записи используйте в выводимой надписи: \
# "Название: <title> | Описание: <description> | Цена: <price>"

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        with open(f'Pictures/{i}.jpg','rb') as img:
            await message.answer(f'*Название*:{product[i][0]} , *Описание*: {product[i][1]} , *Цена*: {product[i][2]} руб',
                                 parse_mode="Markdown")
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=ki_buy)


@dp.callback_query_handler(text='product_buying')
async def set_age(call):
    await call.message.answer('Вы успешно приобрели продукт')


@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growht(message, state):
    await state.update_data(age=int(message.text))
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer(f"Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    calories = 10*(data['weight']) + 6*(data['growth']) - 5*(data['age']) + 5

    await message.answer(f"Ваша норма калорий = {calories}")
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start')


if __name__ == '__main__':
    executor. start_polling(dp, skip_updates=True)


















