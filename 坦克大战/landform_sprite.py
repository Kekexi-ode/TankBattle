import pygame


pygame.init()


'''
砖墙类
提供了横向创建、竖向创建、矩形创建等方法
'''
class BrickWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  #继承模版类
        self.brick_wall = pygame.image.load('砖墙1.png').convert_alpha()    #加载图片

        self.image = self.brick_wall
        self.rect = self.brick_wall.get_rect(center=(x, y))            #定义墙的位置
        self.x = x
        self.y = y


    '''
    创建一排竖直的墙
    参数为（开始x坐标，开始y坐标，建造长度）
    '''
    @classmethod                                             #这是类方法装饰器，用这个可以直接通过当前方法创建实例
    def vertical_wall(cls, start_x, start_y, long):     #cls表示这个类，等价于BrickWall(x, y)
        walls = []
        for i in range(long):                               #range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x, start_y+i*68)

            walls.append(wall)
        return walls


    '''
    创建一排横向的墙
    '''
    @classmethod
    def horizontal_wall(cls, start_x, start_y, long):
        walls = []
        for i in range(long):        # range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x+i*68, start_y)

            walls.append(wall)
        return walls


    """创建一坨墙,可以选择填不填充
    输入开始坐标x,y和x、y方向长度,
    在此区间内填充满墙"""
    @classmethod
    def rect_walls(cls, x, y, x_long, y_long, solid=False):
        walls = []
        for i in range(x_long):
            for j in range(y_long):
                #下面这一坨是在判定墙块是否要被填充或位于边框上，因为在循环最里面，所以每建一个墙都会判定一下
                if solid or i == 0 or i == x_long - 1 or j == 0 or j == y_long - 1:
                    wall = cls(x+i*68, y+j*68)
                    walls.append(wall)
        return walls


#铁墙
class IronWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # 继承模版类
        self.brick_wall = pygame.image.load('铁墙.png').convert_alpha()  # 加载图片

        self.image = self.brick_wall
        self.rect = self.brick_wall.get_rect(center=(x, y))  # 定义墙的位置
        self.x = x
        self.y = y


    '''
    创建一排竖直的墙
    参数为（开始x坐标，开始y坐标，建造长度）
    '''

    @classmethod  # 这是类方法装饰器，用这个可以直接通过当前方法创建实例
    def vertical_wall(cls, start_x, start_y, long):  # cls表示这个类，等价于BrickWall(x, y)
        walls = []
        for i in range(long):  # range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x, start_y + i * 68)

            walls.append(wall)
        return walls

    '''
    创建一排横向的墙
    '''

    @classmethod
    def horizontal_wall(cls, start_x, start_y, long):
        walls = []
        for i in range(long):  # range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x + i * 68, start_y)

            walls.append(wall)
        return walls

    """创建一坨墙,可以选择填不填充
    输入开始坐标x,y和x、y方向长度,

    在此区间内填充满墙"""

    @classmethod
    def rect_walls(cls, x, y, x_long, y_long, solid=False):
        walls = []
        for i in range(x_long):
            for j in range(y_long):
                # 下面这一坨是在判定墙块是否要被填充或位于边框上，因为在循环最里面，所以每建一个墙都会判定一下
                if solid or i == 0 or i == x_long - 1 or j == 0 or j == y_long - 1:
                    wall = cls(x + i * 68, y + j * 68)
                    walls.append(wall)
        return walls


#水池
class Pool(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # 继承模版类
        self.brick_wall = pygame.image.load('pool.png').convert_alpha()  # 加载图片

        self.image = self.brick_wall
        self.rect = self.brick_wall.get_rect(center=(x, y))  # 定义墙的位置
        self.x = x
        self.y = y


    '''
    创建一排竖直的墙
    参数为（开始x坐标，开始y坐标，建造长度）
    '''

    @classmethod  # 这是类方法装饰器，用这个可以直接通过当前方法创建实例
    def vertical_wall(cls, start_x, start_y, long):  # cls表示这个类，等价于BrickWall(x, y)
        walls = []
        for i in range(long):  # range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x, start_y + i * 68)

            walls.append(wall)
        return walls

    '''
    创建一排横向的墙
    '''

    @classmethod
    def horizontal_wall(cls, start_x, start_y, long):
        walls = []
        for i in range(long):  # range（long)表示一个从0到long的数组，不包括long
            wall = cls(start_x + i * 68, start_y)

            walls.append(wall)
        return walls

    """创建一坨墙,可以选择填不填充
    输入开始坐标x,y和x、y方向长度,

    在此区间内填充满墙"""

    @classmethod
    def rect_walls(cls, x, y, x_long, y_long, solid=False):
        walls = []
        for i in range(x_long):
            for j in range(y_long):
                # 下面这一坨是在判定墙块是否要被填充或位于边框上，因为在循环最里面，所以每建一个墙都会判定一下
                if solid or i == 0 or i == x_long - 1 or j == 0 or j == y_long - 1:
                    wall = cls(x + i * 68, y + j * 68)
                    walls.append(wall)
        return walls
