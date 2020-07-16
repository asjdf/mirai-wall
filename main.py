from mirai import Mirai, Plain, MessageChain, Friend, FriendMessage
import asyncio
import TextToImage as t2i
from Qzone_auto_twitter import QzoneSpider as autoTwitter
import base64
from io import BytesIO

qq = 3453167438 # 字段 qq 的值
authKey = '1234567890' # 字段 authKey 的值
mirai_api_http_locate = '127.0.0.1:8080/' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

recordingList = {}
# 记录正在记录中的QQ 存在key则说明正在记录 值为0为正在记录 值为1表示记录完成 正在询问是否匿名 值为2表示正在询问是否发送
note = {'1000': 'test'}
# 记录留言的内容
anonymous = {}
# 记录是否匿名 0为不匿名 1为匿名

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    # 记录留言
    if message.toString() == "/end" and recordingList[str(friend.id)] == 0:
        recordingList[str(friend.id)] = 1
        note[str(friend.id)] = note[str(friend.id)].rstrip()
        await app.sendFriendMessage(friend, [
            Plain(text=note[str(friend.id)])
        ])
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 0:
        note[str(friend.id)] = note[str(friend.id)] + message.toString() + '\n'
        print(note)
    if message.toString() == "/start" and str(friend.id) not in recordingList:
        await app.sendFriendMessage(friend, [
            Plain(text="开始记录")
        ])
        note[str(friend.id)] = ''
        recordingList[str(friend.id)] = 0
    # 记录是否匿名
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 1:
        if message.toString() == "是":
            anonymous[str(friend.id)] = 1
            recordingList[str(friend.id)] = 2
            await app.sendFriendMessage(friend, [
                Plain(text=f'请再次确认您的留言:\n{note[str(friend.id)]}\n是否匿名:是\n请在确认后回复(发送/取消)')
            ])
        elif message.toString() == "否":
            anonymous[str(friend.id)] = 0
            recordingList[str(friend.id)] = 2
            await app.sendFriendMessage(friend, [
                Plain(text=f'请再次确认您的留言:\n{note[str(friend.id)]}\n是否匿名:否\n请在确认后回复(发送/取消)')
            ])
        else:
            await app.sendFriendMessage(friend, [
                Plain(text='上面是您留言的内容,请问是否匿名?(是/否)')
            ])
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 2:
        if message.toString() == "发送":
            if anonymous[str(friend.id)] == 0:
                img=t2i.text2piiic2(friend.id, note[str(friend.id)],20,qName = friend.nickname)#图片生成
            if anonymous[str(friend.id)] == 1:
                img=t2i.text2piiic2('', note[str(friend.id)],20)#图片生成
            # 清除缓存
            del anonymous[str(friend.id)]
            del recordingList[str(friend.id)]
            del note[str(friend.id)]
            # 图片转换为base64
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG')
            base64_str = base64.b64encode(output_buffer.getvalue())
            # 图片发送
            autoTwitter().pImg(msg = '',pic = base64_str)
            await app.sendFriendMessage(friend, [
                Plain(text='已发送,请在万能墙空间查看')
            ])
        elif message.toString() == "取消":
            # 清除缓存
            del anonymous[str(friend.id)]
            del recordingList[str(friend.id)]
            del note[str(friend.id)]
            await app.sendFriendMessage(friend, [
                Plain(text='已取消')
            ])
        else:
            await app.sendFriendMessage(friend, [
                Plain(text='如果确认无误,请回复"发送".如果需要取消发送,请回复"取消"')
            ])


if __name__ == "__main__":
    app.run()

# type=<MessageItemType.FriendMessage: 'FriendMessage'>
# messageChain=MessageChain(
#   __root__=[Source(type=<MessageComponentTypes.Source: 'Source'>, id=19539, time=datetime.datetime(2020, 7, 9, 5, 35, 25, tzinfo=datetime.timezone.utc))
#   , Plain(type=<MessageComponentTypes.Plain: 'Plain'>, text='n')])
# sender=<Friend id=243852814 nickname='Atom' remark=''>