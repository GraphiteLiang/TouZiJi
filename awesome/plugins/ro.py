from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp.message import MessageSegment
import random
import re


@on_command('ro', aliases=('ro'), only_to_me=False)
async def ro(session: CommandSession):
    userid = session.ctx['user_id']
    result = ""

    if session.get('readable') == 1:
        array, result = calculate(session.get('expression'))
        result = MessageSegment.at(userid) + '投掷为' + str(array) + "合计为" + str(result)
    elif session.get('readable') == 2:
        skill = session.get('skill')
        ability = session.get('ability')
        _, result = roll(1, 100)
        success = issuccess(result, ability)
        result = MessageSegment.at(userid) + '投掷的' + skill + '为' + str(result) + ',' + success
    elif session.get('readable') == 3:
        skill = session.get('skill')
        ability = session.get('ability')
        _, tmp1 = roll(1, 100)
        _, tmp2 = roll(1, 100)
        if tmp1 == 100:
            tmp1 = 0
        if tmp2 == 100:
            tmp2 = 0
        result1 = max(tmp1 / 10, tmp2 / 10)
        result2 = min(tmp1 % 10, tmp2 % 10)
        result = int(result1) * 10 + result2
        success = issuccess(result, ability)
        result = MessageSegment.at(userid) + '投掷的' + skill + '为[' + \
                 str(tmp1) + ', ' + str(tmp2) + "]计算惩罚骰结果为" + str(result) + success
    elif session.get('readable') == 4:
        skill = session.get('skill')
        ability = session.get('ability')
        _, tmp1 = roll(1, 100)
        _, tmp2 = roll(1, 100)
        if tmp1 == 100:
            tmp1 = 0
        if tmp2 == 100:
            tmp2 = 0
        result1 = min(tmp1 / 10, tmp2 / 10)
        result2 = max(tmp1 % 10, tmp2 % 10)
        result = int(result1) * 10 + result2
        success = issuccess(result, ability)
        result = MessageSegment.at(userid) + '投掷的' + skill + '为[' + \
                 str(tmp1) + ', ' + str(tmp2) + "]计算奖励骰结果为" + str(result) + "，" + success
    else:
        result = "骰娘无法读懂您的参数呢QAQ"
    with open("command_log.txt", "a") as f:
        f.write(str(result))
    await session.send(result)


@ro.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    pattern1 = "[0-9]*d[0-9].*"
    pattern2 = ".* [0-9]*"
    pattern3 = "-pu .* [0-9]*"
    pattern4 = "-rw .* [0-9]*"
    if stripped_arg:
        if re.match(pattern1, stripped_arg):
            session.state['readable'] = 1
            session.state['expression'] = stripped_arg
            return
        elif re.match(pattern3, stripped_arg):
            session.state['readable'] = 3
            args = stripped_arg.split(' ')
            session.state['skill'] = args[1]
            session.state['ability'] = int(args[2])
            return
        elif re.match(pattern4, stripped_arg):
            session.state['readable'] = 4
            args = stripped_arg.split(' ')
            session.state['skill'] = args[1]
            session.state['ability'] = int(args[2])
        elif re.match(pattern2, stripped_arg):
            session.state['readable'] = 2
            args = stripped_arg.split(' ')
            session.state['skill'] = args[0]
            try:
                session.state['ability'] = int(args[1])
            except ValueError:
                session.state['readable'] = -1
            return
        else:
            session.state['readable'] = -1
            return
    if not stripped_arg:
        session.state['readable'] = 1;
        session.state['expression'] = '1d100'
        return


def roll(num: int, max: int):
    result = 0
    array = []
    if num > 20:
        return array, "个数太多骰娘数不过来啦QAQ"
    for i in range(num):
        tmp = random.randint(1, max)
        result += tmp
        array.append(tmp)
    return array, result


def issuccess(result, ability):
    success = ''
    if result == 1:
        success = '大成功'
    elif result <= ability / 5:
        success = '极难成功'
    elif result <= ability / 2:
        success = '困难成功'
    elif result <= ability:
        success = '成功'
    elif result == 100:
        success = '大失败'
    elif result > 95:
        if ability < 50:
            success = '大失败'
        else:
            success = "失败"
    elif result > ability:
        success = '失败'
    return success


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        pass
    return False


def get_roll_result(op, x, y):
    arr, res = roll(x, y)
    return arr, res


def calculate(args):
    stack = []
    arr_result = []
    result = 0
    n = len(args)
    lastOp = '+'
    i = 0
    while i < n:
        if is_number(args[i]):
            tmp = int(args[i])
            while i + 1 < n and is_number(args[i + 1]):
                i += 1
                tmp = tmp * 10 + int(args[i])
            if lastOp == '+':
                stack.append(tmp)
            elif lastOp == '-':
                stack.append(-tmp)
            else:
                arr, roo_result = get_roll_result(lastOp, stack.pop(), tmp)
                arr_result.append(arr)
                stack.append(roo_result)
        else:
            lastOp = args[i]
        i += 1

    for i in stack:
        result += i
    return arr_result, result
