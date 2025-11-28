import os
import asyncio
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot token
TOKEN = os.getenv("TOKEN")

# Directory setup
VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Video bhejo → reply mein /hardsub → .ass subtitle forward karo\nHardsub karke de dunga ✅")

async def hardsub_cmd(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi video par reply karo /hardsub se!")
        return
    
    reply = update.message.reply_to_message
    if not (reply.video or (reply.document and reply.document.mime_type.startswith('video/'))):
        await update.message.reply_text("Sirf video files support hain!")
        return
    
    user_states[update.effective_user.id] = {"video": reply}
    await update.message.reply_text("Ab .ass subtitle file forward kar do")

async def handle_subtitle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_states:
        return
    
    if not update.message.document:
        return
    
    if not update.message.document.file_name.endswith('.ass'):
        await update.message.reply_text("Sirf .ass files accept hain!")
        return
    
    status_msg = await update.message.reply_text("Downloading video + subtitle...")
    video_msg = user_states[user_id]["video"]
    
    try:
        # Download video file
        video_file = await video_msg.effective_attachment.get_file()
        video_path = os.path.join(VIDEO_DIR, f"video_{user_id}.mp4")
        await video_file.download_to_drive(video_path)
        
        # Download subtitle file
        sub_file = await update.message.document.get_file()
        sub_path = os.path.join(VIDEO_DIR, f"sub_{user_id}.ass")
        await sub_file.download_to_drive(sub_path)
        
        output_path = os.path.join(VIDEO_DIR, f"hardsub_{user_id}.mp4")
        
        await status_msg.edit_text("Hardsubbing chal raha hai...")
        
        # FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles='{sub_path}'",
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-crf', '23',
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            await status_msg.edit_text(f"FFmpeg error: {error_msg[:1000]}")
            return
        
        if not os.path.exists(output_path):
            await status_msg.edit_text("Output file create nahi hua")
            return
        
        await status_msg.edit_text("Uploading...")
        
        # Upload video
        with open(output_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="Hardsub done ✅"
            )
        
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"Error: {str(e)}")
    
    finally:
        # Cleanup files
        for file_path in [video_path, sub_path, output_path]:
            try:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
        
        # Remove user state
        if user_id in user_states:
            del user_states[user_id]

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hardsub", hardsub_cmd))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_subtitle))
    
    # Start bot
    print("Bot starting...")
    application.run_polling()

if __name__ == "__main__":
    main()import os
import asyncio
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot token
TOKEN = os.getenv("TOKEN")

# Directory setup
VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Video bhejo → reply mein /hardsub → .ass subtitle forward karo\nHardsub karke de dunga ✅")

async def hardsub_cmd(update: Update, context: CallbackContext):
    if not update.message.reply_to_message:
        await update.message.reply_text("Kisi video par reply karo /hardsub se!")
        return
    
    reply = update.message.reply_to_message
    if not (reply.video or (reply.document and reply.document.mime_type.startswith('video/'))):
        await update.message.reply_text("Sirf video files support hain!")
        return
    
    user_states[update.effective_user.id] = {"video": reply}
    await update.message.reply_text("Ab .ass subtitle file forward kar do")

async def handle_subtitle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_states:
        return
    
    if not update.message.document:
        return
    
    if not update.message.document.file_name.endswith('.ass'):
        await update.message.reply_text("Sirf .ass files accept hain!")
        return
    
    status_msg = await update.message.reply_text("Downloading video + subtitle...")
    video_msg = user_states[user_id]["video"]
    
    try:
        # Download video file
        video_file = await video_msg.effective_attachment.get_file()
        video_path = os.path.join(VIDEO_DIR, f"video_{user_id}.mp4")
        await video_file.download_to_drive(video_path)
        
        # Download subtitle file
        sub_file = await update.message.document.get_file()
        sub_path = os.path.join(VIDEO_DIR, f"sub_{user_id}.ass")
        await sub_file.download_to_drive(sub_path)
        
        output_path = os.path.join(VIDEO_DIR, f"hardsub_{user_id}.mp4")
        
        await status_msg.edit_text("Hardsubbing chal raha hai...")
        
        # FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f"subtitles='{sub_path}'",
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-crf', '23',
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            await status_msg.edit_text(f"FFmpeg error: {error_msg[:1000]}")
            return
        
        if not os.path.exists(output_path):
            await status_msg.edit_text("Output file create nahi hua")
            return
        
        await status_msg.edit_text("Uploading...")
        
        # Upload video
        with open(output_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="Hardsub done ✅"
            )
        
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"Error: {str(e)}")
    
    finally:
        # Cleanup files
        for file_path in [video_path, sub_path, output_path]:
            try:
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
        
        # Remove user state
        if user_id in user_states:
            del user_states[user_id]

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hardsub", hardsub_cmd))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_subtitle))
    
    # Start bot
    print("Bot starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
