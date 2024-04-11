[return to main Readme file](https://github.com/gaifut/GMP-Warranty_ID_bot/blob/main/README.md).

## Table of contents:
- [What this bot can be used for.](#What-this-bot-can-be-used-for)
- [How to use the version of the bot that is already running.](#How-to-use-the-version-of-the-bot-that-is-already-running)
- [Project Description.](#Project-Description)
- [How to download and set up.](#How-to-download-and-set-up)

## What this bot can be used for.
This bot was made to allow fast tracking of the orders for the customers of Gofromachines Premium. The company uses unique IDs to track all shipments, the tracking is done by supply chain department. To reduce the response time as well as to allow 24/7 monitoring this bot automation was added. The bot opens the file, checks the order status that matches the ID and returns it in response. The information about the inquiry is stored in Google Sheets, which allows to see how many inquries there were, regarding which orders, etc.

The bot can be easily adjusted for simiar use cases, furthremore it can be scaled based on specific needs.

## How to use the version of the bot that is already running.
At the moment the bot is running and anyone can test it in Telegram: @Gmach_helpdesk_bot. It is also possible to [use QR code at Gofromachines website](http://g-mach.ru/servisy-dlya-klientov).
When the bot is started there are 2 options to choose from:
- /start (starts the bot)
- /help (provides an overview of what this bot can do)

Anyone can test the bot following step-by-step instructions and using inline keyboard.
In order to provide infomration the bot will need order IDs (for either shipments or warranty supplies), examples of which are provided below. Please keep in mind that the bot currently uses only the Russian language as that is the primary language of communication for Gofromachines customers.
### Warranty IDs to test the bot:
 - Em0042205002S2104
   This is not actually a warranty ID so the bot will return the error message.
 - Qu079220223W0C
   The bot will return the following status: Ожидается ответ производителя по рекламации
 - Em003280922W1C
  The bot will return the following status: Груз доставлен заказчику 01.02.2023
Чтобы проверить несколько рекламаций можно после получения статуса о рекламации вводить следующий интересующий ID.
### Order IDs to test the bot:
 - Em0042205002S2104
  The bot will return the following status: Груз предеан заказчику.
 - Em003280922W1C
    This is not actually an order ID so the bot will return the error message.
 - RO0772202302S2102
   The bot will return the following status: Груз на складе поставщика. Ожидание оплаты.
   
To switch from order ID statuses to warranty IDs use /start command.

## Project Description.
### Stack:
Python, Pandas, Gspread.
### Step by step program logic.
When received input from the user (either order ID or warranty ID) the bot does the following:
1. Opens a relevant Excel table moves to a designated tab (depending on the inquiry) and finds the value in the status column that matches the ID in question. It looks like this:
   ![Screenshot from 2024-04-11 15-09-46](https://github.com/gaifut/GMP-Warranty_ID_bot/assets/113767276/636d4a85-a217-46cc-90a3-608edfc2deb9)
This happens 'under the hood' using pandas library.
2. If the bot finds the ID, it returns its status to the user, otherwise it returns a message stating as much.
3. The bot connects to the specified Google Sheets using the Google API (gspread library) and records there:
    - id of the user who made the request
    - Order or warranty ID that the user entered
    - request time (computer time, Greenwich, Moscow)
    - request number (counted for each user during 1 session).
   It looks like this:
   ![image](https://github.com/gaifut/GMP-Warranty_ID_bot/assets/113767276/f4000d2b-4894-4da6-9fb1-2050f47fc799)
### Note:
- The maximum number of requests per session = 25; if the limit is exceeded, the bot will ask you to restart it.

## How to download and set up.
#### Важно! Проект делался на Windows, возможны проблемы при запуске на других операционных системах.
1. Fork'ните этот репозиторий.
2. Клонируйте форкнутый репозиторий.
3. Советую установить виртуальное окружение, например так: ```python -m venv venv```
   и далее активируйте его: ```. venv/Scripts/activate``` (для линукса это ```. venv/bin/activate```, но данный проект реализован на Windows)
   для деактивации можно набрать ```deactivate```
   Вероятно, Windows выдаст вам ошибку про Scripts, для ее устранения:
    - Зайдите в PowerShell как администратор (наберите powershell в пуск).
    - Наберите ```set-executionpolicy remotesigned```
    - Вас попросят подтвердить это, укажите Y или Yes.
    - После этого активащия виртуального окружения должна заработать.
5. Установите зависимости из requirements.txt
   ```pip install -r requirements. txt```
7. Создайте .env файл в папке, где находится проект, в него добавьте следующие переменные (ниже указан пример с вымышленными данными):
   ```
   API_KEY=123123123:SFDSsdsfgfOYSADBasdas123asdasdAGw
   bot_username=dummy_name_bot
   bot_name=dummy_name_bot
   Google_sheets_API_details=test-name-placeholder.json
   FEEDS=https://spreadsheets.google.com/feeds
   DRIVE=https://www.googleapis.com/auth/drive
   ```
   Если вы не хотите использовать какую-то функциональность, например Google API, то можно просто убрать код, отвечающий за это.

   #### Как зарегистрировать нового бота в Telegram:
   1. Зайдите в приложение телеграм и в поиске аккаунтов наберите @BotFather.
   2. Внизу кликните на меню и выберите Create a new bot либо просто наберите /newbot
   3. Напишите имя для вашего бота (может быть любым).
   4. Напишите имя пользователя для вашего бота, обязательно должно оканчиваться на bot, например: ui_bot, salesbot.
      После этого BotFather выдаст вам всю информацию о вашем боте, в том числе API токен (как в примере в пункте 7).
   #### Как установить API соединение с Google Sheets.
   1. Зайдите на ссылку https://console.cloud.google.com/projectcreate
   2. В Project name укажите имя вашего проекта и после нажмите кнопку CREATE.
   3. Включите google sheets API, для этого вверху страницы справа от лого GoogleCloud выберите имя вашего проекта. Далее в колонке слева выберите API, если его нет, внизу нажмите на MORE PRODUCTS, и далее зайдите в APIs & Services, перейдите в Enabled APIs & Services.
      На открывшейся странице вверху нажимите + ENABLE APIS AND SERVICES.
      Далее у вас откроется список APIs and Services, вы в нем ищете Google Sheets API и кликаете на него, после чего в открывшемся окне нажимаете ENABLE.
   4. Под APIs & Services в Google Sheets API выберите CREATE CREDENTIALS, в открывшемся окне выберите Google Sheets API и Application Data и нажмите NEXT.
      В открывшемся окне напишите Service account name (любое имя в одно слово) и нажмите CREATE AND CONTINUE.
      Выберите роль - Editor, нажмите CONTINUE и далее нажмите DONE.
   5. Теперь вам необходимо будет загрузить credentials, для этого перейдите в CREDENTIALS вкладку все в том же Google Sheets API, кликните на service account, что вы только что создали. В открывшемся окне нажмите на вкладку KEYS. В ней нажмите ADD KEY, create a new key. Key type   выберите JSON и нажмите CREATE. Файл загрузится на ваш компьютер, перенесите его в ту же папку, где находится ваш проект. Название файла укажите в переменной Google_sheets_API_details в вашем .env файле.
   6. Скопируйте email вашего service account (смотрите пункт 5), зайдите в Google Sheet, который вы планируете использовать для выгрузки данных (для этого в своем обычном гугл аккаунте можно создать новый sheet) и нажмите поделиться (share). В открывшемся окне вставьте скопированный адрес, убедитесь, что уровень доступа указан Editor и нажмите Send.
9. Создайте файл sensitive.py, в котором укажите адреса файлов с таблицами. Вы также можете не создавать отдельный файл, проект я делал давно и на Windows, поэтому оставил именно эту логику.
   Если хотите вносить минимум изменений, мой файл выглядел так:
   ```
   # sensitive.py
   # location paths
   excel_file_location_W = `указывается адрес таблицы для рекламаций`
   excel_file_location_S = `указывается адрес таблицы для обычных поставок`
   ```
10. Внесите изменения в файл definitions.py:

   Как минимум вам необходимо переопредилить названия файлов и вкладок (ниже строки 25 #GENERAL). В зависимости от целей проекта вы также можете изменить здесь название кнопок и прочие переменные.
