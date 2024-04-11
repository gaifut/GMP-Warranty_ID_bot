[вернуться в основной Readme файл](https://github.com/gaifut/GMP-Warranty_ID_bot/blob/main/README.md).

Оглавление:
-[Информация по использованию работающей версии бота.](#-Информация-по-использованию-работающей-версии-бота)


## Информация по использованию работающей версии бота.
В данный момент бот запущен и любой может протестировать его в телеграме: @Gmach_helpdesk_bot.
При заходе в бота есть меню, в котором 2 кнопки:
- /start (отвечает за запуск бота)
- /help (содержит краткое описание возможностей бота)

Любой может протестировать бота, следуя пошаговым инструкциям и нажимая на inline клавиатуру.
Для реализации запросов бот будет запрашивать ID поставок ЗЧ (запасных частей) либо ID рекламаций. Ниже несколько примеров ID, которые вернут разные статусы.
### Рабочие примеры ID рекламаций:
 - Em0042205002S2104
   Данный id не является ID рекламации, поэтому бот вернет сообщение об ошибке.
 - Qu079220223W0C
   Бот вернет статус: Ожидается ответ производителя по рекламации
 - Em003280922W1C
   Бот вернет статус: Груз доставлен заказчику 01.02.2023
Чтобы проверить несколько рекламаций можно после получения статуса о рекламации вводить следующий интересующий ID.
### Рабочие примеры ID поставок:
 - Em0042205002S2104
   Бот вернет статус: Груз предеан заказчику.
 - Em003280922W1C
   Данный id не является ID поставки, поэтому бот вернет сообщение об ошибке.
 - RO0772202302S2102
   Бот вернет статус: Груз на складе поставщика. Ожидание оплаты.
   
Для того, чтобы с ID рекламаций перейти в ID поставок необходимо перезапустить бота командой /start

## Реализация.
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

## Как скачать и запустить.
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
