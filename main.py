import os
import asyncio
import ffmpeg
import pysubs2
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("hardsubbot", bot_token=os.getenv("TOKEN"))

VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Video bhejo → reply mein /hardsub → .ass subtitle forward karo\nHardsub karke de dunga ✅")

@app.on_message(filters.command("hardsub") & filters.reply)
async def hardsub_cmd(client, message: Message):
    reply = message.reply_to_message
    if not (reply.video or reply.document):
        return await message.reply("Video ko reply kar /hardsub se!")
    
    user_states[message.from_user.id] = {"video": reply}
    await message.reply("Ab .ass subtitle file forward kar do")

@app.on_message(filters.document & filters.regex(r"\.ass$"))
async def receive_subtitle(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return
    
    status_msg = await message.reply("Downloading video + subtitle...")
    video_msg = user_states[user_id]["video"]
    
    video_path = await video_msg.download(VIDEO_DIR)
    sub_path = await message.download(VIDEO_DIR)
    output_path = VIDEO_DIR + f"hardsub_{user_id}.mkv"
    
    try:
        await status_msg.edit("Hardsubbing chal raha hai...")
        
        ffmpeg.input(video_path).output(
            output_path,
            vf=f"subtitles={sub_path.replace(':', '\\:')}",
            c_v="libx264", preset="veryfast", crf=23, c_a="copy"
        ).overwrite_output().run(quiet=True)
        
        await status_msg.edit("Uploading...")
        await message.reply_video(output_path, caption="Hardsub done ✅")
        
        # cleanup
        for f in [video_path, sub_path, output_path]:
            try: os.remove(f)
            except: pass
        del user_states[user_id]
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit(f"Error: {str(e)}")

app.run()import os
import asyncio
import ffmpeg
import pysubs2
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("hardsubbot", bot_token=os.getenv("TOKEN"))

VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Video bhejo → reply mein /hardsub → .ass subtitle forward karo\nHardsub karke de dunga ✅")

@app.on_message(filters.command("hardsub") & filters.reply)
async def hardsub_cmd(client, message: Message):
    reply = message.reply_to_message
    if not (reply.video or reply.document):
        return await message.reply("Video ko reply kar /hardsub se!")
    
    user_states[message.from_user.id] = {"video": reply}
    await message.reply("Ab .ass subtitle file forward kar do")

@app.on_message(filters.document & filters.regex(r"\.ass$"))
async def receive_subtitle(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        return
    
    status_msg = await message.reply("Downloading video + subtitle...")
    video_msg = user_states[user_id]["video"]
    
    video_path = await video_msg.download(VIDEO_DIR)
    sub_path = await message.download(VIDEO_DIR)
    output_path = VIDEO_DIR + f"hardsub_{user_id}.mkv"
    
    try:
        await status_msg.edit("Hardsubbing chal raha hai...")
        
        ffmpeg.input(video_path).output(
            output_path,
            vf=f"subtitles={sub_path.replace(':', '\\:')}",
            c_v="libx264", preset="veryfast", crf=23, c_a="copy"
        ).overwrite_output().run(quiet=True)
        
        await status_msg.edit("Uploading...")
        await message.reply_video(output_path, caption="Hardsub done ✅")
        
        # cleanup
        for f in [video_path, sub_path, output_path]:
            try: os.remove(f)
            except: pass
        del user_states[user_id]
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit(f"Error: {str(e)}")

app.run()
