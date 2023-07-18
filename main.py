from sqlite3 import OperationalError

import aiogram.types
from aiogram import executor, types, Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import text, bold
import requests
import asyncio
import aiosqlite
from config import token


class Form(StatesGroup):
    communication_with_operator = State()
    answer_to_users_question = State()
    add_bot_name = State()
    bot_description = State()
    bot_photo = State()
    finish_bot = State()
    bot_functions = State()
    cost_of_bot = State()



bot = Bot(token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

global name
global description
global photo_path
global photo_id
global number_of_the_bot
global functions
global cost_of_the_bot
number_of_the_bot = 0


@dp.message_handler(commands=['start'])
async def startmessage(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Ассортимент🍱')
    button2 = KeyboardButton('Почему мы❓️')
    button2_5 = KeyboardButton('Что мы разрабатываем?')
    button3 = KeyboardButton('Как мы работаем?')
    button4 = KeyboardButton('Связь с админом')
    markup.add(button1, button2)
    markup.add(button2_5)
    markup.add(button3)
    markup.add(button4)
    await bot.send_photo(chat_id=message.chat.id,
                         photo=open('photos/Grasmurr_minimalistic_logo_with_mountains_on_a_'
                                    'white_background_2427829a-beaf-4eec-93a5-e2573e01428b.png', 'rb'),
                         caption=f'{message.from_user.first_name}, Добро пожаловать в магазин ботов '
                                 f'Grasmurr Shop Bots.\n\n'
                                 f'Через него вы можете ознакомиться с ассортиментом ботов, '
                                 f'которые могут помочь вашему бизнесу освоить новые возможности и '
                                 f'потенциально увеличить ваши продажи', reply_markup=markup)


@dp.message_handler(commands=['addbotforexample', 'deletebot'])
async def startmessage(message: Message):
    if message.text == '/addbotforexample':
        await bot.send_message(text='Хорошо! Пришлите ссылку на бота:', chat_id=message.chat.id)
        await Form.add_bot_name.set()
    elif message.text == '/deletebot':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
        markup = InlineKeyboardMarkup()
        m = ''
        n = 1
        buttons = []
        for i in rows:
            m += f'{n}. '
            m += i[0]
            m += '\n\n'
            buttons.append(InlineKeyboardButton(text=f'{n}', callback_data=f'{n}deletebot'))
            n += 1
        for i in buttons:
            markup.add(i)

        await bot.send_message(chat_id=message.chat.id, text=f'Выберите, номер какого бота вы хотите удалить: \n\n{m}', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def messagebuttons(message: Message):
    global photo_id
    if message.text == 'Почему мы❓️':
        await bot.send_message(chat_id=message.chat.id,
                               text='Наша команда состоит из нескольких профессиональных разработчиков, '
                                    'которые выполняют свою работу наилучшим образом.\n\n'
                                    'Нашими преимуществами являются:\n\n'
                                    '—> Большой опыт разработки и знание всех тонкостей, '
                                    'возможностей телеграм ботов\n\n'
                                    '—> Круглосуточная поддержка по всем возникающим вопросам\n\n'
                                    '—> Большой спектр предлагаемых услуг\n\n'
                                    '—> Выполнение работы с учетом специфики вашего бизнеса и конкретных нужд\n\n'
                                    '—> Все проекты имеют простое и понятное техническое задание, '
                                    'заранее обозначенный срок выполнения и бюджет\n\n'
                                    '—> Доводим все проекты до конца, работая “под ключ”, '
                                    'но оставаясь гибкими для правок.')

    elif message.text == 'Связь с админом':
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Связаться с админом через бота', callback_data='communication')
        markup.add(button1)

        await bot.send_message(chat_id=message.chat.id,
                               text='Вы можете позвонить админу Роману по номеру телефона: '
                                    '+79670282821. Или написать в Whatsapp по нему. \n\nТакже, '
                                    'у нас есть и контакт в самом телеграме: @Grasmurr.'
                                    ' \n\nПомимо этого, вы можете нажать на кнопку ниже чтобы'
                                    ' связаться с админом прямо через бота',
                               reply_markup=markup)
    elif message.text == 'Как мы работаем?':
        await bot.send_message(chat_id=message.chat.id,
                               text='''Обычно процесс разработки выглядит следующим образом:\n\n1️⃣ Встреча с заказчиком

Конференция в сети, либо личная встреча. Мы проанализируем Ваш проект, закроем интересующие вопросы и пробелы, дополним его, пользуясь своим опытом. Мы сразу же обозначим точные сроки выполнения и конечную стоимость проекта.

2️⃣ Составление ТЗ

Для крупных проектов - подготавливаем техническое задание, руководствуясь стандартами в работе с этим документом. Для небольших проектов - подготовим упрощенное техническое задание.

3️⃣ Разработка

Наши специалисты разработают ваш проект. Мы работаем, пользуясь высокоуровневыми языками программирования в связке с нейронными сетями, что даст Вам возможность внести правки на любом этапе проекта.

4️⃣ Тестирование

Перед сдачей проекта мы педантично протестируем проект, исключив возможность неполадки и предоставив бессрочную гарантию.

5️⃣ Развертывание

Разворачиваем проекты на партнерских серверах ООО "TimeWeb" со стоимостью хостинга 200 рублей в месяц.

6️⃣ Поддержка

Мы остаемся на короткой ноге с Заказчиком, быстро реагируя на его просьбы и обновляем продукт по мере надобности.''')

    elif message.text == 'Ассортимент🍱':
        global number_of_the_bot
        number_of_the_bot = 0
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]

        await bot.send_message(chat_id=message.chat.id, text='Примеры наших нескольких работ:')
        photo_message = await bot.send_photo(chat_id=message.chat.id, photo=open(rows[0][4], 'rb'))
        photo_id = photo_message.message_id
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Следующая работа', callback_data='nextbot')
        button2 = InlineKeyboardButton(text='Узнать функционал', callback_data='aboutbot')
        button3 = InlineKeyboardButton(text='Заказать похожий', callback_data='orderthebot')
        markup.add(button1)
        markup.add(button2, button3)
        await bot.send_message(chat_id=message.chat.id, text=f'{rows[0][0]}\n\n{rows[0][1]}', reply_markup=markup)

    elif message.text == 'Что мы разрабатываем?':
        await bot.send_message(chat_id=message.chat.id, text='''Мы можем разработать ботов для таких задач, как:
        
- Доставка товаров / цветов / еды

- Чат-бот связанный с сайтом для выгрузки отчетов, показа дополнительной информации и многое другое (html, Css, JavaScript, React)

- Онлайн магазин с корзиной и онлайн оплатой

- Онлайн школа с проверкой домашнего задания

- Воронка прогрева и продажи ваших продуктов 

- FAQ вопросы / Служба поддержки

- Вебинарный чат-бот (прогрев, запись, напоминание, сбор ответов)

- Фитнес тренировки с выдачей полезной информации

- Визитка для записи к вам на прием / занятие / встречу

- Просмотр меню и заказ в кафе / ресторане

- Программа лояльности с реферальными ссылками

- Система пригласи друга и получи подарки и бонусы

- Автоматизация бронирования записи или места

- Неограниченные рассылки по всей базе в чат-боте

- Сегментированные рассылки по интересам вашей аудитории

- Авто напоминание о повторной услуге

- И многое другое''')
    elif message.text == 'Отмена':
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton('Ассортимент🍱')
        button2 = KeyboardButton('Почему мы❓️')
        button2_5 = KeyboardButton('Что мы разрабатываем?')
        button3 = KeyboardButton('Как мы работаем?')
        button4 = KeyboardButton('Связь с админом')
        markup.add(button1, button2)
        markup.add(button2_5)
        markup.add(button3)
        markup.add(button4)

        await bot.send_message(
            text='Хорошо! Вы можете попробовать снова!',
            chat_id=message.chat.id, reply_markup=markup)


@dp.callback_query_handler(lambda c: True)
async def inline_buttons(call: types.CallbackQuery):
    req = call.data
    global photo_id
    global id_of_the_user_to_answer
    global id_of_the_message_to_delete_while_answering
    global number_of_the_bot
    if req == 'communication':
        await bot.edit_message_text(text='Хорошо, отправьте сообщение с вашим вопросом.'
                                    ' Мы постараемся ответить как можно скорее:', chat_id=call.message.chat.id, message_id=call.message.message_id)

        await Form.communication_with_operator.set()
    elif req[-20:] == 'answertousersqustion':
        id_of_the_user_to_answer = int(req[:-20])
        id_of_the_message_to_delete_while_answering = call.message.message_id
        await bot.send_message(text='Хорошо, отправьте сообщение с вашим ответом:', chat_id=call.message.chat.id)
        await Form.answer_to_users_question.set()

    elif req == 'savethebot':
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        await bot.send_message(chat_id=call.message.chat.id, text='Успешно!')

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(
                f'''CREATE TABLE IF NOT EXISTS bots
                    (name TEXT, description TEXT, functions TEXT, cost INT, photo TEXT)''')
            await conn.commit()
            await cur.execute(f'''INSERT OR IGNORE INTO bots (name, description, functions, cost, photo) 
                                  VALUES (?, ?, ?, ?, ?)''', (name, description, functions, cost_of_the_bot, photo_path))
            await conn.commit()

    elif req in ['nextbot', 'previousbot']:
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]


        markup = InlineKeyboardMarkup()
        button0 = InlineKeyboardButton(text='Предыдущая работа', callback_data='previousbot')
        button1 = InlineKeyboardButton(text='Следующая работа', callback_data='nextbot')
        button2 = InlineKeyboardButton(text='Узнать функционал', callback_data=f'{number_of_the_bot}aboutbot')
        button3 = InlineKeyboardButton(text='Заказать похожий', callback_data=f'{number_of_the_bot}orderthebot')
        if req == 'nextbot':
            number_of_the_bot += 1

        elif req == 'previousbot':
            number_of_the_bot -= 1

        if number_of_the_bot == len(rows) - 1:
            markup.add(button0)
            markup.add(button2, button3)
        elif number_of_the_bot == 0:
            markup.add(button1)
            markup.add(button2, button3)
        else:
            markup.add(button0, button1)
            markup.add(button2, button3)

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f'{rows[number_of_the_bot][0]}\n\n{rows[number_of_the_bot][1]}',
                                    reply_markup=markup)
        await bot.edit_message_media(chat_id=call.message.chat.id, message_id=photo_id,
                                     media=types.InputMediaPhoto(media=open(f'{rows[number_of_the_bot][4]}', 'rb')))
    elif req[-9:] == 'deletebot':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]

        bot_to_delete = req[:-9]
        print(bot_to_delete)
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Продолжить', callback_data=f'{bot_to_delete}finaldelete')
        button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
        markup.add(button1, button2)
        await bot.edit_message_text(text=f'Вы уверены, что хотите удалить бота {rows[int(bot_to_delete) - 1][0]}',
                               chat_id=call.message.chat.id, reply_markup=markup, message_id=call.message.message_id)

    elif req[-11:] == 'finaldelete':
        bot_to_delete = req[:-11]
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            name_of_deleting_bot = rows[int(bot_to_delete) - 1][0]
            await cur.execute(f'DELETE FROM bots WHERE name = ?', (name_of_deleting_bot, ))
            await conn.commit()
        await bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text='Успешно!')

    elif req[-8:] == 'aboutbot':
        global the_bot_to_print_about
        the_bot_to_print_about = number_of_the_bot
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]
            the_bot_to_print_about = rows[the_bot_to_print_about]

        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Заказать аналогичного бота', callback_data='orderthebot')
        button2 = InlineKeyboardButton(text='Назад', callback_data='back')

        markup.add(button1)
        markup.add(button2)

        cost = text(bold(f'Стоимость разработки такого бота: от {the_bot_to_print_about[3]} руб'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               text=f'Функционал этого бота следующий:  \n\n{the_bot_to_print_about[2]}\n\n\n' + cost + '.',
                                    parse_mode=types.ParseMode.MARKDOWN, reply_markup=markup)

    elif req[-11:] == 'orderthebot':
        the_bot_to_order = number_of_the_bot

        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]

            the_bot_to_print_about = rows[the_bot_to_order]



        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton(text='Назад', callback_data='back')
        button2 = InlineKeyboardButton(text='Продолжить заказ', callback_data='continueorder')

        markup.add(button1)
        markup.add(button2)

        cost = text(bold(f'Стоимость разработки такого бота: от {the_bot_to_print_about[3]} руб'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'Хорошо! Вы собираетесь заказать аналог бота: {the_bot_to_print_about[0]}\n\n' + cost + '.',
                                    parse_mode=types.ParseMode.MARKDOWN, reply_markup=markup)

    elif req == 'back':
        async with aiosqlite.connect('database.db') as conn:
            cur = await conn.cursor()
            await cur.execute(f'SELECT * FROM bots')
            await conn.commit()
            rows = await cur.fetchall()
            rows = [list(i) for i in rows]

        markup = InlineKeyboardMarkup()
        button0 = InlineKeyboardButton(text='Предыдущая работа', callback_data='previousbot')
        button1 = InlineKeyboardButton(text='Следующая работа', callback_data='nextbot')
        button2 = InlineKeyboardButton(text='Узнать функционал', callback_data=f'{number_of_the_bot}aboutbot')
        button3 = InlineKeyboardButton(text='Заказать похожий', callback_data=f'{number_of_the_bot}orderthebot')

        if number_of_the_bot == len(rows) - 1:
            markup.add(button0)
            markup.add(button2, button3)
        elif number_of_the_bot == 0:
            markup.add(button1)
            markup.add(button2, button3)
        else:
            markup.add(button0, button1)
            markup.add(button2, button3)
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    text=f'{rows[number_of_the_bot][0]}\n\n{rows[number_of_the_bot][1]}',
                                    message_id=call.message.message_id,
                                    reply_markup=markup)

    elif req == 'continueorder':

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton(text='Отправить номер телефона', request_contact=True)
        button2 = KeyboardButton(text='Отмена')
        markup.add(button1)
        markup.add(button2)
        await bot.send_message(text='Для заказа нужно указать ваш номер телефона!\n\n'
                                    'Пожалуйста, нажмите на кнопку ниже чтобы мы получили ваш номер телефона!',
                               chat_id=call.message.chat.id, reply_markup=markup)



    elif req == 'Cancel':
        await bot.edit_message_text(message_id=call.message.message_id,
                                    chat_id=call.message.chat.id,
                                    text='Хорошо, вы можете попробовать снова, нажав на кнопку или введя команду')


@dp.message_handler(content_types=['contact'])
async def phone_number(message: types.Message, state: FSMContext):
    global the_bot_to_print_about
    phone_number = message.contact.phone_number
    await bot.send_message(chat_id=305378717, text=f'Заказ от пользователя {phone_number} на бота: {the_bot_to_print_about[0]}')
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Ассортимент🍱')
    button2 = KeyboardButton('Почему мы❓️')
    button2_5 = KeyboardButton('Что мы разрабатываем?')
    button3 = KeyboardButton('Как мы работаем?')
    button4 = KeyboardButton('Связь с админом')
    markup.add(button1, button2)
    markup.add(button2_5)
    markup.add(button3)
    markup.add(button4)

    await bot.send_message(text='Успешно! Большое спасибо вам за заказ! В ближайшее время админ свяжется с вами!\n\n'
                                'Если есть какие-то моменты, касающиеся связи с вами, например: '
                                'вы хотите заказать звонок вместо сообщения в whatsapp/telegram или что-то еще, то воспользуйтесь связью с оператором через кнопку "Связь с админом"',
                           chat_id=message.chat.id, reply_markup=markup)
    await state.finish()


@dp.message_handler(state=Form.communication_with_operator)
async def communication(message: types.Message, state: FSMContext):
    message_to_operator = message.text
    async with aiosqlite.connect('database.db') as conn:
        cur = await conn.cursor()
        await cur.execute(
            f'''CREATE TABLE IF NOT EXISTS questions
                (id TEXT, message TEXT)''')
        await conn.commit()
        await cur.execute(f'INSERT OR IGNORE INTO questions (id, message)'
                          f'VALUES (?, ?)', (message.from_user.id, message_to_operator,))
        await conn.commit()

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Ответить', callback_data=f'{message.from_user.id}answertousersqustion')
    markup.add(button1)
    await bot.send_message(chat_id=305378717,
                           text=f'Сообщение от пользователя: @{message.from_user.username}\n\n{message_to_operator}',
                           reply_markup=markup)
    await bot.send_message(chat_id=message.chat.id, text='Отправлено!')

    await state.finish()


@dp.message_handler(state=Form.answer_to_users_question)
async def answer_to_user(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=305378717, message_id=id_of_the_message_to_delete_while_answering)
    message_from_operator = message.text
    await bot.send_message(chat_id=id_of_the_user_to_answer, text=f'Ответ от админа:\n\n{message_from_operator}\n\nДля дальнейшей связи вы можете снова нажать на кнопку "Связь с оператором"')
    await bot.send_message(chat_id=305378717, text='Успешно!')
    await state.finish()


@dp.message_handler(state=Form.add_bot_name)
async def add_bot_name(message: types.Message, state: FSMContext):
    global name
    name = message.text
    await bot.send_message(chat_id=message.chat.id, text='Хорошо, теперь отправьте описание бота:')
    await Form.bot_description.set()


@dp.message_handler(state=Form.bot_description)
async def add_bot_name(message: types.Message, state: FSMContext):
    global description
    description = message.text
    await bot.send_message(chat_id=message.chat.id, text=f'Хорошо, теперь отправьте функционал бота:')
    await Form.bot_functions.set()


@dp.message_handler(state=Form.bot_functions)
async def add_bot_name(message: types.Message, state: FSMContext):
    global functions
    functions = message.text
    await bot.send_message(chat_id=message.chat.id, text=f'Хорошо, теперь отправьте стоимость этого бота:')
    await Form.cost_of_bot.set()


@dp.message_handler(state=Form.cost_of_bot)
async def add_bot_cost(message: types.Message):
    global cost_of_the_bot
    cost_of_the_bot = message.text
    await bot.send_message(chat_id=message.chat.id, text=f'Хорошо, теперь отправьте фото для бота:')
    await Form.bot_photo.set()


@dp.message_handler(state=Form.bot_photo, content_types=['photo'])
async def add_bot_name(message: types.Message, state: FSMContext):
    global photo_path
    photo = message.photo[-1].file_id
    file = await bot.get_file(photo)
    response = requests.get(f"https://api.telegram.org/file/bot{token}/{file.file_path}")
    with open(f"photos/{file.file_id}.jpg", "wb") as f:
        photo_path = f"photos/{file.file_id}.jpg"
        f.write(response.content)

    await bot.send_message(chat_id=message.chat.id, text=f'Хорошо, вы отправили следующего бота:')

    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text='Сохранить', callback_data='savethebot')
    button2 = InlineKeyboardButton(text='Отмена', callback_data='Cancel')
    markup.add(button1)
    markup.add(button2)

    await bot.send_photo(chat_id=message.chat.id, photo=open(photo_path, 'rb'), caption=f'\n{name}\n\n{description}', reply_markup=markup)
    await state.finish()

try:
    print('Запускаюсь...')
    executor.start_polling(dp)
except asyncio.TimeoutError as E:
    print('time error, продолжаю работать...')
    executor.start_polling(dp)
