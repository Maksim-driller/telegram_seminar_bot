import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
import json
import csv
class NotesStates(StatesGroup):
    title = State()
    description = State()
    delete = State()
    edit_select = State()
    edit_title = State()
    edit_description  = State()
notes = {}
class TaskStates(StatesGroup):

bot = telebot.TeleBot('7874336513:AAEmXcMaUXzwpYTGIPd3HRJE7Q4lCrJapY4')

def show_main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('1. Управление заметками')
    button2 = types.KeyboardButton('2. Управление задачами')
    button3 = types.KeyboardButton('3. Управление контактами')
    button4 = types.KeyboardButton('4. Управление финансовыми записями')
    button5 = types.KeyboardButton('5. Калькулятор')
    button6 = types.KeyboardButton('6. Выход')
    keyboard.add(button1, button2, button3, button4, button5, button6)
    bot.reply_to(message, '''Добро пожаловать в Персональный помощник! 
    Выберите действие: 
    1. Управление заметками 
    2. Управление задачами 
    3. Управление контактами 
    4. Управление финансовыми записями 
    5. Калькулятор 
    6. Выход''', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def handle_start(message):
    show_main_menu(message)

@bot.message_handler(func=lambda message: message.text == '1. Управление заметками')
def handle_notes(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_notes = types.KeyboardButton('Создать новую заметку')
    button_notes_2 = types.KeyboardButton('Просмотр списка заметок')
    button_notes_3 = types.KeyboardButton('Просмотр подробностей заметки')
    button_notes_4 = types.KeyboardButton('Редактирование заметки')
    button_notes_5 = types.KeyboardButton('Удаление заметки')
    button_notes_back = types.KeyboardButton('Назад в главное меню')
    keyboard.add(button_notes, button_notes_2, button_notes_3, button_notes_4, button_notes_5, button_notes_back)
    bot.reply_to(message, 'Вы выбрали управление заметками. Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Создать новую заметку')
def create_title_notes(message):
    bot.reply_to(message, 'Введи название заметки')
    bot.set_state(message.from_user.id, NotesStates.title, message.chat.id)

@bot.message_handler(state=NotesStates.title)
def get_note_title(message):
    bot.set_state(message.from_user.id, NotesStates.description, message.chat.id)
    bot.reply_to(message, 'Добавь описание заметки')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['title'] = message.text

@bot.message_handler(state=NotesStates.description)
def get_note_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        title = data['title']
        description = message.text
        notes[title] = description
    bot.reply_to(message, f"Заметка '{title}' успешно создана!")
    bot.delete_state(message.from_user.id, message.chat.id)
    handle_notes(message)

@bot.message_handler(func=lambda message: message.text == 'Удаление заметки')
def delete_note_start(message):
    if not notes:
        bot.reply_to(message, "У вас нет сохраненных заметок.")
        handle_notes(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2)
        for title in notes.keys():
            keyboard.add(types.KeyboardButton(title))
        keyboard.add(types.KeyboardButton('Отмена'))
        bot.reply_to(message, "Выберите заметку для удаления:", reply_markup=keyboard)
        bot.set_state(message.from_user.id, NotesStates.delete, message.chat.id)

@bot.message_handler(state=NotesStates.delete)
def delete_note(message):
    if message.text == 'Отмена':
        bot.reply_to(message, "Удаление отменено.")
        bot.delete_state(message.from_user.id, message.chat.id)
        handle_notes(message)
    elif message.text in notes:
        del notes[message.text]
        bot.reply_to(message, f"Заметка '{message.text}' успешно удалена.")
        bot.delete_state(message.from_user.id, message.chat.id)
        handle_notes(message)
    else:
        bot.reply_to(message, "Такой заметки не существует. Попробуйте еще раз или выберите 'Отмена'.")
@bot.message_handler(func=lambda message: message.text == 'Просмотр списка заметок')
def get_all_notes(message):
    if not notes:
        bot.reply_to(message, 'У вас нету заметок')
    else:
        note_list = 'Список ваших заметок: \n\n'
        for i, title in enumerate(notes.keys() ,start = 1 ):
            note_list += f"{i}. {title}\n"
        bot.reply_to(message, note_list)
    handle_notes(message)
@bot.message_handler(func=lambda message: message.text == 'Редактирование заметки')
def edit_note(message):
    if message.text == 'Отмена':
        bot.reply_to(message, 'Редактирование отменено')
        bot.delete_state(message.from_user.id, message.chat.id)
        handle_notes(message)
    elif message.text in notes:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['edit_title'] = message.text
        bot.reply_to(message,
                     f"Редактирование заметки '{message.text}'. Введите новое название заметки или отправьте '-', чтобы оставить текущее:")
        bot.set_state(message.from_user.id, NotesStates.edit_title, message.chat.id)
    else:
        bot.reply_to(message, "Такой заметки не существует. Попробуйте еще раз или выберите 'Отмена'.")
@bot.message_handler(state=NotesStates.edit_title):
def edit_note_title(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        old_title = data['edit_title']
        if message.text != '-':
            new_title = message.text
            notes[new_title] = notes.pop(old_title)
            data['edit_title'] = new_title
        else:
            new_title = old_title
        bot.reply_to(message, f"Введите новое описание заметки или отправьте '-', чтобы оставить текущее:")
        bot.set_state(message.from_user.id, NotesStates.edit_description, message.chat.id)
@bot.message_handler(state=NotesStates.edit_description)
def edit_note_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        title = data['edit_title']
        if message.text != '-':
            notes[title] = message.text
    bot.reply_to(message, f"Заметка '{title}' успешно отредактирована!")
    bot.delete_state(message.from_user.id, message.chat.id)
    handle_notes(message)
@bot.message_handler(func=lambda message: message.text == 'Назад в главное меню')
def load_contacts():
    try:
        with open('contacts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_contacts(contacts):
    with open('contacts.json', 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

contacts = load_contacts()

# Обработчики команд для управления контактами
@bot.message_handler(func=lambda message: message.text == '3. Управление контактами')
def handle_contacts(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_contact_1 = types.KeyboardButton('Добавить новый контакт')
    button_contact_2 = types.KeyboardButton('Поиск контакта')
    button_contact_3 = types.KeyboardButton('Редактировать контакт')
    button_contact_4 = types.KeyboardButton('Удалить контакт')
    button_contact_5 = types.KeyboardButton('Экспорт контактов CSV')
    button_contact_6 = types.KeyboardButton('Назад в главное меню')
    keyboard.add(button_contact_1, button_contact_2, button_contact_3, button_contact_4, button_contact_5, button_contact_6)
    bot.reply_to(message, 'Выберите действие с контактами:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Добавить новый контакт')
def add_contact(message):
    msg = bot.reply_to(message, 'Введи имя контакта:')
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    name = message.text
    msg = bot.reply_to(message, 'Введи номер телефона:')
    bot.register_next_step_handler(msg, process_phone_step, name)

def process_phone_step(message, name):
    phone = message.text
    msg = bot.reply_to(message, 'Введи email (или оставьте пустым):')
    bot.register_next_step_handler(msg, process_email_step, name, phone)

def process_email_step(message, name, phone):
    email = message.text
    contact_id = len(contacts) + 1
    contacts[contact_id] = {'name': name, 'phone': phone, 'email': email}
    save_contacts(contacts)
    bot.reply_to(message, "Контакт  добавлен!")
    handle_contacts(message)

@bot.message_handler(func=lambda message: message.text == 'Поиск контакта')
def search_contact(message):
    msg = bot.reply_to(message, 'Введите имя или номер телефона:')
    bot.register_next_step_handler(msg, process_search)

def process_search(message):
    query = message.text
    found_contacts = [contact for contact in contacts.values() if query in contact['name'] or query in contact['phone']]
    if found_contacts:
        result = 'Найденные контакты:\n' + '\n'.join([f"{c['name']}, {c['phone']}, {c['email']}" for c in found_contacts])
    else:
        result = 'Контакты не найдены.'
    bot.reply_to(message, result)
    handle_contacts(message)

@bot.message_handler(func=lambda message: message.text == 'Редактировать контакт')
def edit_contact_start(message):
    msg = bot.reply_to(message, 'Введите имя контакта для редактирования:')
    bot.register_next_step_handler(msg, edit_contact_process)

def edit_contact_process(message):
    query = message.text
    contact_id = next((id for id, contact in contacts.items() if contact['name'] == query), None)
    if contact_id:
        msg = bot.reply_to(message, 'Введите новое имя (или оставьте пустым):')
        bot.register_next_step_handler(msg, edit_contact_name, contact_id)
    else:
        bot.reply_to(message, 'Контакт не найден.')
        handle_contacts(message)

def edit_contact_name(message, contact_id):
    new_name = message.text or contacts[contact_id]['name']
    msg = bot.reply_to(message, 'Введите новый номер телефона (или оставьте пустым):')
    bot.register_next_step_handler(msg, edit_contact_phone, contact_id, new_name)

def edit_contact_phone(message, contact_id, new_name):
    new_phone = message.text or contacts[contact_id]['phone']
    msg = bot.reply_to(message, 'Введите новый email (или оставьте пустым):')
    bot.register_next_step_handler(msg, edit_contact_email, contact_id, new_name, new_phone)

def edit_contact_email(message, contact_id, new_name, new_phone):
    new_email = message.text or contacts[contact_id]['email']
    contacts[contact_id] = {'name': new_name, 'phone': new_phone, 'email': new_email}
    save_contacts(contacts)
    bot.reply_to(message, f"Контакт '{new_name}' обновлён!")
    handle_contacts(message)

@bot.message_handler(func=lambda message: message.text == 'Удалить контакт')
def delete_contact_start(message):
    msg = bot.reply_to(message, 'Введите имя контакта для удаления:')
    bot.register_next_step_handler(msg, delete_contact_process)

def delete_contact_process(message):
    query = message.text
    contact_id = next((id for id, contact in contacts.items() if contact['name'] == query), None)
    if contact_id:
        del contacts[contact_id]
        save_contacts(contacts)
        bot.reply_to(message, 'Контакт удалён.')
    else:
        bot.reply_to(message, 'Контакт не найден.')
    handle_contacts(message)

@bot.message_handler(func=lambda message: message.text == 'Экспорт контактов CSV')
def export_contacts(message):
    with open('contacts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'phone', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cid, info in contacts.items():
            writer.writerow({'id': cid, **info})
    bot.reply_to(message, "Контакты экспортированы")
    handle_contacts(message)
import telebot
from telebot import types
import json
import csv
from datetime import datetime

# Загрузка и сохранение финансовых записей
def load_finance_records():
    try:
        with open('finance.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_finance_records(records):
    with open('finance.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

finance_records = load_finance_records()

# Финансовые записи
@bot.message_handler(func=lambda message: message.text == '4. Управление финансовыми записями')
def handle_finance(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button_add = types.KeyboardButton('Добавить новую запись')
    button_view = types.KeyboardButton('Просмотр всех записей')
    button_report = types.KeyboardButton('Генерация отчёта')
    button_import = types.KeyboardButton('Импорт записей CSV')
    button_export = types.KeyboardButton('Экспорт записей CSV')
    button_back = types.KeyboardButton('Назад в главное меню')
    keyboard.add(button_add, button_view, button_report, button_import, button_export, button_back)
    bot.reply_to(message, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Добавить новую запись')
def add_finance_record(message):
    msg = bot.reply_to(message, 'Введите сумму операции (положительная для дохода, отрицательная для расхода):')
    bot.register_next_step_handler(msg, process_amount_step)

def process_amount_step(message):
    try:
        amount = float(message.text)
        msg = bot.reply_to(message, 'Введите категорию:')
        bot.register_next_step_handler(msg, process_category_step, amount)
    except ValueError:
        bot.reply_to(message, 'Некорректная сумма. Пожалуйста, введите число.')
        handle_finance(message)

def process_category_step(message, amount):
    category = message.text
    msg = bot.reply_to(message, 'Введите дату в формате ДД-ММ-ГГГГ:')
    bot.register_next_step_handler(msg, process_date_step, amount, category)

def process_date_step(message, amount, category):
    date = message.text
    try:
        datetime.strptime(date, '%d-%m-%Y')
        msg = bot.reply_to(message, 'Введите описание операции:')
        bot.register_next_step_handler(msg, process_description_step, amount, category, date)
    except ValueError:
        bot.reply_to(message, 'Некорректная дата. Используйте формат ДД-ММ-ГГГГ.')
        handle_finance(message)

def process_description_step(message, amount, category, date):
    description = message.text
    record_id = len(finance_records) + 1
    finance_records.append({
        'id': record_id,
        'amount': amount,
        'category': category,
        'date': date,
        'description': description
    })
    save_finance_records(finance_records)
    bot.reply_to(message, f"Финансовая запись добавлена!")
    handle_finance(message)

@bot.message_handler(func=lambda message: message.text == 'Просмотр всех записей')
def view_finance_records(message):
    if not finance_records:
        bot.reply_to(message, 'Записей нет.')
    else:
        records_list = 'Ваши записи:\n' + '\n'.join([f"{r['date']} - {r['category']}: {r['amount']} ({r['description']})" for r in finance_records])
        bot.reply_to(message, records_list)
    handle_finance(message)

@bot.message_handler(func=lambda message: message.text == 'Экспорт записей CSV')
def export_finance_records(message):
    with open('finance.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'amount', 'category', 'date', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in finance_records:
            writer.writerow(record)
    bot.reply_to(message, "Записи экспортированы в finance.csv.")
    handle_finance(message)

@bot.message_handler(func=lambda message: message.text == '5. Калькулятор')
def handle_calculator(message):
    msg = bot.reply_to(message, 'Введите выражение для вычисления:')
    bot.register_next_step_handler(msg, process_calculation)

def process_calculation(message):
    try:
        result = eval(message.text)
        bot.reply_to(message, f"Результат: {result}")
    except Exception:
        bot.reply_to(message, "Ошибка в выражении.")
    show_main_menu(message)

def handle_back_to_main(message):
    show_main_menu(message)

bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))

bot.polling()

