# TextToImage
- 文字转化为图片
- 可以转换为长图或根据图片大小转换为多图
- `simhei.ttf` 为中文字库文件
- `a.txt` 为测试的文字文件
## 文字转换为长图

text2piiic(string, poster, length, fontsize=20, x=20, y=40, spacing=20)

string: 需要转换的文字

poster：每一段末尾需要添加的内容

length：图片一行的文字个数

fontsize：字体大小

x：文字的起始位置

y：文字的起始位置

spacing：文字行间距\

return：生成的长图,`PIL` 模块的 `Image` 类型
## 文字根据图片转换为多图

text2multigraph(string, poster, backdrop, fontsize=20, x=20, y=40, spacing=20)

string: 需要转换的文字

poster：每一段末尾需要添加的内容

backdrop：背景图片，`PIL` 模块的 `Image` 类型

fontsize：字体大小

x：文字的起始位置

y：文字的起始位置

spacing：文字行间距

return：生成的长图列表,`PIL` 模块的 `Image` 类型
