from json_db_class import JSONTool
JSONTool = JSONTool()
import random
from config import NICKNAME_ADJ, NICKNAME_SUBJ

def check_user_in_db(msg, db): 
    if str(msg.from_user.id) not in db["Users"]:
        db["Users"][f"{msg.from_user.id}"] = {}
        db["Users"][f"{msg.from_user.id}"]["chat_nickname"] = f"{random.choice(NICKNAME_ADJ)} {random.choice(NICKNAME_SUBJ)}"
        JSONTool.save_db(db=db, url='db.json')

def is_user_in_room(msg, db):
    if str(msg.from_user.id) in db["Room"]["users_in"]:
        return True