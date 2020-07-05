import telebot
import conditions
import startCards
import config
import random


class Registration:
    started_in_chats = []

    def start(self, chat_id):
        in_list = False
        for status in self.started_in_chats:
            if chat_id in status:
                in_list = True
                status[chat_id] = True
        if not in_list:
            self.started_in_chats.insert(len(self.started_in_chats), {chat_id: True})

    def stop(self, chat_id):
        for status in self.started_in_chats:
            if chat_id in status:
                status[chat_id] = False

    def status(self, chat_id):
        try:
            for status in self.started_in_chats:
                if chat_id in status:
                    return status[chat_id]
        except IndexError or KeyError:
            return False


bot = telebot.TeleBot(config.token)
bot_name = 'Bunker Bot'
markdown = """
        *bold text*
        """
users = []
reg = Registration()


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Привет, я бот для игры в бункер. \nЧто бы поиграть, добавь бота в чат и введи команду /reg_start для регистрации и /reg_end или /game_start для начала игры.\n Для отмены регистрации можешь ввести /reg_cancel ')


@bot.message_handler(commands=['game_start', 'reg_end'])
def game_start(message):
    if reg.status(message.chat.id):
        actual_description = conditions.description[random.randrange(0, len(conditions.description))]['value']
        actual_duration = conditions.duration[random.randrange(0, len(conditions.duration))]['value']
        actual_survivors = conditions.survivors[random.randrange(0, len(conditions.survivors))]['value']
        actual_area = conditions.area[random.randrange(0, len(conditions.area))]['value']
        actual_first_stock = conditions.stock[random.randrange(0, len(conditions.stock))]['value']
        actual_second_stock = conditions.stock[random.randrange(0, len(conditions.stock))]['value']
        bot.send_message(message.chat.id, f'*Катастрофа*: {actual_description}\n'
                                          f'*Длительность*: {actual_duration}\n'
                                          f'*Количество выживших*: {actual_survivors}\n'
                                          f'*Площадь бункера*: {actual_area}\n'
                                          f'*Дополнительно*: {actual_first_stock}, {actual_second_stock}',
                         markdown, parse_mode="Markdown")
        reg.stop(message.chat.id)
        for user_chat in users:
            for chat_id in user_chat:
                for user_id in user_chat[chat_id]:
                    user_first_action = startCards.actions[random.randrange(0, len(startCards.actions))]['value']
                    user_second_action = startCards.actions[random.randrange(0, len(startCards.actions))]['value']
                    user_profession = startCards.professions[random.randrange(0, len(startCards.professions))]['value']
                    user_gender = startCards.gender[random.randrange(0, len(startCards.gender))]['value']
                    user_age = random.randrange(14, 95)
                    user_health = startCards.health[random.randrange(0, len(startCards.health))]['value']
                    user_phobia = startCards.phobias[random.randrange(0, len(startCards.phobias))]['value']
                    user_hobby = startCards.hobbies[random.randrange(0, len(startCards.hobbies))]['value']
                    user_character = startCards.character[random.randrange(0, len(startCards.character))]['value']
                    user_baggage = startCards.baggage[random.randrange(0, len(startCards.baggage))]['value']
                    if user_gender == 'Женщина' and user_age > 49 or user_gender == 'Мужчина' and user_age > 60:
                        user_childfree = 'Чайлдфри'
                    else:
                        user_childfree = startCards.childfree[random.randrange(0, len(startCards.childfree))]['value']
                    user_info = startCards.info[random.randrange(0, len(startCards.info))]['value']
                    bot.send_message(user_id, f'Ваши данные для игры в чате: *{message.chat.title}*\n'
                                              f'*Пол, возраст, чайлдфри:* {user_gender}. Возраст: {user_age} лет(года). {user_childfree}\n'
                                                      f'*Профессия*: {user_profession}\n'
                                                      f'*Состояние здоровья*: {user_health}\n'
                                                      f'*Фобия*: {user_phobia}\n'
                                                      f'*Хобби*: {user_hobby}\n'
                                                      f'*Характер*: {user_character}\n'
                                                      f'*Доп.информация*: {user_info}\n'
                                                      f'*Багаж*: {user_baggage}\n'
                                                      f'*Карта действий №1*: {user_first_action}\n'
                                                      f'*Карта действий №2*: {user_second_action}\n',
                                     markdown, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, 'Сначала начните регистрацию командой /reg_start')


# Блок с регистрацией

@bot.message_handler(commands=['reg_start'])
def registration_start(message):
    if not reg.status(message.chat.id):
        reg.start(message.chat.id)
        for user_chat in users:
            try:
                del user_chat[message.chat.id]
            except KeyError:
                pass
        reg_keyboard = telebot.types.InlineKeyboardMarkup()
        reg_button = telebot.types.InlineKeyboardButton(text="Регестрироваться", callback_data='user_info')
        reg_keyboard.add(reg_button)
        bot.send_message(message.chat.id, "Регистрация на игру Бункер начата. Для регистрации нажмите на кнопку снизу.",
                         reply_markup=reg_keyboard, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Регистрация уже начата, вторую начать нельзя 🤷‍♂️\nВы можете отменить регистрацию командой /reg_cancel")


@bot.message_handler(commands=['reg_cancel'])
def registration_cancel(message):
    global users
    global reg
    for user_chat in users:
        try:
            del user_chat[message.chat.id]
        except KeyError:
            pass
    reg.stop(message.chat.id)
    bot.send_message(message.chat.id, "Регистрация завершена, начинайте новую командой /reg_start")


# Ниже будет калбэк регистрации на бункер))0

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global users
    if call.message:
        in_users = False
        for user_chat in users:
            for chat_id in user_chat:
                if chat_id == call.message.chat.id:
                    for user_id in user_chat[chat_id]:
                        if user_chat[chat_id][user_id] == call.from_user.username:
                            in_users = True
                            break
        if call.data == "user_info" and not in_users:
            try:
                bot.send_message(call.from_user.id, 'Вы успешно зарегестрированы в игру "Бункер"')
                users.insert(len(users), {call.message.chat.id:{call.from_user.id: call.from_user.username}})
                reg_keyboard = telebot.types.InlineKeyboardMarkup()
                actual_users = ''
                for user_chat in users:
                    for chat_id in user_chat:
                        if chat_id == call.message.chat.id:
                            for user_id in user_chat[chat_id]:
                                actual_users += user_chat[chat_id][user_id] + '\n'
                reg_button = telebot.types.InlineKeyboardButton(text="Регестрироваться", callback_data='user_info')
                reg_keyboard.add(reg_button)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Регистрация на игру Бункер начата. Для регистрации нажмите на кнопку снизу "
                                           f"\nУчастники: {actual_users}", reply_markup=reg_keyboard)
            except Exception:
                bot.send_message(call.message.chat.id, f'{call.from_user.username}, напишите боту впервые в личные сообщения, прежде, чем начинать игру в "Бункер"!')


if __name__ == '__main__':
    print(f'Бот "{bot_name}" готов к работе.')
    bot.polling(none_stop=True)
