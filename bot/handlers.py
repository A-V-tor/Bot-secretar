import os
import time
from flask import request, abort, current_app as app
import telebot
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("token"))


@bot.message_handler(commands=["start"])
def start_chat(message):
    bot.send_message(message.from_user.id, "OK")


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK"
    else:
        abort(403)


# bot.polling()

bot.remove_webhook()
time.sleep(0.1)

bot.set_webhook(url="")
