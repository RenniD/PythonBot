from telegram import InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import sqlite3

# Стадії конверсії
CRYPTOCURRENCY, PAYMENT, FINISH = range(3)

appLication = Application.builder().token('8182581834:AAFXBuRAOexW7GH7W40q4_FIkPrYJnGJ4jo').build()



def setup_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Створення таблиці користувачів
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cryptocurrency INTEGER NOT NULL,
        created_ad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    connection.commit()
    connection.close()
    print('База даних успішно налаштована.')

def add_user(username, chat_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f'Користувач {username} успішно доданий.')
    except sqlite3.Error as e:
        print(f'Помилка при додаванні користувача: {e}')
    finally:
        connection.close()

def add_buy(chat_id, cryptocurrency):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            cursor.execute("""
           INSERT INTO buy (user_id, cryptocurrency) VALUES (?, ?)
              """, (user_id, cryptocurrency))
            connection.commit()
            print('Криптовалюта успішно отримано')
        else:
            print('Користувача не знайдено в базі.')
    except sqlite3.Error as e:
        print(f'Помилка при додаванні Криптовалюти: {e}')
    finally:
        connection.close()

def set_user_currency(currency_code):
    """
    Зберігає або оновлює основну валюту користувача.

    :param currency_code: Код валюти ('USD')
    """
    # Підключення до бази даних
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Створюємо таблицю, якщо вона ще не існує
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_currency (
            user_id INT PRIMARY KEY,
            currency_code TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

        # Команда /start с приветсвенным сообщением и кнопками
async def start_command(update, context):
    username = update.effective_user.username or "NoUsername"
    chat_id = update.effective_user.id


    # Додавання користувача в базу даних
    add_user(username, chat_id)
    await update.message.reply_text('Добро пожаловать в КриптоБот! \n'
                                '/help - Более подробно ознакомится с ботом! \n', )

async def cryptocurrency(update, context):
    chat_id = update.effective_user.id
    context.user.data['cryptocurrency'] = update.message.text

    # Збереження купівлі криптовалюти в базі
    add_buy(
        chat_id,
        context.user_data['cryptocurrency']
    )



async def menu(update, context) :
    inline_keyboard = [
        [InlineKeyboardButton( 'Купить криптовалюту' , callback_data='buy')],
        [InlineKeyboardButton('пока недоступнно', callback_data='help')],
        [InlineKeyboardButton('пока недоступнно', callback_data='donate')],
        [InlineKeyboardButton('пока недоступнно', callback_data='shop')]]


    markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(        'Добро пожаловать в КриптоБот! \n'
        '/help - Более подробно ознакомится с ботом! \n',        reply_markup=markup)

#  Обработчик действий с кнопок
async def button_handler(update, context) :
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        await query.message.reply_text(
            "Для покупки криптовалюты напишите название например(Bitcoin,Ethereum,DogeCoin,Cronos "
        )
        return cryptocurrency
    if query.data == 'help':
       await query.messeage.reply_text(           'Доступные команды \n'
           '/shop \n'           '/menu  \n'
           '/info  \n'           '/pay  \n'
           '/sell \n'           '/buy  \n')
    elif query.data == 'donate':
        await query.message.reply_text(
            'Поддержать создателя бота - 456789098765 карта')
    elif query.date == 'shop' :
        await query.message.reply_text(            'позвляет просмотреть криптовалюту в продаже')

async def help(update, context):   await update.message.reply_text(
           'Доступные команды \n'           '/shop \n'
           '/menu  \n'           '/info  \n'
           '/pay  \n'           '/sell \n'
           '/buy  \n')

# Сбор данных для крипты
async def CRYPTOCURRENCY(update, context):
    context.user_data['CRYPTOCURRENCY'] = update.message.text
    await update.message.reply_text("Введите количество которое вы хотите купить криптовалюты")
    return PAYMENT

async def PAYMENT(update, context):
    context.user_data['PAYMENT'] = update.message.text
    await update.message.reply_text("Оплатите сумму за приобритение криптовалюты \n"
                                    "Номер карты - 456789098765 \n"
                                    "И отправьте скриншот оплаты")
    return FINISH

async def FINISH(update, context):
    context.user_data['FINISH'] = update.message.text
    await update.message.reply_text("Модераторы проверят оплату в течении 5 минут \n"
                                    "Если все правильно вам автоматически зачислят вашу криптовалюту")

 


async def info(update, context):
    await update.message.reply_text(
            'Бот создан для криптовалют' )
async def shop(update, context):
    await update.message.reply_text(
           'позвляет просмотреть криптовалюту в продаже')
async def pay(update, context):
    await update.message.reply_text(
       'оправить криптовалюту определеному пользователю')
async def sell(update, context):
    await update.message.reply_text(
       'продать криптовалюту онлайн пользователям')
async def buy(update, context):
    await update.message.reply_text(
       'купить криптовалюту' )
async def donate(update, context):
    await update.message.reply_text(
       'Поддержать создателя бота - 456789098765 карта' )
async def bitcoin(update, context):
    await update.message.reply_text(
       'bitcoin' )



# Додавання обробника команди
appLication.add_handler(CommandHandler("start", start_command))
appLication.add_handler(CommandHandler("help", help))
appLication.add_handler(CommandHandler("shop", shop))
appLication.add_handler(CommandHandler("menu", menu))
appLication.add_handler(CommandHandler("info", info))
appLication.add_handler(CommandHandler("pay", pay))
appLication.add_handler(CommandHandler("sell", sell))
appLication.add_handler(CommandHandler("buy", buy))
appLication.add_handler(CommandHandler("donate", donate))
appLication.add_handler(CommandHandler("bitcoin", bitcoin))
appLication.add_handler(CallbackQueryHandler(button_handler))


async def photo(update,context):
    # Шляхи до локальних файлів
      photo_paths = ['Image/bitcoin.jpg', 'Image/Buy.png' , 'Image/CryptoBot.jpg' , 'Image/Cryptocurrency.jpg' ,
                  'Image/Donate.jpg' ,  'Image/info.png',  'Image/Pay.png', 'Image/Sell.jpg' ]

    # Перевірка на існування файлів
      try:
          media_group = [InputMediaPhoto(open(photo, 'rb')) for photo in photo_paths]
          await update.message.reply_media_group(media_group)
          await update.message.reply_text('Приклад')
      except FileNotFoundError as e:
          await update.message.reply_text(f'Помилка: файл {e.filename} не знайдено. ')
      except Exception as e:
          await update.message.reply_text(f'Виникла помилка: {str(e)}')


appLication.add_handler(CommandHandler('photo', photo))


# Ініціалізаців бази даних
setup_database()


#Запуск бота
if __name__ == '__main__':
     appLication.run_polling()







