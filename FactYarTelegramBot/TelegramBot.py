import datetime
import logging
import os

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import configs.config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
CHAT_TIMEOUT=120
ADMIN_chanell_id = configs.config.factyar_admins_channel_id
BOT_TOKEN =configs.config.telegram_bot_token

def start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "به ربات فکت‌یار خوش آمدید .\n"
        "با استفاده از این ربات می‌توانید هر خبری که در درستی آن شک دارید را برای تیم فکت‌یار ارسال کنید. تا تیم, این اخبار را در سریع‌ترین زمان ممکن راستی‌آزمایی کرده و نتایج را در سایت و رسانه‌های اجتماعی فکت‌یار قرار خواهیم داد. "
        "\n\n\nدرباره فکت‌یار  /about "
        "\n نحوه کار با ربات /help "
        "\nفکت‌یار در فضای مجازی /link  \n"

        + '\n @factyar \n'
      #  reply_markup=markup,
    )

    return CHOOSING


def received_information(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "خبر شما برای کارشناسان راستی‌آزمایی ارسال شد." +
        " برای اطلاعات بیشتر از سایت http://factyar.com/ و یا دیگر صفحات مجازی فکت‌یار بازدید کنید\n ",
        #     reply_markup=markup,
    )
    #     # forward user message to group
    #     # note: group ID with the negative sign
    bot = context.bot
    bot.forward_message(chat_id=ADMIN_chanell_id,
                            from_chat_id=update.message.chat_id,
                            message_id=update.message.message_id)
    return CHOOSING


def get_addresses(update: Update, context: CallbackContext) -> int:
    update.message.reply_text( 'سایت  http://factyar.com/'
                               +'\nتلگرام  https://t.me/factyar'
                               + '\nاینستاگرام https://www.instagram.com/factyar_com/'
                                + '\n لینکدین /https://www.linkedin.com/company/factyar '
                               + '\nپست الکترونیکی   info@factyar.com'
                                + '\n @factyar \n'
                             #  ,reply_markup= markup
                  )
    return CHOOSING

def how_to_use(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
                             'این ربات جهت ارسال اخبار مشکوک فضای مجازی به تیم فکت‌یار تهیه شده‌است. کافی است هر خبر مشکوکی که در کانال یا گروهی دیده‌اید, برای این ربات Forward یا Copy-paste کنید. '+
                            '\n کارشناسان فکت‌یار خبر موردنظر را راستی‌آزمایی کرده و نتیجه آن را در سایت و رسانه‌های اجتماعی فکت‌یار قرار می‌دهند'+
                            'برای دیدن نشانی رسانه‌های اجتماعی فکت‌یار بر روی link/ کلیک کنید'+
                            '\n @factyar \n'

                              #, reply_markup=markup
                                )

    return CHOOSING

def about_us(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'ما یک تیم مستقل از متخصصین علوم اجتماعی محاسباتی و کارشناسان و فعالان رسانه هستیم که به پایش، اکتشاف، اطلاع‌رسانی، و مقابله با انتشار اطلاعات نادرست یا گمراه‌کننده در اینترنت می‌پردازیم.' +
        '\nفکت‌یار از شخص، گروه، یا حزبی جانب‌داری نمی‌کند. هر شخصی طبیعتا دارای جهت‌گیری سیاسی است که لاجرم در تصمیمات او تاثیرگذار است. برای جلوگیری از نفوذ تصمیمات شخصی در سراسر فرآیندهای راستی‌آزمایی، فکت‌یار از مجموعه‌ای متوازن از کارشناسان و فعالان رسانه‌ای که نماینده تمام گروه‌های سیاسی پذیرفته‌شده داخل کشور باشند بهره می‌گیرد. فکت‌یار وابسته یا شرکت پوششی هیچ شخص، گروه، سازمان، یا حزب سیاسی داخل یا خارج از کشور نیست.' +
        '\n @factyar \n'
        #    , reply_markup=markup
                              )

    return CHOOSING

def not_standard_info(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('پیامی که ارسال کردید فرمت مناسبی ندارد' ,
                              #reply_markup=markup
                              )
    return CHOOSING


def start_telegram_bot() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN,use_context=True)


    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", how_to_use))
    dispatcher.add_handler(CommandHandler("about", about_us))
    dispatcher.add_handler(CommandHandler("link", get_addresses))


    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler( ~Filters.command, received_information))

    # Start the Bot from API
    updater.start_polling()

    #start the bot from WebHook
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=BOT_TOKEN)
    # updater.bot.setWebhook(URL_to_send_updates_to + BOT_TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


