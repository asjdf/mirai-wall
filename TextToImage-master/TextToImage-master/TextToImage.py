from PIL import Image, ImageDraw, ImageFont
import textwrap
import random


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
    segments = subsection(string);
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


def text2multigraph(string, poster, backdrop, fontsize=20, x=20, y=40, spacing=20):
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


if __name__ == "__main__":
    f = open("a.txt",'r', encoding='UTF-8')
    str = f.read()
    f.close()
    imgs = text2multigraph(str, "(回复1)", Image.new('RGB', (700, 1000), (255, 255, 255)))
    for img in imgs:
        img.show()
    # img=text2piiic(str,"(回复1)",30)
    # img.show()
