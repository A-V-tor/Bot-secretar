text_for_new_user = """
Вы добавлены в пользователи бота
Ваш логин и пароль от админки:
<code>Логин: {username}</code>
<code>Пароль: {user_psw}</code>\n
"""

note_workout = """
➖➖➖➖➖➖➖➖
Всего за день: <b>{len_workouts}</b>
➖➖➖➖➖➖➖➖
{date}
➖➖➖➖➖➖➖➖

{text}
"""


retry_logs = """Попытка {attempt} для события {event} tg_id: {chat_id} - user: {username} - текст: {text}"""
