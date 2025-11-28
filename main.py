import os
import ffmpeg
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

VIDEO_DIR = "videos/"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

user_state = {}
user_video = {}

# ---------------- Handlers ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a video, then use /hardsub")

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    file = update.message.video or update.message.document

    if file is None:
        await update.message.reply_text("Send a valid video")
        return

    video_path = f"{VIDEO_DIR}{user_id}.mp4"
    await file.get_file().download_to_drive(video_path)
    user_video[user_id] = video_path

    await update.message.reply_text("Video saved ✔️\nNow reply /hardsub")

async def hardsub_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_video:
        await update.message.reply_text("Pehle video bhejo!")
        return

    user_state[user_id] = "WAIT_SUB"
    await update.message.reply_text("Now send .ass subtitle file")

async def subtitle_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_state.get(user_id) != "WAIT_SUB":
        return

    file = update.message.document
    if not file.file_name.endswith(".ass"):
        await update.message.reply_text("Send .ass subtitle only")
        return

    sub_path = f"{VIDEO_DIR}{user_id}.ass"
    await file.get_file().download_to_drive(sub_path)

    await update.message.reply_text("Hardsubbing... ⏳")

    input_video = user_video[user_id]
    output_path = f"{VIDEO_DIR}hardsub_{user_id}.mp4"

    try:
        ffmpeg.input(input_video).output(
            output_path,
            vf=f"subtitles={sub_path.replace(':', '\\:')}",
            vcodec='libx264',
            acodec='copy'
        ).run(overwrite_output=True)

        await update.message.reply_video(video=open(output_path, "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

    user_state.pop(user_id, None)
    user_video.pop(user_id, None)

# ---------------- Main ---------------- #

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hardsub", hardsub_cmd))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, save_video))
    app.add_handler(MessageHandler(filters.Document.ALL, subtitle_received))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
