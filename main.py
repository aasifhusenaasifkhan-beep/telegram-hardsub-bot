import os
import ffmpeg
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot

VIDEO_DIR = "videos/"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

user_state = {}
user_video = {}

def start(update, context):
    update.message.reply_text("Send a video, then use /hardsub")

def save_video(update, context):
    user_id = update.message.from_user.id
    file = update.message.video or update.message.document

    if file is None:
        return update.message.reply_text("Send a valid video")

    video_path = f"{VIDEO_DIR}{user_id}.mp4"
    file.get_file().download(video_path)
    user_video[user_id] = video_path

    update.message.reply_text("Video saved ✔️\nNow reply /hardsub")

def hardsub_cmd(update, context):
    user_id = update.message.from_user.id

    if user_id not in user_video:
        return update.message.reply_text("Pehle video bhejo!")

    user_state[user_id] = "WAIT_SUB"
    update.message.reply_text("Now send .ass subtitle file")

def subtitle_received(update, context):
    user_id = update.message.from_user.id

    if user_state.get(user_id) != "WAIT_SUB":
        return

    file = update.message.document
    if not file.file_name.endswith(".ass"):
        return update.message.reply_text("Send .ass subtitle only")

    sub_path = f"{VIDEO_DIR}{user_id}.ass"
    file.get_file().download(sub_path)

    update.message.reply_text("Hardsubbing... ⏳")

    input_video = user_video[user_id]
    output_path = f"{VIDEO_DIR}hardsub_{user_id}.mp4"

    try:
        ffmpeg.input(input_video).output(
            output_path,
            vf=f"subtitles={sub_path.replace(':', '\\:')}",
            vcodec='libx264',
            acodec='copy'
        ).run(overwrite_output=True)

        update.message.reply_video(video=open(output_path, "rb"))
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

    user_state.pop(user_id, None)
    user_video.pop(user_id, None)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hardsub", hardsub_cmd))
    dp.add_handler(MessageHandler(Filters.video | Filters.document.video, save_video))
    dp.add_handler(MessageHandler(Filters.document, subtitle_received))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
