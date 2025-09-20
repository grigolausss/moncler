import os
import asyncio
from telegram import Bot

# IMPORTANT: User must provide their own Bot Token and Chat ID.
# These can be set as environment variables.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str):
    """
    Sends a message to a predefined Telegram chat.

    This function is a placeholder and requires the user to set
    TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("WARNING: Telegram Bot Token or Chat ID not set. Skipping notification.")
        print(f"         Would have sent: {message}")
        return

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"Successfully sent Telegram notification to chat {TELEGRAM_CHAT_ID}.")
    except Exception as e:
        print(f"ERROR: Failed to send Telegram notification: {e}")

def format_stock_update_message(product_name, sku, store_name, city_name, changes):
    """
    Formats a message for a stock update.
    `changes` should be a list of strings describing the change.
    """
    header = f"🟢 Stock Update: {product_name} ({sku}) at {store_name}, {city_name}\n"
    body = "\n".join(f"- {change}" for change in changes)
    return header + body

# Example of how to run the async function from a sync context
if __name__ == '__main__':
    # This is for testing purposes only.
    # To run, set the environment variables and execute: python -m backend.notifications
    example_message = "This is a test notification from the Moncler Stock Monitoring system."
    asyncio.run(send_telegram_message(example_message))
