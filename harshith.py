import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Info Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)



@Bot.on_message(filters.private & filters.command("mhinfo"))
async def info(bot, update):
    
    text = f"""--**Information from Mutyala Harshith**--
**💞 First Name :** {update.from_user.first_name}
**😎 Your Second Name :** {update.from_user.last_name if update.from_user.last_name else 'None'}
**🥳 Your Username :** {update.from_user.username}
**😜 Your Telegram ID :** {update.from_user.id}
**🤫 Your Profile Link :** {update.from_user.mention}"""
    
    await update.reply_text(        
        text=text,
        disable_web_page_preview=True,
        reply_markup=BUTTONS
    )

   
@Bot.on_message(filters.private & filters.audio)
async def tag(bot, m):
    mes = await m.reply("`Downloading...`", parse_mode='md')
    await m.download(f"temp/{m.audio.file_name}.mp3")
    music = load_file(f"temp/{m.audio.file_name}.mp3")

    try:
        artwork = music['artwork']
        image_data = artwork.value.data
        img = Image.open(io.BytesIO(image_data))
        img.save("temp/artwork.jpg")
    except ValueError:
        image_data = None

    await mes.delete()
    fname = await bot.ask(m.chat.id,'`Send the Filename`', filters=filters.text, parse_mode='Markdown')
    title = await bot.ask(m.chat.id,'`Send the Title name`', filters=filters.text, parse_mode='Markdown')
    artist = await bot.ask(m.chat.id,'`Send the Artist(s) name`', filters=filters.text, parse_mode='Markdown')
    answer = await bot.ask(m.chat.id,'`Send the Artwork or` /skip', filters=filters.photo | filters.text, parse_mode='Markdown')
    music.remove_tag('artist')
    music.remove_tag('title')
    music['artist'] = artist.text
    music['title'] = title.text

    if answer.photo:
        await bot.download_media(message=answer.photo, file_name="temp/artwork.jpg")
        music.remove_tag('artwork')
        with open('temp/artwork.jpg', 'rb') as img_in:
            music['artwork'] = img_in.read()
    music.save()

    try:
        await bot.send_audio(chat_id=m.chat.id, file_name=fname.text, performer=artist.text, title=title.text, duration=m.audio.duration, audio=f"temp/{m.audio.file_name}.mp3", thumb='temp/artwork.jpg' if answer.photo or image_data else None)
    except Exception as e:
        print(e)
        return
    os.remove(f"temp/{m.audio.file_name}.mp3")
