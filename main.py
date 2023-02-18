import telebot
import random
import numpy as np
from PIL import Image
import io
import tensorflow as tf

API_KEY = '6003853915:AAGpFhWzggKQU2ud_wiB91tg-By2vLYcj4o'
bot = telebot.TeleBot(API_KEY)

model = tf.keras.models.load_model('C:/Users/ф/Desktop/addp/my_model (14).h5')
class_names = {0: 'paper', 1: 'rock', 2: 'scissors'}

hands = {
    0: '🖐️ Paper',
    1: '👊 Rock',
    2: '✌️ Scissors'
}


def start_game(message):
    bot.send_message(message.chat.id, "Welcome to rock-paper-scissors game! Please send /play to start.")


def play_game(message):
    bot.send_message(message.chat.id, "Please take a picture of your hand showing a rock, paper, or scissors.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    img = Image.open(io.BytesIO(downloaded_file))
    img = img.resize((224, 224), resample=Image.BICUBIC)
    img = np.array(img) / 255.0

    prediction = model.predict(np.array([img]))
    predicted_class_index = np.argmax(prediction)
    if predicted_class_index < len(class_names):
        user_gesture = class_names[predicted_class_index]
    else:
        user_gesture = "unknown"

    bot_gesture = hands[random.randint(0, 2)]

    result = ''

    if user_gesture == 'paper':
        if bot_gesture == hands[1]:
            result = 'You win! 🎉'
        elif bot_gesture == hands[2]:
            result = 'You lose! 😢'
        else:
            result = 'It\'s a tie! 🤝'
    elif user_gesture == 'rock':
        if bot_gesture == hands[2]:
            result = 'You win! 🎉'
        elif bot_gesture == hands[0]:
            result = 'You lose! 😢'
        else:
            result = 'It\'s a tie! 🤝'
    elif user_gesture == 'scissors':
        if bot_gesture == hands[0]:
            result = 'You win! 🎉'
        elif bot_gesture == hands[1]:
            result = 'You lose! 😢'
        else:
            result = 'It\'s a tie! 🤝'

    bot.send_message(message.chat.id, f"You chose {user_gesture}. I chose {bot_gesture}. {result}")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.chat.id, "Welcome to rock-paper-scissors game! Please send /play to start.")
@bot.message_handler(commands=['play'])
def play_game(message):
    bot.send_message(message.chat.id, "Send me photo")

bot.polling()
