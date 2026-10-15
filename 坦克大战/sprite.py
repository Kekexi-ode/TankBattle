import pygame
import random                                 ##随机数

pygame.init()



#模板类，用于定义游戏元素的图像，位置,等信息，也引用了精灵组方法。
class Sprite:
    def __init__(self):
        self.image = None     #储存精灵图像
        self.rect = None      #定义精灵位置大小

        self.groups = []      #记录精灵属于哪个组

    def update(self, *args):          #*args 表示任意个参数
        """定义更新方法，需要子类自行定义"""
        pass


    def kill(self):
        """用于精灵自杀，可以将一个精灵从所有包含它的组里删掉"""
        for group in self.groups:         #遍历登记过自己的精灵名单
            group.remove(self)            #从名单中删除自己
        self.groups = []                  #清空登记名单


    def remove(self, *groups):
        """将自己从输入的组中删除"""
        for group in groups:              #同上
            group.remove(self)


    def add(self, *groups):
        """可以将自己添加到精灵组"""
        for group in groups:              #遍历每个输入的组
            group.add(self)               #在每个组里添加自己

    def alive(self):
        """检查精灵是否还活着（至少在一个组里）
           解释起来有点复杂，精灵被kill后不会直接消失，
           为了节省算力，在检验碰撞时只检验活着的精灵。"""
        return len(self.groups) > 0
        #返回布尔值，True表示活着，False表示死了（但还没有消失！）



"""
   定义我方坦克类
   坦克的基本属性，运动方式等都在这里定义
   炮弹的发射冷却也在这里
"""
class MyTank(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, speed=8):      #x, y为坐标 ,angle为角度，控制坦克朝向
        super().__init__()   #调用模板定义方法，使该类继承模板类
        self.my_tank_image = pygame.image.load('MyTank.png').convert_alpha()
        #convert_alpha是一个优化，好像可以让图片加载更快，还能保留透明度，需要时详细研究吧
        self.image = self.my_tank_image                   #定义坦克图像
        self.rect = self.image.get_rect(center=(x, y))    #定义坦克位置
        self.collision_scale = 0.9       #坦克碰撞箱面积


        self.angle = angle                 #控制坦克方向
        self.speed = speed                 #控制坦克速度

        self.cooldown = 0                # 冷却计数器，用于发射炮弹后的冷却
        self.cooldown_time = 30          # 冷却时间  15大概0.5s，30大概1s30, 50大概2s， 80大概3s

    def rotate(self, angle):               #用于旋转坦克
        self.angle = angle                 #设定角度（防止失真累计？）
        self.image = pygame.transform.rotate(self.my_tank_image, -self.angle)
        #让picture_image逆时针旋转angle度，然后赋值给image，py默认顺时针，所以加负号
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        #记录中心点坐标，防止旋转后图片偏移，.center用于获取中心点坐标

        return self.angle

    def update(self):
        if self.cooldown > 0:                     #进行倒计时
            self.cooldown -= 1


    def shoot(self):                              #用于判定冷却是否结束，是否符合发射条件
        #当冷却时间未结束时不能发射
        if self.cooldown > 0:
            return False

        else:
            self.cooldown = self.cooldown_time  # 重置冷却时间
            return True


    '''坦克碰撞检查方法，测试阶段'''

    def get_collision_rect(self):              #获取用于碰撞检测的矩形

        #把self的碰撞箱体积乘进去，缩小碰撞箱
        width = self.rect.width * self.collision_scale
        height = self.rect.height * self.collision_scale
        #先在左上角放一个碰撞箱
        collision_rect = pygame.Rect(0, 0, width, height)
        #再把碰撞箱放到坦克的坐标上
        collision_rect.center = self.rect.center
        return collision_rect


    def collide_with_walls(self, walls_group):      #与墙的碰撞检测，返回布尔值
        old_pos = self.rect.center                    #保存当前位置

        collision_rect = self.get_collision_rect()    #获取碰撞箱

        for wall in walls_group:                        #检查是否与墙碰撞
            if collision_rect.colliderect(wall.rect):
                self.rect.center = old_pos
                return True
        return False



"""
定义炮弹类
设定了炮弹的速度，方向等基本属性，不过位置、方向这些需要在游戏循环里输入一下
这里还定义了炮弹的自杀位置
以及炮弹飞行的自我刷新
发射冷却请移步MyTank类
"""
class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, angle=0, speed=10, killx=1110, killy=780, ignore_time=310):
        super().__init__()

        self.shell_image = pygame.image.load('炮弹1.png').convert()
        self.image = self.shell_image                    #定义炮弹图像
        self.rect = self.image.get_rect(center=(x, y))   #
        self.x = x
        self.y = y
        self.speed = speed                               #控制炮弹速度
        self.angle = angle                               #炮弹方向
        self.killx = killx                               #设定炮弹的自杀阈值X
        self.killy = killy                               #设定炮弹的自杀阈值Y
        self.ignore_time = ignore_time + pygame.time.get_ticks()       #炮弹的无效时间，防止炮弹刚发射就发生碰撞
        #无效时间为炮弹的无效时间加上游戏时钟，判定时用游戏时钟直接比较，
        #如果游戏时钟大于这个量，那碰撞就成立


    def update(self):                             #自动更新模块


        if self.angle == 0:
            self.rect.y -= self.speed
        if self.angle == 90:
            self.rect.x += self.speed
        if self.angle == 180:
            self.rect.y += self.speed
        if self.angle == 270:
            self.rect.x -= self.speed

        if self.rect.x > self.killx or self.rect.y > self.killy:
            self.kill()                         #判定炮弹是否超出屏幕，如果超出就自杀





"""
    坏坦克类
    定义敌方坦克几乎所有行为
    包括速度、方向、炮弹发射之类
"""
class BadTank(pygame.sprite.Sprite):
    # x, y为坐标 ,speed为速度，控制坦克速度
    def __init__(self, x, y, callback=None, speed=8, collision_group=None, player_tank=None):
        super().__init__()  # 调用模板定义方法，使该类继承模板类
        self.my_tank_image = pygame.image.load('BadTank.png').convert_alpha()
        # convert_alpha是一个优化，好像可以让图片加载更快，还能保留透明度，需要时详细研究吧
        self.image = self.my_tank_image  # 定义坦克图像
        self.rect = self.image.get_rect(center=(x, y))  # 定义坦克位置
        self.collision_scale = 0.9                      #碰撞箱体积
        self.collision_group = collision_group if collision_group else []
        #所有用于碰撞检测的组,三元运算符，表示如果有collision传入,self就用这个组，否则就是空列表，用于处理None情况
        #参数传入时应写为：collision_group = [a_group, b_group, ...]

        self.callback = callback                        #留一个回调函数的空位，以便添加功能

        anglr_list = [0, 90, 180, 270, 404]             #坦克的方向数组, 404表示停止

        self.cooldown_time = random.randint(50, 120)       #设定敌方坦克发射炮弹的间隔
        self.cooldown = 0                                #冷却计数器，用于发射炮弹后的冷却
        self.move_time = 0                               #移动计数器，用于坦克移动时间重置


        self.angle = random.choice(anglr_list)   #从坦克方向数组里随机一个作为坦克方向
        self.move = random.randint(15, 80)        #设定敌方坦克移动时间，最短0.5s，最长3s
        self.speed = speed                         #控制坦克速度
        if self.angle != 404:
            self.old_angle = self.angle               #保存有效方向，用于发射炮弹
        else:
            self.old_angle = 180
        #random_time_shoot = self.cooldown_time      #冷却时间

        #以下定义用于追逐AI
        self.player_tank = player_tank      #玩家坦克引用
        self.ai_update_timer = 0
        self.ai_update_interval = 60      #每60帧重新计算一次方向

        #初始化结束时把图片旋转到对应角度，
        if self.angle != 404:
            self.image = pygame.transform.rotate(self.my_tank_image, -self.angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
            self.old_angle = self.angle


    """旋转敌方坦克"""
    def change_angle(self):                             #用于修改方向，直接修改内部，没有返回
        angle_list = [0, 90, 180, 270, 404]             #坦克的方向数组, 404表示停止
        self.angle = random.choice(angle_list)        #从坦克方向数组里随机一个作为坦克方向


        if self.angle != 404:
            self.image = pygame.transform.rotate(self.my_tank_image, -self.angle)
            # 让picture_image逆时针旋转angle度，然后赋值给image，py默认顺时针，所以加负号
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
            # 记录中心点坐标，防止旋转后图片偏移，.center用于获取中心点坐标
            self.old_angle = self.angle


        return self.angle                               #返回旋转后的方向

    """碰撞箱获取方法"""
    def get_collision_rect(self):                  #更新碰撞箱

        #乘入碰撞箱体积
        width = int(self.rect.width * self.collision_scale)
        height = int(self.rect.height * self.collision_scale)

        #放置碰撞箱
        collision_rect = pygame.Rect(0, 0, width, height)
        #将碰撞箱移动到坦克位置
        collision_rect.center = self.rect.center
        return collision_rect


    """碰撞检测方法"""
    def collide_with_walls(self, collision_group):      #与精灵的碰撞检测，返回布尔值

        collision_rect = self.get_collision_rect()  #获取碰撞箱
        for group in collision_group:
            if isinstance(group, pygame.sprite.Group):
                #isinstance函数用于判断group是否属于后面那个的类或它的子类
                #比如判断group是对象还是精灵组，以便针对不同情况分别操作，
                #这里只写了group是精灵组时的操作
                for sprite in group:
                    if sprite == self:
                        continue
                    if hasattr(sprite, 'rect') and collision_rect.colliderect(sprite.rect):  #在输入的列表中检测碰撞
                        #hasattr函数用于判断sprite对象是否有‘rect’属性，返回布尔值
                        #这一句的意思是判断这个对象有rect属性再进行碰撞，否则短路and跳过碰撞

                        return True                          #并且返回True
        return False

    #追逐AI方法
    def ai_chase(self):
        if self.player_tank is None:
            return

            # 计算到玩家的距离
        dx = self.player_tank.rect.centerx - self.rect.centerx
        dy = self.player_tank.rect.centery - self.rect.centery

        # 决定移动方向
        if abs(dx) > abs(dy):
            # 水平方向移动
            if dx > 0:
                self.angle = 90  # 向右
            else:
                self.angle = 270  # 向左
        else:
            # 垂直方向移动
            if dy > 0:
                self.angle = 180  # 向下
            else:
                self.angle = 0  # 向上

            # 更新图片旋转
        if self.angle != 404:
            self.image = pygame.transform.rotate(self.my_tank_image, -self.angle)
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
            self.old_angle = self.angle


    def update(self):

        self.move_time += 1

        old_x, old_y = self.rect.x, self.rect.y       ##保存旧位置，用于碰撞时回退
        #old_rect = self.rect

        if self.angle == 0 and self.rect.y > 20:                        ##向上
            self.rect.y -= self.speed

        elif self.angle == 90 and self.rect.x < 964:                       ##向右
            self.rect.x += self.speed

        elif self.angle == 180 and self.rect.y < 708:                      ##向下
            self.rect.y += self.speed

        elif self.angle == 270 and self.rect.x > 20:                      ##向左
            self.rect.x -= self.speed

        elif self.angle == 404:                      ##停止

            pass

        #随机移动部分
        if self.move_time >= self.move:
            if random.randint(0, 100) < 30:         #70%概率随机移动，为了避免和AI移动冲突
                self.angle = self.change_angle()                       #调用上面的函数，改变前进方向
            self.move_time = 0                        #重置移动时间
            self.move = random.randint(15, 80)    #设定敌方坦克移动时间，最短0.5s，最长3s

        # AI决策部分
        self.ai_update_timer += 1
        if self.ai_update_timer >= self.ai_update_interval:
            self.ai_update_timer = 0
            self.ai_chase()  # 调用 AI



        #与各个精灵的碰撞检测
        if self.collide_with_walls(self.collision_group):
            self.rect.x, self.rect.y = old_x, old_y

        if self.cooldown < self.cooldown_time:
            self.cooldown += 1

        """炮弹发射触发"""
        if self.cooldown >= self.cooldown_time:

            """下方参数用于主文件夹’add_shell‘（创建炮弹）函数，后被用于创建敌方坦克函数"""
            self.callback(self.rect.centerx, self.rect.centery, self.old_angle)    #发射一个炮弹
            """bug : 当方向为404（停止）时，炮弹无法识别方向"""

            self.cooldown = 0                       ##重置冷却时间




"""文字显示类"""
class Text(pygame.sprite.Sprite):
    def __init__(self, text, color=(255, 255, 255),
                 position=(550, 385), size=8, up_time=3):
        super().__init__()
        self.text = text
        self.color = color
        self.position = position      #这是表示文字位置的元组（x，y），方便确定中心位置
        self.font = pygame.font.SysFont('华文楷体', size)     #使用默认字体，size为文字大小
        self.image = None             #文字没有图片属性，不过需要初始化
        self.rect = None
        self.surface = None
        self.start_time = pygame.time.get_ticks()      #获取游戏时钟作为文字显示的开始时间
        self.up_time = up_time * 1000                  #设定文字显示时间，-1永久显示
        self.update_time = pygame.time.get_ticks() + self.up_time
        self.display = True                           #显示是否成立
        self.update()


    """更新文字表面"""
    def update(self):

        if not self.display:
            self.image = None  #不显示时图片属性None
            return             #这个返回用于提前退出函数
        else:
            self.surface = self.font.render(self.text, True, self.color)
            # 使用self.font字体创建一个self.surface表面，
            # render用于将所给参数绘制为表面，True表示启动抗锯齿
            self.image = self.surface              #把render绘制的表面赋值给self image
            self.rect = self.surface.get_rect()    #把位置给rect，这两个变量来自模板类，必须的有
            self.rect.center = self.position


        if self.up_time > 0 and self.display:
            elapsed_time = pygame.time.get_ticks() - self.update_time
            if elapsed_time > self.up_time:
                self.display = False
                self.kill()                         #显示时间结束后杀死自己，
        # 更新时间加载



    """更新文本内容"""
    def new_text(self, new_text):
        self.text = new_text
        self.update()      #更新表面


    """更新文本颜色"""
    def new_color(self, new_color):
        self.color = new_color
        self.update()


    """更新文本位置位置"""
    def new_position(self, new_position):
        self.position = new_position
        self.update()


    """绘制文本"""
    def draw(self, surface):
        if self.display:
            text_rect = self.surface.get_rect()              #获取文字表面矩形位置
            text_rect.center = self.position           #获取位置元组的中心位置
            surface.blit(self.surface, text_rect)          #将surface绘制到表面rect位置
            self.update()


