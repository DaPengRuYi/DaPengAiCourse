# 导入 Python 自带的画图工具 turtle（小海龟）
import turtle
# 导入数学库，用来计算爱心的曲线
import math

# 设置窗口标题（出现在窗口最上方）
turtle.title("我的爱心 - Hello Claude")
# 设置窗口背景颜色为浅粉色
turtle.bgcolor("pink")

# 创建一支画笔（就是那只“小海龟”）
pen = turtle.Turtle()
# 把画笔变快一点（速度 0 表示最快）
pen.speed(0)
# 设置画笔颜色为红色
pen.color("red")
# 设置线条粗细为 3
pen.pensize(3)

# 告诉画笔：接下来要用粉色来填充
pen.fillcolor("hotpink")
# 开始记录填充区域（画完爱心轮廓后再填满颜色）
pen.begin_fill()

# 抬起画笔，移动时不留下痕迹
pen.penup()

# 让角度从 0 走到 360 度，一点一点画出爱心
for angle in range(0, 361):
    # 把角度转成弧度（数学公式需要用弧度）
    t = math.radians(angle)
    # 爱心的横坐标公式
    x = 16 * (math.sin(t) ** 3)
    # 爱心的纵坐标公式
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    # 把坐标放大 20 倍，这样爱心更大更好看
    pen.goto(x * 20, y * 20)
    # 第一次到达起点后，放下画笔开始画线
    pen.pendown()

# 结束填充，把爱心轮廓里面填满粉色
pen.end_fill()

# 抬笔移动到爱心下方，准备写字
pen.penup()
pen.goto(0, -250)
# 把画笔（写字）颜色改成深红色
pen.color("darkred")
# 在当前位置写一句话，居中显示，字体大小 24
pen.write("Hello Claude", align="center", font=("Arial", 24, "bold"))

# 画完后把小海龟箭头藏起来
pen.hideturtle()

# 让窗口一直显示，点击窗口才会关闭
turtle.done()
