from typing import Optional, Dict, Callable  #用于解决类型不确定导致的警告
import pygame
import landform


pygame.init()

# 全局变量（会在 init_level_groups 中被赋值）
all_sprites: Optional[pygame.sprite.Group] = None
brick_group: Optional[pygame.sprite.Group] = None
iron_group: Optional[pygame.sprite.Group] = None
pool_group: Optional[pygame.sprite.Group] = None

#坐标换算函数，懒得引用所以复杂了一份
def coordinate(x=None, y=None):
    n = None
    if x is not None:
        n = 35 + 68*x
    if y is not None:
        n = 45 + 68*y
    return n

#初始化函数，用于将主函数中的精灵组导入
def init_level_groups(groups):
    global all_sprites, brick_group, iron_group, pool_group
    all_sprites = groups.get('all_sprites')
    brick_group = groups.get('brick_group')
    iron_group = groups.get('iron_group')
    pool_group = groups.get('pool_group')



'''
添加竖直砖墙
输入位置坐标，x:0-14,y:0-10
wall可以指定生成哪种墙，默认砖墙
砖墙：brick
铁墙：iron
'''
def add_ve_wall(x, y, long, wall='brick'):
    x_s = 35           #开始位置，既最外层墙块距离游戏外框的像素数量
    y_s = 45
    #判断创建那种墙
    if wall == 'brick':
        wall = landform.BrickWall.vertical_wall(x_s+68*x, y_s+68*y, long)
        brick_group.add(wall)
    elif wall == 'iron':
        wall = landform.IronWall.vertical_wall(x_s+68*x, y_s+68*y, long)
        iron_group.add(wall)
    elif wall == 'pool':
        wall = landform.Pool.vertical_wall(x_s+68*x, y_s+68*y, long)
        pool_group.add(wall)


    all_sprites.add(wall)
    return wall


'''
添加横向墙,输入x、y坐标，和墙的长度
'''
def add_ho_wall(x, y, long, wall='brick'):
    x_s = 36
    y_s = 45
    if wall == 'brick':
        wall = landform.BrickWall.horizontal_wall(x_s+68*x, y_s+68*y, long)
        brick_group.add(wall)
    elif wall == 'iron':
        wall = landform.IronWall.horizontal_wall(x_s+68*x, y_s+68*y, long)
        iron_group.add(wall)
    elif wall == 'pool':
        wall = landform.Pool.horizontal_wall(x_s+68*x, y_s+68*y, long)
        pool_group.add(wall)

    all_sprites.add(wall)
    return wall


'''
添加矩形砖墙
输入x、y坐标和横向、竖向长度，默认不填充，若需填充将solid改为True
'''
def add_re_wall(x, y, x_long, y_long, solid=False, wall='brick'):
    x_s = 36
    y_s = 45
    if wall == 'brick':
        wall = landform.BrickWall.rect_walls(x_s+68*x, y_s+68*y, x_long, y_long, solid)
        brick_group.add(wall)
    elif wall == 'iron':
        wall = landform.IronWall.rect_walls(x_s + 68 * x, y_s + 68 * y, x_long, y_long, solid)
        iron_group.add(wall)
    elif wall == 'pool':
        wall = landform.Pool.rect_walls(x_s+68*x, y_s+68*y, x_long, y_long, solid)
        pool_group.add(wall)

    all_sprites.add(wall)
    return wall




'''
地形刷新模块
'''
#第一关
def walls_fun_1():
    """关卡1"""

    # 外边框
    add_ho_wall(0, 0, 15)
    add_ho_wall(0, 10, 15)
    add_ve_wall(0, 1, 9)
    add_ve_wall(14, 1, 9)

    # ===== X形铁墙（四个斜线方向）=====
    # 左上-右下斜线（用单个铁墙块堆出斜线效果）
    add_ve_wall(3, 2, 1, wall='iron')
    add_ve_wall(5, 3, 1, wall='iron')
    add_ve_wall(7, 4, 1, wall='iron')
    add_ve_wall(9, 5, 1, wall='iron')
    add_ve_wall(11, 6, 1, wall='iron')

    # 右上-左下斜线
    add_ve_wall(11, 2, 1, wall='iron')
    add_ve_wall(9, 3, 1, wall='iron')
    add_ve_wall(7, 4, 1, wall='iron')
    add_ve_wall(5, 5, 1, wall='iron')
    add_ve_wall(3, 6, 1, wall='iron')

    # ===== 四个角落的水池 =====
    add_re_wall(1, 1, 2, 2, solid=True, wall='pool')
    add_re_wall(12, 1, 2, 2, solid=True, wall='pool')
    add_re_wall(1, 8, 2, 2, solid=True, wall='pool')
    add_re_wall(12, 8, 2, 2, solid=True, wall='pool')

    # ===== 中央砖墙堡垒 =====
    add_re_wall(6, 4, 3, 3, solid=True)

    # ===== 散落砖墙 =====
    add_ve_wall(4, 4, 2)
    add_ve_wall(10, 4, 2)
    add_ho_wall(4, 5, 2)
    add_ho_wall(9, 5, 2)

    # ===== 出生点（底部中央）=====
    add_ho_wall(6, 9, 1)
    add_ho_wall(8, 9, 1)

    return coordinate(x=7), coordinate(y=9)


#第二关
def walls_fun_2():
    # 1. 外围边框（砖墙）
    add_ho_wall(1, 0, 13, 'brick')  # 顶部横墙
    add_ho_wall(1, 10, 13, 'brick')  # 底部横墙
    add_ve_wall(0, 1, 9, 'brick')  # 左边竖墙
    add_ve_wall(14, 1, 9, 'brick')  # 右边竖墙

    # 2. 内部对称砖墙（掩体）
    add_ve_wall(2, 2, 1, 'brick')
    add_ve_wall(4, 2, 1, 'brick')
    add_ve_wall(10, 2, 1, 'brick')
    add_ve_wall(12, 2, 1, 'brick')

    add_ve_wall(2, 4, 1, 'brick')
    add_ve_wall(5, 4, 1, 'brick')
    add_ve_wall(9, 4, 1, 'brick')
    add_ve_wall(12, 4, 1, 'brick')

    add_ve_wall(2, 6, 1, 'brick')
    add_ve_wall(5, 6, 1, 'brick')
    add_ve_wall(9, 6, 1, 'brick')
    add_ve_wall(12, 6, 1, 'brick')

    add_ve_wall(2, 8, 1, 'brick')
    add_ve_wall(4, 8, 1, 'brick')
    add_ve_wall(10, 8, 1, 'brick')
    add_ve_wall(12, 8, 1, 'brick')

    add_ve_wall(3, 3, 1, 'brick')
    add_ve_wall(11, 3, 1, 'brick')
    add_ve_wall(3, 7, 1, 'brick')
    add_ve_wall(11, 7, 1, 'brick')

    # 3. 铁墙（不可破坏，核心防御）
    add_ve_wall(7, 2, 1, 'iron')
    add_ve_wall(7, 8, 1, 'iron')
    add_ve_wall(4, 5, 1, 'iron')
    add_ve_wall(7, 5, 1, 'iron')
    add_ve_wall(10, 5, 1, 'iron')

    # 4. 水池（不可通行，用矩形最方便！）
    add_re_wall(5, 3, 5, 1, True, 'pool')  # 上水池 5,3 → 8,3
    add_re_wall(5, 7, 5, 1, True, 'pool')  # 下水池 5,7 → 8,7

    return coordinate(x=7), coordinate(y=9)

#第三关《小D出的》
def walls_fun_3():
    """关卡14：八卦阵·改 - 矩形水池框 + 单入口"""

    # 外边框
    add_ho_wall(0, 0, 15)
    add_ho_wall(0, 10, 15)
    add_ve_wall(0, 1, 9)
    add_ve_wall(14, 1, 9)

    # ===== 外圈铁墙（八角形）=====
    add_ho_wall(3, 1, 9, wall='iron')  # 上
    add_ho_wall(3, 9, 9, wall='iron')  # 下
    add_ve_wall(1, 3, 2, wall='iron')  # 左上
    add_ve_wall(1, 6, 2, wall='iron')  # 左下
    add_ve_wall(13, 3, 2, wall='iron')  # 右上
    add_ve_wall(13, 6, 2, wall='iron')  # 右下

    #铁墙中间的砖墙
    add_ho_wall(1, 5, 2)    #左
    add_ho_wall(12, 5, 2)   #右

    # ===== 中圈：矩形水池框（用直线围成）=====
    # 上边水池（x=2 到 12，y=3）
    add_ho_wall(5, 3, 5, wall='pool')
    # 下边水池（左半）
    add_ho_wall(5, 6, 2, wall='pool')
    # 下边水池（右半）
    add_ho_wall(8, 6, 2, wall='pool')
    # 左边水池（y=3 到 7，x=2）
    add_re_wall(4, 3, 2, 4, wall='pool')
    # 右边水池（y=3 到 7，x=12）
    add_re_wall(9, 3, 2, 4, wall='pool')

    # ===== 核心区域（3x3空地）周围用砖墙围住 =====
    # 上方入口（唯一入口，用砖墙封住，可摧毁）
    add_ho_wall(6, 2, 3)  # 核心上方的砖墙

    # 左右两侧砖墙
    add_ve_wall(3, 4, 3)  # 核心左侧砖墙
    add_ve_wall(11, 4, 3)  # 核心右侧砖墙

    # 下方砖墙（封死）
    add_ho_wall(6, 7, 3)  # 核心下方砖墙

    # 四角入口（用砖墙封住）
    add_ve_wall(2, 2, 1)
    add_ve_wall(12, 2, 1)
    add_ve_wall(2, 8, 1)
    add_ve_wall(12, 8, 1)

    return coordinate(x=13), coordinate(y=1)

#第四关
def walls_fun_4():
    # 从上到下，从左到右排放
    add_ho_wall(0, 0, 15, wall='iron')  # 每个墙块长、宽都是68像素
    add_ve_wall(0, 1, 3, wall='iron')
    add_ve_wall(12, 1, 2, wall='iron')
    add_ve_wall(2, 2, 5, wall='iron')
    add_ho_wall(4, 2, 8, wall='iron')  # 上方中间铁墙
    add_ho_wall(0, 4, 2, wall='iron')
    add_ho_wall(5, 5, 10, wall='iron')
    add_ho_wall(3, 8, 4, wall='iron')
    add_ve_wall(12, 7, 3, wall='iron')
    add_ho_wall(13, 7, 2, wall='iron')
    add_ve_wall(2, 7, 3, wall='iron')
    add_ve_wall(9, 8, 3, wall='iron')

    return coordinate(x=3), coordinate(y=9)
#第五关
def walls_fun_5():
    """关卡9：环形废墟 - 不对称环形"""

    # 外边框
    add_ho_wall(0, 0, 15)
    add_ho_wall(0, 10, 15)
    add_ve_wall(0, 1, 9)
    add_ve_wall(14, 1, 9)

    # ===== 外圈铁墙（不完整环形）=====
    add_ho_wall(1, 1, 6, wall='iron')  # 上左铁墙
    add_ho_wall(8, 1, 6, wall='iron')  # 上右铁墙
    add_ve_wall(1, 2, 4, wall='iron')  # 左铁墙
    add_ve_wall(13, 2, 7, wall='iron')  # 右铁墙
    add_ho_wall(1, 9, 6, wall='iron')  # 下左铁墙
    # 右下角留出缺口

    # ===== 内圈水池（偏心）=====
    add_re_wall(5, 3, 2, 2, solid=True, wall='pool')
    add_re_wall(9, 6, 2, 3, solid=True, wall='pool')

    # ===== 中央砖墙堡垒（偏右）=====
    add_re_wall(8, 3, 3, 3, solid=True)
    add_ve_wall(7, 3, 2, wall='iron')

    # ===== 散落障碍=====
    add_ho_wall(3, 5, 2, wall='iron')
    add_ve_wall(5, 7, 2)
    add_ho_wall(11, 4, 2, wall='pool')

    # ===== 出生点（左下缺口）=====
    add_ho_wall(2, 9, 3)

    return coordinate(x=13), coordinate(y=9)

#第六关
def walls_fun_6():
    """关卡4：混合阵地 - 综合考验"""

    # 外边框
    add_ho_wall(0, 0, 15)
    add_ho_wall(0, 10, 15)
    add_ve_wall(0, 1, 9)
    add_ve_wall(14, 1, 9)

    # 外层铁墙
    add_re_wall(1, 1, 13, 1, solid=True, wall='iron')  # 上铁墙
    add_re_wall(1, 9, 5, 1, solid=True, wall='iron')  # 下铁墙
    add_re_wall(9, 9, 5, 1, solid=True, wall='iron')
    add_ve_wall(1, 2, 3, wall='iron')  # 左铁墙
    add_ve_wall(1, 6, 4, wall='iron')         #左侧中间砖墙
    #add_ve_wall(14, 7, 3, wall='iron')  # 右铁墙
    add_ve_wall(13, 6, 4, wall='iron')        #右侧中间砖墙
    # 形成铁墙围成的封闭区域，只有中间通道

    # 中间通道的水池
    add_ho_wall(3, 5, 3, wall='pool')
    add_ho_wall(9, 5, 3, wall='pool')
    #中间砖墙
    add_ho_wall(0, 5, 3)
    add_ho_wall(12, 5, 3)

    # 中间留下 3 格通道

    # 通道内的砖墙障碍
    add_ve_wall(6, 3, 3)
    add_ve_wall(8, 3, 3)

    # 铁墙堡垒（核心区域）
    add_re_wall(5, 2, 5, 2, solid=True, wall='iron')

    # 出生点
    add_ho_wall(4, 9, 7)

    return coordinate(x=7), coordinate(y=4)


#关卡映射
LEVEL_WALLS: Dict[int, Callable] = {
    1: walls_fun_1,
    2: walls_fun_2,
    3: walls_fun_3,
    4: walls_fun_4,
    5: walls_fun_5,
    6: walls_fun_6
}

#关卡加载函数，负责与主函数交互
def load_level_walls(level_num):
    if level_num in LEVEL_WALLS:
        #清空现有墙壁
        brick_group.empty()
        iron_group.empty()
        pool_group.empty()

        #创建新墙壁
        spawn_x, spawn_y = LEVEL_WALLS[level_num]()     #获取对应关卡的出生位置
        return spawn_x, spawn_y



