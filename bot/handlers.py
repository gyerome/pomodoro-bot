from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
import bot.messages as messages
import re

pomodoro_timers = {}

async def timer(update=None, context=None, time=None):
    if time is None:
        message = update.message.text
        
        if message[0] == '/':
            message=message[1:]

        time=int(message)


    text = messages.timer_start.format(time)

    if update is None:
        chat_id = context.job.chat_id

    else:
        chat_id = update.effective_chat.id

    keyboard=InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text=u'\U0000231B', #Песочные часы
            callback_data='stop',
            )]]
        )

    message = await context.bot.send_message(
        text=text,
        chat_id=chat_id,
        reply_markup=keyboard,
        )

    context.job_queue.run_once(
        when=time*60,
        chat_id=chat_id,
        name=str(chat_id),
        callback = timer_callback,
        data={'message': message}
        )


async def timer_callback(context: CallbackContext):
    timer = pomodoro_timers.get(context.job.chat_id)
    message = context.job.data['message']

    await context.bot.edit_message_text(
        text=message.text,
        message_id=message.message_id,
        chat_id=context.job.chat_id
        )

    if timer is None:
        await context.bot.send_message(text=messages.timer_end, chat_id=context.job.chat_id)

    elif timer['type'] == 'short':
        timer['type'] = 'long'
        await timer(context, time=time)

    elif timer['num_short'] == 3:
        await context.bot.send_message(text=messages.pmdr_end, chat_id=context.job.chat_id)
        pomodoro_timers.pop(context.job.chat_id)

    elif timer['type'] == 'long':
        timer['type'] = 'short'
        timer['num_short']+=1
        await timer(context, time=time)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text=messages.start,
                                   chat_id=update.effective_chat.id)

async def pomodoro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pomodoro_timers[update.effective_chat.id] = {'type': 'long', 'num_short': 0}
    await timer(update, context, time=25)

async def keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback = update.callback_query
    if callback.data == 'stop':
        timer = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))
        for i in timer:
            i.schedule_removal()

        if pomodoro_timers.get(update.effective_chat.id) is not None:
            pomodoro_timers.pop(update.effective_chat.id)

        await context.bot.edit_message_text(
            text=messages.timer_interupt,
            chat_id=callback.message.chat_id,
            message_id=callback.message.message_id
            )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text=messages.rules,
                                   chat_id=update.effective_chat.id)
