# 文字转换为长图
# text2piiic(string, poster, length, fontsize=20, x=20, y=40, spacing=20)
# string: 需要转换的文字
# poster：每一段末尾需要添加的内容
# length：图片一行的文字个数
# fontsize：字体大小
# x：文字的起始位置
# y：文字的起始位置
# spacing：文字行间距
# return：生成的长图,PIL 模块的 Image 类型

# 文字根据图片转换为多图
# text2multigraph(string, poster, backdrop, fontsize=20, x=20, y=40, spacing=20)
# string: 需要转换的文字
# poster：每一段末尾需要添加的内容
# backdrop：背景图片，PIL 模块的 Image 类型
# fontsize：字体大小
# x：文字的起始位置
# y：文字的起始位置
# spacing：文字行间距
# return：生成的长图列表,PIL 模块的 Image 类型

from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
import requests
import io


def subsection(string):
    return string.split('\n')


def carry(x, y):
    if x % y != 0:
        return (x // y + 1)
    return x // y


def insert_poster(sections, poster, num=3):
    if num > len(sections):
        num = len(sections)
    poster_pos = [random.randint(0, len(sections)) for _ in range(num)]
    for i in range(len(sections)):
        if i in poster_pos:
            sections[i] = sections[i] + poster
    return sections


def linefeed(sections, length):
    stringlins = []
    for section in sections:
        strs = textwrap.fill(section, length).split('\n')
        stringlins = stringlins + strs
    return stringlins


def text2lins(string, poster, length):
    segments = subsection(string)
    segments = insert_poster(segments, poster)
    string_lins = linefeed(segments, length)
    return string_lins


def text2piiic(string, poster, length, fontsize=20, x=20, y=40, spacing=20):
    lins = text2lins(string, poster, length)
    heigh = y * 2 + (fontsize + spacing) * len(lins)
    width = x * 2 + fontsize * length
    font = ImageFont.truetype('./simhei.ttf', fontsize, encoding="utf-8")
    picture = Image.new('RGB', (width, heigh), (255, 255, 255))
    draw = ImageDraw.Draw(picture)
    for i in range(len(lins)):
        y_pos = y + i * (fontsize + spacing)
        draw.text((x, y_pos), lins[i], font=font, fill=(0, 0, 0))
    return picture


def text2piiic2(qq, string, length, poster = '', qName = '匿名', fontsize=40, x=20, y=30, spacing=20):
    lins = text2lins(string, poster, length)
    heigh = y * 2 + (fontsize + spacing) * len(lins) + 60
    width = x * 2 + fontsize * length
    font = ImageFont.truetype('./simhei.ttf', fontsize, encoding="utf-8")
    picture = Image.new('RGB', (width, heigh), (255, 255, 255))
    draw = ImageDraw.Draw(picture)
    # 文字绘制
    for i in range(len(lins)):
        y_pos = y + i * (fontsize + spacing)
        draw.text((x, y_pos), lins[i], font=font, fill=(0, 0, 0))
    # 下划线绘制
    draw.line((10,heigh - 60,width-10,heigh - 60),fill = '#000000')
    # 名称绘制(字体本身自带offset的，需要减去)
    qName_width, qName_height = draw.textsize(qName, font)
    draw.text((width-130-qName_width-font.getoffset(qName)[0], heigh-55), qName, font=font, fill=(0, 0, 0))
    # 头像绘制
    if qq != '':
        r = requests.get('http://q1.qlogo.cn/g?b=qq&nk='+ str(qq) +'&s=640', stream=True)
        if r.status_code == 200:
            headPic = Image.open(io.BytesIO(r.content))
    else:
        headPic = Image.open('./headPic.jpg')
    headPic.thumbnail((100,100))
    headPic = circle_corner(headPic, 50)
    r,g,b,a = headPic.split()
    picture.paste(headPic, (width - 120,heigh - 110), mask = a)
    return picture


def text2multigraph(string, poster, backdrop, fontsize=20, x=20, y=40, spacing=15):
    row = (backdrop.width - x * 2) // fontsize
    lin = carry((backdrop.height - y * 2), (fontsize + spacing))
    str_lin = text2lins(string, poster, row)
    str_lin_len = len(str_lin)
    num_lin = carry(str_lin_len, lin)
    font = ImageFont.truetype('simhei.ttf', fontsize, encoding="utf-8")
    imgs = []
    for num in range(num_lin):
        img = backdrop.copy()
        draw = ImageDraw.Draw(img)
        for i in range(lin):
            if (num * lin + i) < str_lin_len:
                draw.text((x, y + i * (fontsize + spacing)), str_lin[num * lin + i], font=font, fill=(0, 0, 0))
            else:
                break
        imgs.append(img)
    return imgs

# 矩形图像转为圆角矩形
def circle_corner(img, radii):
	# 画圆（用于分离4个角）
	circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
	# circle.save('1.jpg','JPEG',qulity=100)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形
	# circle.save('2.jpg','JPEG',qulity=100)
 
	# 原图转为带有alpha通道（表示透明程度）
	img = img.convert("RGBA")
	w, h = img.size
 
	# 画4个角（将整圆分离为4个部分）
	alpha = Image.new('L', img.size, 255)	#与img同大小的白色矩形，L 表示黑白图
	# alpha.save('3.jpg','JPEG',qulity=100)
	alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
	alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
	alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
	alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
	# alpha.save('4.jpg','JPEG',qulity=100)
 
	img.putalpha(alpha)		# 白色区域透明可见，黑色区域不可见
	return img

if __name__ == "__main__":
    # f = open("a.txt",'r', encoding='UTF-8')
    # str = f.read()
    # f.close()
    # imgs = text2multigraph(str, "(回复1)", Image.new('RGB', (700, 1000), (255, 255, 255)))
    # for img in imgs:
    #     img.show()
    # img=text2piiic(str,"(回复1)",30)
    # img.show()
    img=text2piiic2(qq = '',string = '我觉得没有得没有有的实力地方爱上了大幅拉升的实力地方爱上了大幅拉升的房间里睡觉了附件是解放拉升的房间里睡觉了附件是解放',poster = '',length = 15)
    img.show()
