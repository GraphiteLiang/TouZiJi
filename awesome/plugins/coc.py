from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp.message import MessageSegment
import random

@on_command('coc', aliases=('coc'),only_to_me=False)
async def coc(session: CommandSession):
    userid = session.ctx["user_id"]
    attribute = ['力量','体质','体型','敏捷','外貌','智力','意志','教育','幸运']
    result = "COC7版投掷结果\n"
    for i in range(6):
        tmp = get_coc()
        for j in range(9):
            result = result + attribute[j] + ":" + str(tmp[j]);
        result = result + '\n'
    await session.send(MessageSegment.at(userid)+result)


def get_coc():
    result = []
    STR = roll(3, 6) * 5
    CON = roll(3, 6) * 5
    SIZ = (roll(2, 6) + 6) * 5
    DEX = roll(3, 6) * 5
    APP = roll(3, 6) * 5
    INT = (roll(2, 6) + 6) * 5
    POW = roll(3, 6) * 5
    EDU = (roll(2, 6) + 6) * 5
    LUK = (roll(3, 6)) * 5
    result = [STR, CON, SIZ, DEX, APP, INT, POW, EDU, LUK]
    return result
def roll(num: int, max:int):
    result = 0
    if num > 20:
        return "个数太多骰娘数不过来啦QAQ"
    for i in range(num):
        result += random.randint(1, max)
    return result
