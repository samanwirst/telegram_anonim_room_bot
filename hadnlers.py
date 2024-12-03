from aiogram import Dispatcher, types
from json_db_class import JSONTool
JSONTool = JSONTool()
import utils
from config import BOT

bot_commands = ['start', 'help', 'set_name', 'my_name', 'join', 'online', 'exit']
bot = BOT

async def answer_commands(msg: types.Message):
    global db

    try:
        db = JSONTool.load_db('db.json')
    except:
        new_db = {
            "Users": {},
            "Room": {
                "users_in": {}
            }
        }
        JSONTool.save_db(db=new_db, url='db.json')
        db = JSONTool.load_db('db.json')
        
    utils.check_user_in_db(msg, db)
    
    if msg.text == "/start":
        await msg.answer(f'Привет!\nЭтот бот откроет тебе врата в анонимную чат-комнату.\n\nТебе был выдан случайный никнейм: "{db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}"\nНо ты можешь в любое время изменить его на свой\n\nПропиши /help для большей информации')
    if msg.text == "/help":
        await msg.answer("Анонимная чат-комната — это специальное виртуальное пространство, в котором все твои личные данные аккаунта скрываются от других участников. Тут у нас полная свобода, ты можешь поставить себе абсолютно любое имя, писать все, что душе угодно, а кто ты такое до сих пор никто не знает\n\nПробежимся по основным командам:\n\n/start — Вызвать приветственное сообщение\n/help — Вызвать это сообщение\n\n/set_name — Установить никнейм, который будет отображаться в чат-комнате\n/my_name — Узнать свой активный никнейм\n/join — Вступить в чат-комнату\n/online — Список участников, которые в находятся в чат-комнате\n/exit — Выйти из чат-комнаты")

    if msg.text.startswith("/set_name"):
        if msg.text != "/set_name":
            new_name = msg.text.replace('/set_name ', '')
            db["Users"][f"{msg.from_user.id}"]["chat_nickname"] = new_name
            JSONTool.save_db(db=db, url='db.json')
            await msg.reply(f"Имя было изменено на: {new_name}")
        else:
            await msg.reply(f"Неверный синтаксис!\n\nПример правильного использования:\n/set_name Твоё Имя")
    
    if msg.text == "/my_name":
        await msg.reply(f'Твой активный никнейм: {db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}')

    if msg.text == "/join":
        if str(msg.from_user.id) not in db["Room"]["users_in"]:
            db["Room"]["users_in"].append(f"{msg.from_user.id}")
            JSONTool.save_db(db=db, url='db.json')
            
            for i in range(len(db["Room"]["users_in"])):
                await bot.send_message(db["Room"]["users_in"][i], f'{db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}, присоедининяется к комнате')
        else: 
            await msg.reply("Ты уже в комнате!")
    
    if msg.text == "/online":
        in_online = ""
        for i in range(len(db["Room"]["users_in"])):
            in_online += f'\n{i+1}. {db["Users"][db["Room"]["users_in"][i]]["chat_nickname"]}'
        await msg.answer(f'В онлайне сейчас:\n {in_online}')

    if msg.text == "/exit":
        if utils.is_user_in_room(msg, db):
            for i in range(len(db["Room"]["users_in"])):
                await bot.send_message(db["Room"]["users_in"][i], f'{db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}, выходит из комнаты')
            
            db["Room"]["users_in"].remove(f"{msg.from_user.id}")
            JSONTool.save_db(db=db, url='db.json')

        else: 
            await msg.reply("Тебя и так нет в комнате :/")

async def answer_messages(msg: types.Message):
    for command in bot_commands:
        if not msg.text.startswith(command):
            if utils.is_user_in_room(msg, db):
                for i in range(len(db["Room"]["users_in"])):
                    if db["Room"]["users_in"][i] != str(msg.from_user.id):
                        await bot.send_message(db["Room"]["users_in"][i], f'{db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}:\n\n{msg.text}')

async def answer_photo(msg: types.Message):
    if utils.is_user_in_room(msg, db):
        for i in range(len(db["Room"]["users_in"])):
            if db["Room"]["users_in"][i] != str(msg.from_user.id):
                if msg.caption == None:
                    msg.caption = ""
                await bot.send_photo(db["Room"]["users_in"][i], msg.photo[0].file_id, f'{db["Users"][f"{msg.from_user.id}"]["chat_nickname"]}:\n\n{msg.caption}')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(answer_commands, commands=bot_commands)
    dp.register_message_handler(answer_messages, content_types=['text'])
    dp.register_message_handler(answer_photo, content_types=['photo'])