from utils.msg_responses import msg
from modules.model.entities.user import User
from modules.model import (
	register_user as RUser, 
	update_user as UUser, 
	get_user as GUser)
from telegram import Update
from utils.logger import logger
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


NOMBRE, AHORRO_DIARIO, DIAS, REGISTRO = range(4)

# ----------------------------------


def start(update: Update, context: CallbackContext) -> int:
	if not GUser.is_user(update.effective_chat.id):

		update.message.reply_text(
			'¡Me llamo Ahorracio! Te ayudaré a llevar tus ahorros durante el tiempo que tú desees.'
			'Recuerda que en cualquier momento puedes escribir /cancelar para no seguir esta conversación.\n\n'
			'¿Cómo quieres que te llame? Puedes escribir /saltar y usaré tu usuario de Telegram',
		)

		RUser.insert_new_user(chat_id = update.effective_chat.id)
		
		return NOMBRE

	if GUser.is_completed(update.effective_chat.id):
		update.message.reply_text(
			'¡Ya has registrado tus datos! Si lo que deseas es hacer un cambio, escribe /help para ver como lo puedes hacer.',
		)
		return ConversationHandler.END
	
	update.message.reply_text(
		'Tu registro anterior no se terminó, te volveré a pedir tus datos.\n\n',
		'¿Cómo quieres que te llame? Puedes escribir /saltar y usaré tu usuario de Telegram',
	)

	return NOMBRE

# ----------------------------------

def insert_name(update: Update, context: CallbackContext) -> int:
	user = UUser.update_user_by_chat_id(
			update.effective_chat.id, 
			name=update.message.text )

	
	logger.info(f"Nombre de {user['chat_id']}: {user['name']}")
	update.message.reply_text(f"¡Entendido! Desde ahora te llamaré {user['name']}")
	
	update.message.reply_text(
		msg['ahorro_text_intro_1'](user['name']), parse_mode='MarkdownV2'
	)
	update.message.reply_text(
		msg['ahorro_text_intro_2'], parse_mode='MarkdownV2'
	)

	return AHORRO_DIARIO


def skip_insert_name(update: Update, context: CallbackContext) -> int:
	telegram_user = update.message.from_user
	user = UUser.update_user_by_chat_id(
			update.effective_chat.id, 
			name = telegram_user.first_name )

	logger.info(f"Nombre de {user['chat_id']}: {user['name']}")
	update.message.reply_text(f"¡No te preocupes! Te llamaré {user['name']}")

	update.message.reply_text(
		msg['ahorro_text_intro_1'](user['name']), parse_mode='MarkdownV2'
	)
	update.message.reply_text(
		msg['ahorro_text_intro_2'], parse_mode='MarkdownV2'
	)

	return AHORRO_DIARIO

# ----------------------------------

def insert_ahorro(update: Update, context: CallbackContext) -> int:
	
	ahorro = float(update.message.text.replace('$',''))
	user = UUser.update_user_by_chat_id(
			update.effective_chat.id, 
			save_per_day=ahorro)

	logger.info(f"El ahorro de {user['chat_id']} será: {user['save_per_day']}")
	update.message.reply_text(f'¡Excelente! Desde ahora, ahorrarás {user["save_per_day"]} al día')
	update.message.reply_text(msg['days_text_intro'])

	return DIAS


def skip_insert_ahorro(update: Update, context: CallbackContext) -> int:
	user = GUser.get_user(update.effective_chat.id)

	logger.info(f"El ahorro de {user['chat_id']} será: {user['save_per_day']}")
	update.message.reply_text(f'¡Va! Desde ahora, ahorrarás de manera aleatoria todos días')
	update.message.reply_text(msg['days_text_intro'])

	return DIAS


# ----------------------------------
def insert_dias(update: Update, context: CallbackContext) -> int:
	days = int(update.message.text)
	user = UUser.update_user_by_chat_id(
			update.effective_chat.id, 
			total_days=days,
			completed=True)

	saving = UUser.submit_saving(user['chat_id'])[1]

	logger.info(f"Los dias que {user['chat_id']} ahorrará serán {user['total_days']}")
	update.message.reply_text(
		msg['first_saving_text'](saving), 
		parse_mode='MarkdownV2')

	update.message.reply_text(msg['final_text'])

	return ConversationHandler.END
# ----------------------------------
def cancel(update: Update, context: CallbackContext) -> int:
	user = update.message.from_user
	logger.info(f"User {user.first_name} canceled the conversation.")
	update.message.reply_text(
		'¡Puedes intentarlo en otro momento!'
	)
	
	return ConversationHandler.END

# The conversation start with a simple presentation of the bot,
# Next, the user will write all their information and create a new User object
# When they finish, the user will be uploaded to the database
conversation_handler = ConversationHandler(
  entry_points = [CommandHandler('start', start)],
  states = {
    NOMBRE: [
      MessageHandler(Filters.text & ~Filters.command, insert_name),
      CommandHandler('saltar', skip_insert_name)
    ],
    AHORRO_DIARIO: [
      MessageHandler(Filters.regex(r'^([$]?[0-9]+[.]?[0-9]*)$'), insert_ahorro), 
      CommandHandler('saltar', skip_insert_ahorro)
    ],
    DIAS: [
        MessageHandler(Filters.regex(r'^[0-9]*[0-9]+$'), insert_dias),
    ],
  },
  fallbacks = [CommandHandler('cancelar', cancel)],
)
