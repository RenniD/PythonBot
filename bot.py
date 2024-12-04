
from telegram import  InputMediaPhoto, InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes,  Application

appLication = Application.builder().token('8182581834:AAFXBuRAOexW7GH7W40q4_FIkPrYJnGJ4jo').build()
# Команда /start с приветсвенным сообщением и кнопками
async def start(update, context):
    await update.message.reply_text(
            'Добро пожаловать в бот криптовалют! \n' 
            'Более подробно команда /help')

async def menu(update, context) :
    inline_keyboard = [
        [InlineKeyboardButton('пока недоступнно', callback_data='menu')],
        [InlineKeyboardButton('пока недоступнно', callback_data='donate')],
        [InlineKeyboardButton('пока недоступнно', callback_data='shop')]]
    markup = InlineKeyboardMarkup(inline_keyboard)
    await update.message.reply_text(        'Добро пожаловать в КриптоБот! \n'
        '/help - Более подробно ознакомится с ботом! \n',        reply_markup=markup)

#  Обработчик действий с кнопок
async def button_handler(update, context) :
    query = update.callback_query
    await query.answer()
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

appLication.add_handler(CommandHandler("start", start))
appLication.add_handler(CommandHandler("help", help))
appLication.add_handler(CommandHandler("shop", shop))
appLication.add_handler(CommandHandler("menu", menu))
appLication.add_handler(CommandHandler("info", info))
appLication.add_handler(CommandHandler("pay", pay))
appLication.add_handler(CommandHandler("sell", sell))
appLication.add_handler(CommandHandler("buy", buy))
appLication.add_handler(CommandHandler("donate", donate))
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

 # Додавання обробника команди
appLication.add_handler(CommandHandler('photo', photo))


#Запуск бота
if __name__ == '__main__':
     appLication.run_polling()








