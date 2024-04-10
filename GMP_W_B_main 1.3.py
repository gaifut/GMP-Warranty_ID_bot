import logging
import os
import time

import gspread
import pandas as pd
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

import sensitive as s
import definitions as d

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot_username = os.getenv('bot_username')
bot_name = os.getenv('bot_name')
Google_sheets_API_details = os.getenv('Google_sheets_API_details')
FEEDS = os.getenv('FEEDS')
DRIVE = os.getenv('DRIVE')


# connect to Google Sheets
sa = gspread.service_account(filename=Google_sheets_API_details)
sheet_connect = sa.open(d.workbook_name)
# wks stands for worksheet
wks = sheet_connect.worksheet(d.worksheet_name)
scope = [FEEDS, DRIVE]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    Google_sheets_API_details, scope)
gc = gspread.authorize(credentials)

# Configure logging
logging.basicConfig(filename=d.logs_filename, level=logging.INFO)

# timeout
bot_timeout = d.session_timeout

# Accessing warranty table
data_W = pd.read_excel(s.excel_file_location_W, sheet_name='Гарантийные')
df_W = pd.DataFrame(data_W)
df_W.set_index(['Наш ID'], inplace=True)

# Accessing spare parts table
data_S = pd.read_excel(s.excel_file_location_S, sheet_name='Поставки на нас')
df_S = pd.DataFrame(data_S)
df_S.set_index(['ID'], inplace=True)


# Human-bot interaction
async def set_bot_commands():
    commands = [
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Показать информацию")
    ]
    await bot.set_my_commands(commands)

# Bot info
bot = Bot(API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# keyboard
keyboard_inline = InlineKeyboardMarkup().add(d.button1).add(d.button2)


@dp.message_handler(commands=['help'], state='*')
async def help_message(message: types.Message):
    await message.answer(d.help_intro)


@dp.message_handler(commands=['start'], state='*')
async def choose_inquiry(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.reset_state()
    await state.update_data(session_start_time=time.time())
    await state.update_data(query_count=0)
    await state.update_data(user_no=user_id)
    user_name = message.from_user.first_name
    logging.info(f'{user_id} {user_name} {time.asctime()}')
    await message.answer(
        text=f"{user_name}, {d.introduction}", reply_markup=keyboard_inline)

    data_start_handler_time = await state.get_data()
    session_start_time = data_start_handler_time.get("session_start_time")
    if time.time() - session_start_time > d.session_timeout:
        await message.answer(d.session_timeout_message)
        await state.finish()
        return


@dp.callback_query_handler(
        lambda call: call.data in ['warranty', 'spareparts_sales'])
async def inline_buttons_handler(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)
    if call.data == 'warranty':
        await state.update_data(warranty_chosen=call.data)
        await call.message.answer(d.enter_warranty_ID)
        await d.Warranty_state.provide_ID.set()
    elif call.data == 'spareparts_sales':
        await state.update_data(spareparts_sales_chosen=call.data)
        await call.message.answer(d.enter_spareparts_sales_ID)
        await d.Spareparts_sales_state.provide_ID.set()


@dp.message_handler(state=d.Warranty_state.provide_ID)
async def receive_ID_info(message: types.Message, state: FSMContext):
    try:
        # get the current state for query count
        get_current_value_for_query_count = await state.get_data()
        # get the value of the query count from the current state
        # or 0 if it doesnt exist
        query_count = get_current_value_for_query_count.get("query_count", 0)
        if query_count >= d.query_limit:
            await message.answer(d.querry_limit_exceed_message)
            await state.finish()
            return

        await state.update_data(query_count=query_count + 1)
        await state.update_data(provide_ID=message.text)
        warranty_state_dictionary = await state.get_data()
        ID_info_W = (f"{warranty_state_dictionary['provide_ID']}")
        status_W = df_W.loc[f'{ID_info_W}', 'Статус полный для табл']
        status_W_ID_text = (f'По ID {ID_info_W} статус: {status_W}')
        await message.answer(status_W_ID_text)
        await d.Warranty_state.provide_ID.set()
    except KeyError:
        await message.answer(d.error_message)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")
    finally:
        data_receive_ID_info_W_handler_time = await state.get_data()
        session_start_time = data_receive_ID_info_W_handler_time.get(
            "session_start_time")
        print(warranty_state_dictionary)
        wks.append_row(
            [warranty_state_dictionary['user_no'],
             warranty_state_dictionary['provide_ID'],
             warranty_state_dictionary['session_start_time'],
             warranty_state_dictionary['query_count']]
        )
        if time.time() - session_start_time > d.session_timeout:
            await message.answer(d.session_timeout_message)
            await state.finish()
            return
        # If the user enters "/cancel", reset the state and send the menu
        if message.text == "/cancel":
            await state.finish()
            await message.answer("Отменено")


@dp.message_handler(state=d.Spareparts_sales_state.provide_ID)
async def receive_sales_ID_info(message: types.Message, state: FSMContext):
    try:
        # get the current state for query count
        get_current_value_for_query_count = await state.get_data()
        # get the value of the query count from the current state
        # or 0 if it doesnt exist
        query_count = get_current_value_for_query_count.get("query_count", 0)
        if query_count >= d.query_limit:
            await message.answer(d.querry_limit_exceed_message)
            await state.finish()
            return

        await state.update_data(query_count=query_count + 1)
        await state.update_data(provide_ID=message.text)
        spareparts_sales_dictionary = await state.get_data()
        ID_info_S = (f"{spareparts_sales_dictionary['provide_ID']}")
        status_S = df_S.loc[f'{ID_info_S}', 'Статус внешний']
        status_S_ID_text = (f'По ID {ID_info_S} статус: {status_S}')
        await message.answer(status_S_ID_text)
        await d.Spareparts_sales_state.provide_ID.set()
        print(spareparts_sales_dictionary)
        wks.append_row(
            [spareparts_sales_dictionary['user_no'],
             spareparts_sales_dictionary['provide_ID'],
             spareparts_sales_dictionary['session_start_time'],
             spareparts_sales_dictionary['query_count']]
        )
    except KeyError:
        await message.answer(d.error_message)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")
    finally:
        data_receive_ID_info_W_handler_time = await state.get_data()
        session_start_time = data_receive_ID_info_W_handler_time.get(
            "session_start_time")
        if time.time() - session_start_time > d.session_timeout:
            await message.answer(d.session_timeout_message)
            await state.finish()
            return

if __name__ == '__main__':
    executor.start_polling(dp)
