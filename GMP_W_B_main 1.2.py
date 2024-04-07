import pandas as pd
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time


import sensitive as s
import definitions as d


# timeout
bot_timeout = d.session_timeout

# Accessing warranty table
data = pd.read_excel(s.excel_file_location, sheet_name = 'Гарантийные')
df = pd.DataFrame(data)
df.set_index(['Наш ID'], inplace = True)

# Bot info
bot = Bot (s.API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)

# keyboard
keyboard_inline = InlineKeyboardMarkup().add(d.button1)

# Menu
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# Human-bot interaction
async def set_my_commands():
    commands = [
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("menu", "Открыть меню")
    ]
    await bot.set_my_commands(commands)

async def startcommand_on_startup():
    await set_my_commands()
    await dp.start_polling()

@dp.message_handler(commands=['start'])
async def choose_inquiry(message: types.Message, state: FSMContext):
    await state.reset_state()
    await state.update_data(session_start_time=time.time())
    await state.update_data(query_count=0)
    user_name = message.from_user.first_name
    await message.answer (text = f"{user_name}, {d.introduction}", reply_markup=keyboard_inline)

    data_start_handler_time = await state.get_data()
    session_start_time = data_start_handler_time.get("session_start_time")
    if time.time() - session_start_time > d.session_timeout:
        await message.answer(d.session_timeout_message)
        await state.finish()
        return


@dp.callback_query_handler(lambda call: call.data in ['warranty'])
async def inline_buttons_handler(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    await state.update_data(warranty_chosen=call.data)
    await call.message.answer (d.enter_warranty_ID)
    await d.warranty_state.provide_ID.set()

    
@dp.message_handler(state=d.warranty_state.provide_ID)
async def receive_ID_info (message: types.Message, state: FSMContext):
    try:
        get_current_value_for_query_count =  await state.get_data() # get the current state for query count
        query_count = get_current_value_for_query_count.get("query_count", 0) #get the value of the query count from the current state or 0 if it doesnt exist
        if query_count >= d.query_limit:
            await message.answer (d.querry_limit_exceed_message)
            await state.finish()
            return
        
        await state.update_data(query_count=query_count + 1)
        await state.update_data(provide_ID = message.text)
        warranty_state_dictionary = await state.get_data()
        ID_info = (f"{warranty_state_dictionary['provide_ID']}")
        status = df.loc[f'{ID_info}', 'Статус полный для табл']
        status_ID_text = (f'По ID {ID_info} статус: {status}')
        await message.answer (status_ID_text)
        await d.warranty_state.provide_ID.set()
    except KeyError:
        await message.answer(d.error_message)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")
    finally:
        data_creceive_ID_info_handler_time = await state.get_data()
        session_start_time = data_creceive_ID_info_handler_time.get("session_start_time")
        if time.time() - session_start_time > d.session_timeout:
            await message.answer(d.session_timeout_message)
            await state.finish()
            return
        # If the user enters "/cancel", reset the state and send the menu
        if message.text == "/cancel":
            await state.finish()
            await message.answer("Отменено", reply_markup=menu_keyboard)
    
# Handler for the menu
@dp.message_handler(commands=['меню'])
async def show_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=menu_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)