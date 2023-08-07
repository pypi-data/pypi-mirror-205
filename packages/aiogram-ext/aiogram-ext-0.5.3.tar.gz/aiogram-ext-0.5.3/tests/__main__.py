from botty import dp, Message, reply, bot


@dp.command("test")
async def _(msg: Message):
    print(bot.url)
    print(bot.start_url)
    print(bot.startgroup_url)
    await reply(msg, "test1")


@dp.command("test").state().has_reply
def _(msg: Message):
    return reply(msg, "test*")


dp.run()
