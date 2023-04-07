import bot
from telegram.ext import (CommandHandler, CallbackQueryHandler, 
                          MessageHandler, ApplicationBuilder, filters
                          )

def main():
    app = ApplicationBuilder().token(bot.config.TOKEN).build()

    command = MessageHandler(filters.Regex(r'/{0,1}\d{1,}'), bot.handlers.timer)
    pomodoro_handler = CommandHandler('pomodoro', bot.handlers.pomodoro)
    start_handler = CommandHandler('start', bot.handlers.start)
    keyboard_handler = CallbackQueryHandler(bot.handlers.keyboard_callback)
    rules_handler = CommandHandler('rules', bot.handlers.rules)
    
    app.add_handler(command)
    app.add_handler(pomodoro_handler)
    app.add_handler(start_handler)
    app.add_handler(keyboard_handler)
    app.add_handler(rules_handler)

    if bot.config.webhook:
        app.run_webhook(**bot.config.webhook_params)

    else:
        app.run_polling()

if __name__ == '__main__':
    main()