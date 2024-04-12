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
1. Fork this repository.
2. Clone forked repository.
3. I recommend to install virtual inviroment, it can be done via this command for instance: ```python -m venv venv```
   then you need to activate it with: ```. venv/Scripts/activate``` (for Linux it is ```. venv/bin/activate```, but this project was created on Windows OS)
   to deactivate virtual environment use this command: ```deactivate```.
   It is possible that Windows will give you Scripts error, to fix it:
    - Run PowerShell as administrator (type powershell in the start menu to find it).
    - Enter this command: ```set-executionpolicy remotesigned```
    - Confirm it with Y or Yes once asked to.
    - After this venv activation should start working.
4. Install dependencies from requirements.txt
   ```pip install -r requirements. txt```
5. Create .env file in the same folder where the project is located add the following variables to the file (use real data instead of sample data that is provided below after = sign):
   ```
   API_KEY=123123123:SFDSsdsfgfOYSADBasdas123asdasdAGw
   bot_username=dummy_name_bot
   bot_name=dummy_name_bot
   Google_sheets_API_details=test-name-placeholder.json
   FEEDS=https://spreadsheets.google.com/feeds
   DRIVE=https://www.googleapis.com/auth/drive
   ```
   If you do not want to use some functionality, for example the Google API, then you can simply remove the code responsible for it.

   #### How to register new bot in Telegram:
    1. Go to the telegram application and type @BotFather in the search box.
    2. Click on the menu at the bottom and select Create a new bot or just type /newbot
    3. Write a name for your bot (can be anything).
    4. Write the username for your bot, it must end in bot, for example: ui_bot, salesbot.
       After this, BotFather will give you all the information about your bot, including the API token (as in the example in step 7).
   #### How to establish API connection with Google Sheets.
   1. Go to the link https://console.cloud.google.com/projectcreate
   2. Enter the name of your project to the Project name box and click CREATE.
   3. Enable Google Sheets API by selecting the name of your project at the top of the page to the right of the GoogleCloud logo.
      Next, in the left column, select API, if it is not there, click on MORE PRODUCTS at the bottom, and then go to APIs & Services -> Enabled APIs & Services.
   4. Under APIs & Services in Google Sheets API select CREATE CREDENTIALS, choose Google Sheets API -> Application Data in the opened window and click NEXT.
      Write Service account name (any name as a single word) and click CREATE AND CONTINUE.
      Choose a role - Editor, click CONTINUE and then click DONE.
   5. Now you will need to download credentials, to do this, go to the CREDENTIALS tab in the same Google Sheets API, click on the service account that you just created. In the window that opens, click on the KEYS tab. In it, click ADD KEY, create a new key. For key type select JSON and click CREATE. The file will download to your computer, move it to the same folder where your project is located. Specify the file name in the Google_sheets_API_details variable in your .env file.
   6. Copy the email of your service account (see point 5), go to the Google Sheet that you plan to use to upload data (for this, you can create a new sheet in your regular Google account) and click share. In the window that opens, paste the copied address, make sure that the access level is set to Editor and click Send.
6. Create a file sensitive.py, in which specify the addresses of files with tables. You don’t have to create a separate file; I did the project a long time ago on Windows, so I decided to keep the original logic.
   If you do not want to change the existing logic you can simply follow my structure as in example below:
   ```
   # sensitive.py
   # location paths
   excel_file_location_W = `the path for warranty shipments table is stated here`
   excel_file_location_S = 'the path for normal shipments table is stated here`
   ```
7. Add changes to definitions.py file:
    
   You need to at least override the file and tab names (below line 25 #GENERAL). Depending on the goals of the project, you can also change the name of the buttons and other variables.

8. Run the project from the GMP_W_B_main 1.3.py file (in VSCode, the run hotkey is F5). After this, your telegram bot should start working.
