from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import pandas as pd

import sensitive as s

# Class for FSM Statesgroup
class warranty_state (StatesGroup):
    none = State()
    warranty_chosen = State()
    provide_ID = State()
    get_ID_status = State()

    # Additional variables for each state
    user_no = None
    inquiry_time = None

class spareparts_sales_state (StatesGroup):
    spareparts_sales_chosen = State()
    provide_ID = State()

    # Additional variables for each state
    user_no = None
    inquiry_timestamp = None


# GENERAL
worksheet_name = "Sheet2"
workbook_name = 'Project 1196493'
logs_filename = 'logs_GMP_B-1.log'
introduction = 'Выберите запрос'
enter_warranty_ID = 'Введите ID рекламации'
enter_spareparts_sales_ID = 'Введите ID сделки'
reset = "Данные очищены"
error_message = "Введенный ID не был найден в системе. Проверьте правильность написания и отсутствие пробелов. Вы можете найти ID в ответе сотрудника Гофромашин на ваш запрос по данному случаю. Введите корректный ID."
query_limit = 25
querry_limit_exceed_message = "Вы сделали максимальное количество запросов в данной сессии. Для продолжения запросов нажмите /start"
session_timeout = 1800 #30 minutes in seconds
session_timeout_message = "Время действия вашей сессии истекло, пожалуйста, начните новую сессию, нажав /start"
help_intro = """Это краткая информация по боту:
            - для активации бота нажмите команду /start
            - для того, чтобы выйти из текущего меню или запроса вам также необходимо нажать команду /start"""



# BUTTONS

# button text
button1_text = 'Получить информацию по рекламации'
button2_text = 'Получить статус поставки ЗЧ'
button_back_text = 'Нажмите сюда, чтобы вернуться назад'

# button logic
button1 = InlineKeyboardButton (text = button1_text, callback_data='warranty')
button2 = InlineKeyboardButton (text = button2_text, callback_data='spareparts_sales')
button_back = InlineKeyboardButton (text = button_back_text, callback_data = 'back_button')
