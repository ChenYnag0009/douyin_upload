import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import subprocess

# Bot Token
TOKEN = "8108185474:AAHhUu6H9BeEp0ZHN46V_sjvK2FtViwMUYk"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Command: /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 សួស្តី! បញ្ជូនវីដេអូមកខ្ញុំ ដើម្បីអាប់ឡូតទៅ Douyin។")

# Handle video uploads
def handle_video(update: Update, context: CallbackContext) -> None:
    video = update.message.video or update.message.document
    if not video:
        update.message.reply_text("⚠️ សូមផ្ញើវីដេអូ។")
        return

    file = context.bot.get_file(video.file_id)
    file_path = f"video/{video.file_id}.mp4"
    file.download(file_path)

    update.message.reply_text("📤 កំពុងបញ្ចូលទៅ Douyin...")

    # Run Douyin Upload Script
    video_data_list = [
        {"title": "Telegram Upload", "desc": ["#TelegramBot"], "path": file_path}
    ]

    os.environ["VIDEO_DATA"] = str(video_data_list)
    subprocess.run(["python", "main.py"])

    update.message.reply_text("✅ អាប់ឡូតរួចរាល់!")

# Main Function
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video | Filters.document, handle_video))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
