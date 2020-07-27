from nonebot import get_bot
import time
bot = get_bot()


@bot.on_message("group")
async def save_log(ctx):
    msg = ctx["message"]
    msg_text = str(msg)
    if "\n" in msg_text:
        tmp = msg_text.split("\n")
        msg_text = ""
        for x in tmp:
            msg_text = msg_text + x
    if msg[0]['type'] == 'text':
        if len(msg_text) >= 2:
            with open ("log/"+str(ctx['group_id'])+".txt", "a") as f:
                f.write("[" + time.asctime(time.localtime(time.time())) + "]" + str(ctx['user_id']) + ":" + msg_text + "\n")
