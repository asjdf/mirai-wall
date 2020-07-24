from mirai import Mirai, Plain, MessageChain, Friend, FriendMessage, Image
import asyncio
import TextToImage as t2i
from Qzone_auto_twitter import QzoneSpider as autoTwitter
import base64
from io import BytesIO
import requests
from PIL import Image as PIL_img
import io
from dotenv import load_dotenv
# 加载环境变量
load_dotenv(verbose=True, override=True, encoding='utf-8')
qq = os.getenv('YOUR_QQ') # 字段 qq 的值
authKey = '1234567890' # 字段 authKey 的值
mirai_api_http_locate = '127.0.0.1:8080/' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

recordingList = {}
# 记录正在记录中的QQ 存在key则说明正在记录 值为0为正在记录 值为1表示记录完成 正在询问是否匿名 值为2表示正在询问是否发送
note = {'1000': 'test'}
note2 = {'1000': 'test'}
# 记录留言的内容
anonymous = {}
# 记录是否匿名 0为不匿名 1为匿名

#二维字典添加数据
def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        if key_b in thedict[key_a]:
            val = thedict[key_a][key_b] + val
            thedict[key_a].update({key_b: val})
        else:
            thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    if message.hasComponent(Plain):
        for content in message.getAllofComponent(Plain):
            addtwodimdict(note2, str(friend.id), 'text', content.toString())
        addtwodimdict(note2, str(friend.id), 'text', '\n')
    if message.hasComponent(Image):
        addtwodimdict(note2, str(friend.id), 'image', message.getAllofComponent(Image))

    
    # 记录留言
    if message.toString() == "end" and recordingList[str(friend.id)] == 0:
        recordingList[str(friend.id)] = 1
        if 'text' in note[str(friend.id)]:
            note[str(friend.id)]['text'] = note[str(friend.id)]['text'].rstrip()
            await app.sendFriendMessage(friend, [ 
                Plain(text=note[str(friend.id)]['text'])
            ])
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 0:
        if message.hasComponent(Plain):
            for content in message.getAllofComponent(Plain):
                addtwodimdict(note, str(friend.id), 'text', content.toString())
            addtwodimdict(note, str(friend.id), 'text', '\n')
        if message.hasComponent(Image):
            addtwodimdict(note, str(friend.id), 'image', message.getAllofComponent(Image))
        print(note)
    if message.toString() == "发帖" and str(friend.id) not in recordingList:
        await app.sendFriendMessage(friend, [
            Plain(text="开始记录")
        ])
        recordingList[str(friend.id)] = 0
    if str(friend.id) not in recordingList:
        await app.sendFriendMessage(friend, [
            Plain(text='hi!需要给墙留言请发送:"发帖",结束留言请发送:"end",请按提示进行操作.暂不支持表情哦!图片会单发')
        ])
    # 记录是否匿名
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 1:
        if message.toString() == "是":
            anonymous[str(friend.id)] = 1
            recordingList[str(friend.id)] = 2
            if 'text' in note[str(friend.id)]:
                await app.sendFriendMessage(friend, [
                    Plain(text=f"请再次确认您的留言:\n{note[str(friend.id)]['text']}\n是否匿名:是\n请在确认后回复(发送/取消)")
                ])
            else:
                await app.sendFriendMessage(friend, [
                    Plain(text=f"是否匿名:是\n请在确认后回复(发送/取消)")
                ])
        elif message.toString() == "否":
            anonymous[str(friend.id)] = 0
            recordingList[str(friend.id)] = 2
            if 'text' in note[str(friend.id)]:
                await app.sendFriendMessage(friend, [
                    Plain(text=f"请再次确认您的留言:\n{note[str(friend.id)]['text']}\n是否匿名:否\n请在确认后回复(发送/取消)")
                ])
            else:
                await app.sendFriendMessage(friend, [
                    Plain(text=f"是否匿名:否\n请在确认后回复(发送/取消)")
                ])
        else:
            await app.sendFriendMessage(friend, [
                Plain(text='上面是您留言的内容,请问是否匿名?(是/否)')
            ])
    if str(friend.id) in recordingList and recordingList[str(friend.id)] == 2:
        if message.toString() == "发送":
            picCache = []
            if anonymous[str(friend.id)] == 0:
                if 'text' in note[str(friend.id)]:
                    img=t2i.text2piiic2(friend.id, note[str(friend.id)]['text'],20,qName = friend.nickname)#图片生成
                else:
                    img=t2i.text2piiic2('', '无文字消息',20)#图片生成
            if anonymous[str(friend.id)] == 1:
                if 'text' in note[str(friend.id)]:
                    img=t2i.text2piiic2('', note[str(friend.id)]['text'],20)#图片生成
                else:
                    img=t2i.text2piiic2('', '无文字消息',20)#图片生成
            # 图片转换为base64
            output_buffer = BytesIO()
            img.save(output_buffer, format='PNG')
            base64_str = base64.b64encode(output_buffer.getvalue())
            picCache.append(base64_str)
            # 附加图片下载
            if 'image' in note[str(friend.id)]:
                print('存在附加图片')
                for img in note[str(friend.id)]['image']:
                    r = requests.get(img.url, stream=True)
                    if r.status_code == 200:
                        a = PIL_img.open(io.BytesIO(r.content))
                        b = BytesIO()
                        a.save(b, format='PNG')
                        base64_str = base64.b64encode(b.getvalue())
                        picCache.append(base64_str)
            print(picCache)
            for pic in picCache:
                print(pic)
                print('\n')

            # 图片发送
            autoTwitter().pImg(msg = '',pic = picCache)
            await app.sendFriendMessage(friend, [
                Plain(text='已发送,请在万能墙空间查看')
            ])
            # 清除缓存
            del anonymous[str(friend.id)]
            del recordingList[str(friend.id)]
            del note[str(friend.id)]
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