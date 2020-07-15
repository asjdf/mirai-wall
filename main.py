from mirai import Mirai, Plain, MessageChain, Friend, FriendMessage
import asyncio

qq = 3453167438 # 字段 qq 的值
authKey = '1234567890' # 字段 authKey 的值
mirai_api_http_locate = '127.0.0.1:8080/' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

recordingList = []
note = {'1000': 'test'}

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    print(message.toString())
    print(friend)
    print(type(friend))
    if message.toString() == "/end":
        recordingList.remove(friend.id)
        await app.sendFriendMessage(friend, [
            Plain(text=note[str(friend.id)])
        ])
    if friend.id in recordingList:
        note[str(friend.id)] = note[str(friend.id)] + message.toString()
        print(note)
    if message.toString() == "/start":
        await app.sendFriendMessage(friend, [
            Plain(text="开始记录")
        ])
        note[str(friend.id)] = ''
        recordingList.append(friend.id)
    await app.sendFriendMessage(friend, [
        Plain(text="Hello, world!")
    ])

if __name__ == "__main__":
    app.run()

# type=<MessageItemType.FriendMessage: 'FriendMessage'>
# messageChain=MessageChain(
#   __root__=[Source(type=<MessageComponentTypes.Source: 'Source'>, id=19539, time=datetime.datetime(2020, 7, 9, 5, 35, 25, tzinfo=datetime.timezone.utc))
#   , Plain(type=<MessageComponentTypes.Plain: 'Plain'>, text='n')])
# sender=<Friend id=243852814 nickname='Atom' remark=''>