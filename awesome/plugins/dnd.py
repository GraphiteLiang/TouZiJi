from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp.message import MessageSegment
import random


@on_command('dnd', aliases=('dnd'),only_to_me=False)
async def coc(session: CommandSession):
    userid = session.ctx["user_id"]
    result = "DND5E投掷结果"
    for i in range(6):
        result += "\n"+str(get_dnd())
    await session.send(MessageSegment.at(userid)+result)


def get_dnd():
    result = []
    for i in range(6):
        result.append(roll())
    return result

def roll():
    result = []
    for i in range(4):
        result.append(random.randint(1, 6));
    result.sort()
    return result[1] + result[2] + result[3]
