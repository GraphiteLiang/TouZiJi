from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp.message import MessageSegment
import random
@on_command('rd', aliases=('rd',"投掷","r"),only_to_me=False)
async def rd(session: CommandSession):
    userid = session.ctx["user_id"]
    number = session.get('num')
    max = session.get('max')
    result = await get_result(number, max, userid)
    await session.send(result)

@rd.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    nam = stripped_arg.split("d")
    if stripped_arg:
        session.state['num'] = int(nam[0])
        session.state['max'] = int(nam[1])
        return
    if not stripped_arg:
        session.state['num'] = 1
        session.state['max'] = 100
        return
async def get_result(num: int, max:int, userid) -> str:
    result = 0
    result_string = ""
    if num > 20:
        return "个数太多骰娘数不过来啦QAQ"
    for i in range(num):
        result_string += "," + str(random.randint(1, max))
    result_string = MessageSegment.at(userid)+"投掷结果为"+result_string
    return result_string
