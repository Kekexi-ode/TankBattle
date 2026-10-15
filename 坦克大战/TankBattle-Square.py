import pygame

pygame.init()

LONG = 680
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, LONG))
pygame.display.set_caption('坦克大战-方块')

#颜色定义
WHITE = (150, 150, 150)
GRET = (210, 210, 210)
RED = (210, 80, 0)
BLUE = (40, 40, 180)
GREEN = (0, 140, 0)
GOLDEN = (255, 255, 18)     #(255, 153, 18)
YELLOW = (255, 140, 0)
ORANGE = (255, 128, 0)
size = 24                #方块大小


#步长变量，控制坦克的单次移动距离
step = 20

#速度变量，控制游戏全局速度
SPEED = 60


#我方坦克的初始位置，（575,606）为下方中间，（1150,606）为右下角。
MyTankX = 575
MyTankY = 606



#函数：绘制一个方块,返回这个方块的位置
def square(x, y, colour=ORANGE):
    pygame.draw.rect(screen, colour, (x, y, size, size))
    list1 = [x, y]
    return list1


#函数：绘制我方坦克
#x,y为车头位置，x,y后可定义颜色,返回所有块的位置
def we_tank(x, y, colour1=ORANGE):
    square(x, y, colour=colour1)
    list2 = []
    a = square(x, y, RED)
    list2.append(a)
    f = square(x-size, y+size)
    list2.append(f)
    b = square(x+size, y+size)
    list2.append(b)
    c = square(x, y+size, RED)
    list2.append(c)
    d = square(x+size, y+2*size)
    list2.append(d)
    e = square(x-size, y+2*size)
    list2.append(e)
    g = square(x, y+2*size)
    list2.append(g)
    return list2


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and MyTankY >= 0:
                MyTankY = MyTankY - step
            if event.key == pygame.K_a and MyTankX >= 0:
                MyTankX = MyTankX - step
            if event.key == pygame.K_s and MyTankY <= 606:
                MyTankY = MyTankY + step
            if event.key == pygame.K_d and MyTankX <= 1150:
                MyTankX = MyTankX + step


        an = we_tank(MyTankX, MyTankY)
        pygame.display.update()


    pygame.time.Clock().tick(SPEED)
    pygame.display.update()