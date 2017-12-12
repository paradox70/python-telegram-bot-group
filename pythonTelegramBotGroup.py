from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
import logging
import config

TOKEN = config.ids['token']	#pythonTelegramGroup_bot
admin_id = config.ids['your_id']
group_id = -1001126366525#config.ids['group_ids']
#join_chat_link = 'https://telegram.me/joinchat/AAAAAEi8EwLY8ejWyIoErQ'

#database connector
#db = DBHelper()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



def start(bot, update):
	user = update.message.from_user
	update.message.reply_text('Welcome to python-telegram-bot group!')

def receive_message(bot, update):
	user = update.message.from_user
	print(update)
	user_id = '[{}](tg://user?id={})\n'.format(user.first_name, user.id)
	new_text = user_id + update.message.text
	bot.send_message(chat_id=admin_id, text=new_text, parse_mode=ParseMode.MARKDOWN)


def send_message(bot, update):
	user = update.message.from_user

	m = update.message
	if m.text:
		bot.send_message(chat_id=group_id, text=m.text, parse_mode=ParseMode.MARKDOWN)
		return

	if (m.photo or m.video or m.document or m.voice or m.audio):
		if m.photo:
			file_id = m.photo[-1].file_id
			caption = m.caption
			res = bot.send_photo(chat_id=group_id, photo=file_id, caption=caption)
			return

		elif m.video:
			file_id = m.video.file_id
			caption = m.caption
			res = bot.send_video(chat_id=group_id, video=file_id, caption=caption)
			return

		elif m.audio:
			file_id = m.audio.file_id
			caption = m.caption
			res = bot.send_audio(chat_id=group_id, audio=file_id, caption=caption)
			return

		elif m.voice:
			file_id = m.voice.file_id
			caption = m.caption
			res = bot.send_voice(chat_id=group_id, voice=file_id, caption=caption)
			return

		elif m.document:
			file_id = m.document.file_id
			caption = m.caption
			res = bot.send_document(chat_id=group_id, document=file_id, caption=caption)
			return
	else:
		update.message.reply_text('This message is not supported!', reply_to_message_id=m.message_id)


def forward(bot, update):
	print('Update-----', update)
	user = update.message.from_user
	res = bot.forward_message(chat_id=admin_id, from_chat_id=group_id, message_id=update.message.message_id)
	print('chat_id= ', res.chat_id, 'message_id= ',res.message_id)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main(webhook_url=None):
	# Create the EventHandler and pass it your bot's token.
	# Get the dispatcher to register handlers
	updater = Updater(TOKEN)
	bot = updater.bot
	dp = updater.dispatcher

	start_handler = CommandHandler('start', start)
	receive_message_handler = MessageHandler(Filters.text & Filters.chat(group_id), receive_message)
	forward_handler = MessageHandler(Filters.all & Filters.chat(group_id), forward)
	send_message_handler = MessageHandler(Filters.all & Filters.chat(admin_id), send_message)
	dp.add_handler(start_handler)
	dp.add_handler(send_message_handler)
	dp.add_handler(receive_message_handler)
	dp.add_handler(forward_handler)
	dp.add_error_handler(error)

	# Start the Bot
	bot.set_webhook()
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()

