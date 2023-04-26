from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import psycopg2

import db_processor

tgToken = '5854604871:AAEA_v6nr1SSi_rMSS5fka2yyV3eAHGgtFQ'
bot = Bot(token=tgToken)
dp = Dispatcher(bot, storage= MemoryStorage())

#connection to database
conn = psycopg2.connect(
    host="localhost",
    database="DBot",
    user="postgres",
    port="5433",
    password="5441"
)

@dp.message_handler(commands=['start'])
async def processStartCommand(message: types.Message):
    kb = [
        [types.KeyboardButton(text="CREATE")],
        [types.KeyboardButton(text="SELECT")],
        [types.KeyboardButton(text="UPDATE")],
        [types.KeyboardButton(text="DELETE")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Введите желаемое действие"
    )

    await message.answer(
        'Привет, я - бот, который реализует CRUD к выбранной таблице',
        reply_markup=keyboard)

class Form(StatesGroup):
    cr = State()
    sel = State()
    upd = State()
    dl = State()

@dp.message_handler(state = Form.cr)
async def creator(message: types.Message, state: FSMContext):
    await state.finish()
    data = message.text
    try:
        data = data.split(" ")
        id = int(data[0])
        age = int(data[2])
        db_processor.insert(id, data[1], age, conn)
        await message.answer('Done!')
    except Exception as e:
        await message.answer(e)

@dp.message_handler(state = Form.sel)
async def reader(message: types.Message, state: FSMContext):
    await state.finish()
    data = message.text
    try:
        if data == '*':
            temp = db_processor.select_all(conn)
            for i in range(len(temp)):
                await message.answer(f'Id: {temp[i][0]}, Имя: {temp[i][1]}, Возраст: {temp[i][2]}')
        else:
            id = int(data)
            temp = db_processor.select(id, conn)
            await message.answer(f'Id: {temp[0][0]}, Имя: {temp[0][1]}, Возраст: {temp[0][2]}')
    except Exception as e:
        await message.answer(e)
        await message.reply('Произошла ошибка, попробуйте еще раз')

@dp.message_handler(state = Form.upd)
async def updater(message: types.Message, state: FSMContext):
    await state.finish()
    data = message.text
    try:
        data = data.split(" ")
        id = int(data[0])
        age = int(data[2])
        db_processor.update(id, data[1], age, conn)
        await message.answer('Done!')
    except Exception as e:
        await message.answer(e)
        await message.reply('Произошла ошибка, попробуйте еще раз')

@dp.message_handler(state = Form.dl)
async def deleter(message: types.Message, state: FSMContext):
    await state.finish()
    data = message.text
    try:
        id = int(data)
        db_processor.delete(id, conn)
        await message.answer('Done!')
    except Exception as e:
        await message.answer(e)
        await message.reply('Произошла ошибка, попробуйте еще раз')

@dp.message_handler(lambda message: message.text =='CREATE')
async def createFunc(message: types.Message):
    await message.answer('Введите параметры для создания записи в таблицы через пробел: id, имя и возраст')
    await Form.cr.set()

@dp.message_handler(lambda message: message.text =='SELECT')
async def selectFunc(message: types.Message):
    await message.answer('Введите id человека, которого хотите увидеть, либо *, если хотите увидеть всех')
    await Form.sel.set()

@dp.message_handler(lambda message: message.text =='UPDATE')
async def updateFunc(message: types.Message):
    await message.answer('Введите id человека для изменения записи в таблице и параметры')
    await Form.upd.set()

@dp.message_handler(lambda message: message.text =='DELETE')
async def deleteFunc(message: types.Message):
    await message.answer('Введите id человека, которого хотите удалить из таблицы')
    await Form.dl.set()

if __name__ == '__main__':
    executor.start_polling(dp)