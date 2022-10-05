import telebot
from datetime import datetime as dt
import logging
import operations as o
from operations import read_csv, tasks
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import stickers as st
import config
from phonebook_bot import choice
bot = telebot.TeleBot(config.TOKEN)
# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора

START, MENU, EDIT, ADD, DELETE, VIEW, SEARCH, SEARCH_MENU, GET_TASK, GET_DATE = range(10)


TIME_NOW = dt.now().strftime('%D_%H:%M')

# функция обратного вызова точки входа в разговор

def start(update, _):
    reply_keyboard = [['👀 VIEW', '📝 ADD','🔎 SEARCH', 'EXIT']]
    markup_key = ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_sticker(update.message.chat.id, st.welcome)
    bot.send_message(update.effective_chat.id,
                     f'Здраствуйте мастер {update.effective_user.first_name}, я Альфред, ваш персональный помощник')

    update.message.reply_text(
        'Добро пожаловать в ToDoList. Чем займёмся? 🧐\nвведите ''/cancel'' для выхода', reply_markup=markup_key)
    return MENU
def main_menu():
    return MENU

def menu(update, _):
    choice = update.message.text
    if choice == '👀 VIEW':
        return view(update, _)
    if choice == '📝 ADD':
        update.message.reply_text('Введите задачу сэр: ')
        return ADD
    if choice == '🔎 SEARCH':
        bot.send_sticker(update.message.chat.id, st.listen)
        bot.send_message(update.effective_chat.id,
                     f'Что бы вы хотели найти, Мастер {update.effective_user.first_name}: ')
        return SEARCH
    if choice == 'EXIT':
        return cancel(update, _)

def view(update, _):
    user = update.message.from_user
    logger.info("Контакт %s: %s", user.first_name, update.message.text)
    bot.send_sticker(update.message.chat.id, st.view_sticker)
    bot.send_message(update.effective_chat.id,
                     f'Давайте-ка взглянем на список задач мастер {update.effective_user.first_name} ⬇⬇⬇')
    tasks = read_csv()
    tasks_string = o.view_tasks(tasks)
    update.message.reply_text(tasks_string)
    return start(update, _)



def add(update, _):
    tasks = read_csv()
    task = {}
    user = update.message.from_user
    logger.info("Task %s: %s", user.first_name, update.message.text)
    name = update.message.text
    task['Имя'] = user.first_name
    task['Фамилия'] = user.last_name
    task['Текущая дата'] = TIME_NOW
    task['Дата выполнения'] = 'НУЖНО СДЕЛАТЬ'
    task['Задача'] = name
    tasks.append(task)
    o.write_csv(tasks)
    return start(update, _)


def search(update, _):
    tasks = o.read_csv()
    searchstring = update.message.text
    searched_tasks = o.search_task(searchstring, tasks)
    if len(searched_tasks) > 1:
        update.message.reply_text('Укажите более точный запрос')
        return
    if len(searched_tasks) == 1:
        bot.send_message(update.effective_chat.id,
                     f'{update.effective_user.first_name}, по вашему запросу <{searchstring}> найдено ⬇')
        tasks_string = o.view_tasks(searched_tasks)
        update.message.reply_text(tasks_string)
        reply_keyboard = [['❌ DELETE', '✍ EDIT']]
        markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        bot.send_sticker(update.message.chat.id, st.hello)
        update.message.reply_text('Выберите операцию с контактом: 🧐\nвведите ''/cancel'' для выхода', reply_markup=markup_key)
        return SEARCH_MENU
    if len(searched_tasks) == 0:
        update.message.reply_text(f'{len(searched_tasks)} элементов найдено')
        update.message.reply_text('Укажите более точный запрос')
        return
    return start(update, _)


def search_menu(update, _):
    choice = update.message.text
    if choice == '❌ DELETE':
        return delete(update, _)
    if choice == '✍ EDIT':
        return EDIT

def delete(update, _):
  
    o.delete_task()
    o.write_csv(tasks)
    bot.send_sticker(update.message.chat.id, st.complete)
    update.message.reply_text('Задача вычеркнута, сэр')
    return start(update, _)


def edit(update, context):
    pass

def get_info(update, context):
    print('1')
    user = update.message.from_user
    logger.info("Ввод данных %s: %s", user.first_name, update.message.text)
    info = update.message.text
    context.user_data['info'] = info
    return 


def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    bot.send_sticker(update.message.chat.id, st.goodbye)
    bot.send_message(update.effective_chat.id,
                     f'До новых встреч, мастер {update.effective_user.first_name}. 👋')
    update.message.reply_text(
        'Вы знаете где меня найти.',)
    bot.send_sticker(update.message.chat.id, st.relax)
    return ConversationHandler.END


if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler`
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    game_conversation_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            VIEW: [MessageHandler(Filters.text, view)],
            START: [CommandHandler('start', start)],
            ADD: [MessageHandler(Filters.text, add)],
            DELETE: [MessageHandler(Filters.text, delete)],
            SEARCH_MENU: [MessageHandler(Filters.text, search_menu)],
            SEARCH: [MessageHandler(Filters.text, search)],
            MENU: [MessageHandler(Filters.text, menu)],
           

        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(game_conversation_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
