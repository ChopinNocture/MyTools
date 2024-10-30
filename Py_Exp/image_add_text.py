from PIL import Image, ImageDraw, ImageFont

# 打开一个图片
image = Image.open('你的图片路径.jpg')

# 创建一个可以在图片上绘图的对象
draw = ImageDraw.Draw(image)

# 加载字体
font = ImageFont.truetype('arial.ttf', 36)  # 确保你有这个字体文件或者替换为你有的字体

# 文字和位置
text = "你好，世界"
x, y = 50, 50  # 指定初始位置

# 获取文本的宽度和高度
text_width, text_height = draw.textsize(text, font=font)

# 计算居中位置
centered_x = x - text_width // 2
centered_y = y - text_height // 2

# 添加文字到图片
draw.text((centered_x, centered_y), text, (255, 255, 255), font=font, anchor="mm")

# 保存图片
image.save('加了文字的图片.jpg')

# 显示结果（可选）
image.show()
