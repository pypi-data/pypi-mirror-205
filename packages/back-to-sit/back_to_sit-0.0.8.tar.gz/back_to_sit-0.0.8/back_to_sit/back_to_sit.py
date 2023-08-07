import telegram
import asyncio
import time 

async def __send_telegram_message(message, chat_id, token):
    # Set up the bot
    bot = telegram.Bot(token=token)

    # Send a message
    await bot.send_message(chat_id=chat_id, text=message)


def back_to_sit(message, chat_id, token, start_time = None, notebook = True):
    """
    Function that send message when is called
    """
    end_time = time.time()
    # Create an event loop
    if start_time is not None:
        message = message + f"\n Time taken to execute: {(end_time - start_time)/60:.6f} minutes"

    if notebook:
        loop = asyncio.get_event_loop()
        loop.create_task(__send_telegram_message(message, chat_id, token))
    else:
        loop = asyncio.new_event_loop()
        # Run the coroutine in the event loop
        loop.run_until_complete(__send_telegram_message(message, chat_id, token))
        loop.stop()
        loop.close()

def back_to_sit_decorator(base_message, chat_id, token, notebook = True):
    """
    Decorator that send a message when the function is done
    and report the time taken to execute the function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            NEW_MESSAGE = base_message + f"\n Time taken to execute {func.__name__}: {(end_time - start_time)/60:.6f} minutes"
            back_to_sit(message=NEW_MESSAGE, chat_id=chat_id, token=token, notebook=notebook)
            return result
        return wrapper
    return decorator
