import os
import asyncio
import pysubs2
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("hardsubbot", bot_token=os.getenv("TOKEN"))

VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply("Video bhejo → usko reply mein /hardsub karo → phir .ass subtitle forward karo\nMain hardsub karke de dunga ✅")

@app.on_message(filters.command("hardsub") & filters.reply)
async def set_video(c, m: Message):
    if not m.reply_to_message.video and not m.reply_to_message.document:
        return await m.reply("Video ya video file ko reply karo /hardsub se")
    
    user_states[m.from_user.id] = {"video": m.reply_to_message}
    await m.reply("Ab .ass subtitle file forward kar do")

@app.on_message(filters.document & filters.regex(r"\.ass$", flags=0))
async def process(c, m: Message):
    user_id = m.from_user.id
    if user_id not in user_states:
        return
    
    status = await m.reply("Downloading video + subtitle… thoda wait karo")
    
    video_msg = user_states[user_id]["video"]
    video_path = await video_msg.download(VIDEO_DIR)
    sub_path = await m.download(VIDEO_DIR)
    output_path = VIDEO_DIR + f"hardsub_{user_id}.mkv"
    
    try:
        await status.edit("Hardsubbing chal raha hai… 480p-1080p tak support hai")
        
        i = ffmpeg.input(video_path)
        (
            ffmpeg
            .input(video_path)
            .output(output_path,
                    vf=f"subtitles={sub_path.replace(':', '\\\\:')}",
                    c_v="libx264", preset="veryfast", crf=23,
                    c_a="copy")
            .overwrite_output()
            .run(quiet=True)
        )
        
        await status.edit("Uploading… almost done")
        await m.reply_video(output_path, caption="Hardsub complete ✅\nYour hard-subbed video")
        
        # Cleanup
        for f in [video_path, sub_path, output_path]:
            try: os.remove(f)
            except: pass
        del user_states[user_id]
        await status.delete()
        
    except Exception as e:
        await status.edit(f"Error ho gaya: {str(e)}")
        # Cleanup on error
        for f in [video_path, sub_path]:
            try: os.remove(f)
            except: pass

app.run()import os
import asyncio
import pysubs2
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("hardsubbot", bot_token=os.getenv("TOKEN"))

VIDEO_DIR = "./downloads/"
os.makedirs(VIDEO_DIR, exist_ok=True)

user_states = {}

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply("Video bhejo → usko reply mein /hardsub karo → phir .ass subtitle forward karo\nMain hardsub karke de dunga ✅")

@app.on_message(filters.command("hardsub") & filters.reply)
async def set_video(c, m: Message):
    if not m.reply_to_message.video and not m.reply_to_message.document:
        return await m.reply("Video ya video file ko reply karo /hardsub se")
    
    user_states[m.from_user.id] = {"video": m.reply_to_message}
    await m.reply("Ab .ass subtitle file forward kar do")

@app.on_message(filters.document & filters.regex(r"\.ass$", flags=0))
async def process(c, m: Message):
    user_id = m.from_user.id
    if user_id not in user_states:
        return
    
    status = await m.reply("Downloading video + subtitle… thoda wait karo")
    
    video_msg = user_states[user_id]["video"]
    video_path = await video_msg.download(VIDEO_DIR)
    sub_path = await m.download(VIDEO_DIR)
    output_path = VIDEO_DIR + f"hardsub_{user_id}.mkv"
    
    try:
        await status.edit("Hardsubbing chal raha hai… 480p-1080p tak support hai")
        
        i = ffmpeg.input(video_path)
        (
            ffmpeg
            .input(video_path)
            .output(output_path,
                    vf=f"subtitles={sub_path.replace(':', '\\\\:')}",
                    c_v="libx264", preset="veryfast", crf=23,
                    c_a="copy")
            .overwrite_output()
            .run(quiet=True)
        )
        
        await status.edit("Uploading… almost done")
        await m.reply_video(output_path, caption="Hardsub complete ✅\nYour hard-subbed video")
        
        # Cleanup
        for f in [video_path, sub_path, output_path]:
            try: os.remove(f)
            except: pass
        del user_states[user_id]
        await status.delete()
        
    except Exception as e:
        await status.edit(f"Error ho gaya: {str(e)}")
        # Cleanup on error
        for f in [video_path, sub_path]:
            try: os.remove(f)
            except: pass

app.run()
