import pandas as pd
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import sensitive as s
import definitions as d

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

# Human-bot interaction

async def startcommand_on_startup():
    await bot.set_my_commands(types.BotCommand("start", "Start the bot"))


@dp.message_handler(commands=['start'])
async def choose_inquiry(message: types.Message, state: FSMContext):
    await state.reset_state()
    user_name = message.from_user.first_name
    await message.answer (text = f"{user_name}, {d.introduction}", reply_markup=keyboard_inline)

@dp.callback_query_handler(lambda call: call.data in ['warranty'])
async def inline_buttons_handler(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    await state.update_data(warranty_chosen=call.data)
    await call.message.answer (d.enter_warranty_ID)
    await d.warranty_state.provide_ID.set()

@dp.message_handler(state=d.warranty_state.provide_ID)
async def receive_ID_info (message: types.Message, state: FSMContext):
    await state.update_data(provide_ID = message.text)
    warranty_state_dictionary = await state.get_data()
    ID_info = (f"{warranty_state_dictionary['provide_ID']}")
    status = df.loc[f'{ID_info}', 'Статус полный для табл']
    status_ID_text = (f'По ID {ID_info} статус: {status}')
    await message.answer (status_ID_text)
    await state.finish()
    
if __name__ == '__main__':
    executor.start_polling(dp)