from aiogram import types

def get_null_answer_keyboard(resize_keyboard=True):
    buttons = [types.KeyboardButton(text="-")]
    return types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard,
        keyboard=[buttons])

def get_start_keyboard(resize_keyboard=True):
    buttons = [types.KeyboardButton(text="Создать очередь"),
               types.KeyboardButton(text="Войти в очередь")]
    return types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard,
        keyboard=[buttons])

def get_wait_keyboard(resize_keyboard=True, is_moder=False, is_current=False):
    if is_current:
        buttons = [types.KeyboardButton(text="Принять"),
               types.KeyboardButton(text="Пропустить")]
    else:
        buttons = [[types.KeyboardButton(text="Покинуть очередь"),
               types.KeyboardButton(text="Пропустить очередь"),
               types.KeyboardButton(text="Поменяться разок"),
               types.KeyboardButton(text="Поменяться")]]
    if is_moder:
        buttons += [[types.KeyboardButton(text="Остановить очередь"),
            types.KeyboardButton(text="Удалить из очереди"),
            types.KeyboardButton(text="Заставить пропустить"),
            types.KeyboardButton(text="Заставить принять текущего")]]
    return types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard,
        keyboard=buttons)
