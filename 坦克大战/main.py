import pygame
import sprite
import random
import level

"""初始化部分"""
pygame.init()        #初始化pygame


#这是一个把像素换算成坐标的函数，
#直接输入坐标位置，函数会将像素换算到这个位置上
#默认输入是x，要计算竖向位置的话要加y=
def coordinate(x=None, y=None):
    n = None
    if x is not None:
        n = 35 + 68*x
    if y is not None:
        n = 45 + 68*y
    return n


WIDE = 768           #窗口高度y
LONG = 1024          #窗口长度x
'''窗口长度以像素为单位'''

screen = pygame.display.set_mode((LONG, WIDE))       #设定窗口
background = pygame.image.load('网格背景_pro.png').convert()


enemies_number = 12                             #敌方坦克总数
en_nu_now = 0                                  #场上敌方坦克数量


all_sprites = pygame.sprite.Group()           #建立存放所有精灵的精灵组
enemies_group = pygame.sprite.Group()         #建立存放敌人的精灵组
shell_group = pygame.sprite.Group()           #建立存放炮弹的精灵组
my_tank_group = pygame.sprite.Group()         #建立存放我方坦克的精灵组
text_group = pygame.sprite.Group()            #建立存放文字的精灵组
brick_group = pygame.sprite.Group()           #建立存放砖墙的精灵组
iron_group = pygame.sprite.Group()            #建立存放铁墙的精灵组
pool_group = pygame.sprite.Group()            #建立存放水池的精灵组


#关卡函数初始化，将主函数精灵组传入
level.init_level_groups({
    'all_sprites': all_sprites,
    'brick_group': brick_group,
    'iron_group': iron_group,
    'pool_group': pool_group
})



""" 
    添加一个炮弹
    可以作为回调函数使用
    目前作用于坏坦克函数里
"""
def add_shell(x, y, angle):

    """下方参数关联到sprite文件的Shell类；被用于add_bad_tank函数"""
    bad_shell = sprite.Shell(x, y, angle)
    bad_shell.add(all_sprites, shell_group)
    bad_shell.update()


'''
添加一个敌方坦克，并加入它的和总的精灵组
这里的x，y表示的是坦克坐标随机范围，既坦克会在这个范围内产生，而不是坦克的具体坐标
默认为屏幕范围

为避免坦克刷新在墙或其他坦克的位置，
函数通过设定临时坦克，使其通过墙体判定、坦克判定，
让符合条件（不产生任何碰撞）的坦克成为将要创建的坦克，
将temp_tank赋值给bad_tank
'''
def add_bad_tank(x1=0, y1=0, x2=LONG-20, y2=WIDE-20,
                 callback=add_shell,
                 walls=brick_group,
                 player_tank=None
                 ):                          #

    max_attempts = 100   #设置最多尝试次数，这么多次尝试无果后将判定为无合适位置

    for attempt in range(max_attempts):

        #生成一个随机位置
        x_ = random.randint(x1, x2)                    #创建两个随机数来定义敌方坦克的位置
        y_ = random.randint(y1, y2)

        #创建临时坦克
        """调整下方参数关联到sprite文件中BadTank类"""
        temp_tank = sprite.BadTank(x_, y_, callback, speed=4,
                                   collision_group=[walls,
                                                    enemies_group,
                                                    my_tank_group,
                                                    iron_group,
                                                    pool_group
                                                    ],                 #此处添加参与碰撞测试的墙组
                                   player_tank=player_tank
                                   )

        #检查是否撞墙
        wall_groups = [brick_group, iron_group, pool_group]
        collide_with_wall = any(pygame.sprite.spritecollide(temp_tank, group, False) for group in wall_groups)

        if collide_with_wall:
            print('撞到墙了，跳过')
            continue  #如果撞到了就跳过这个位置

        #检查是否撞到其他坦克
        collide_with_enemies = pygame.sprite.spritecollide(temp_tank, enemies_group, False)
        if collide_with_enemies:
            print('撞到别人了，跳过')
            continue

        #检查是否撞到了我方坦克
        collide_with_player = pygame.sprite.spritecollide(temp_tank, my_tank_group, False)
        if collide_with_player:
            print('撞到我了，跳过')
            continue


        #通过测试后：
        bad_tank_1 = temp_tank      #临时坦克转正
        bad_tank_1.add(all_sprites, enemies_group)                          #添加坦克到精灵组

        callback(bad_tank_1.rect.centerx, bad_tank_1.rect.centery, bad_tank_1.old_angle)      #使用回调函数创建炮弹

        return bad_tank_1           #返回的是敌方坦克
    print('无法找到合适的敌方坦克刷新点')
    return None


'''
game over函数，用于创建游戏结束后的窗口及操作逻辑
通过上下选择选项，回车或空格确认
可以更改遮罩大小、标题文字、背景颜色
'''
def game_over_fun(screen_=screen, back_color=(128, 28, 28, 5), text_color=(200, 20, 20),
                  long=LONG, wide=WIDE, text='GAME OVER'):
    selected = 0   #选择0  0重新开始；1选择关卡；2退出
    while True:
        #创建遮罩
        overlay = pygame.Surface((long, wide), pygame.SRCALPHA)   #遮罩大小（带透明的创建）
        overlay.set_alpha(128)          #遮罩透明度（0-255）
        overlay.fill(back_color)    #第四个数是透明度，好像是0-10
        screen_.blit(overlay, (0, 0))   #绘制这个遮罩

        #创建标题
        title_font = pygame.font.SysFont('华文楷体', 80)  #似乎是创建字体用的,74是大号，标题用
        title = title_font.render(text, True, text_color)     #设定文字属性
        title_rect = title.get_rect(center=(long//2, wide//2 - 200))
        screen_.blit(title, title_rect)   #绘制标题

        #创建选项
        option_font = pygame.font.SysFont('华文楷体', 48)  #用一个小点的字体

        #如果选择停留，高亮显示该选项
        if selected == 0:
            restart_text = option_font.render('>重新开始<', True, (255, 255, 0))
        else:
            restart_text = option_font.render('>重新开始<', True, (255, 255, 255))

        if selected == 1:
            level_text = option_font.render('>选择关卡<', True, (255, 255, 0))
        else:
            level_text = option_font.render('>选择关卡<', True, (255, 255, 255))

        if selected == 2:
            quit_text = option_font.render('>退出游戏<', True, (255, 255, 0))
        else:
            quit_text = option_font.render('>退出游戏<', True, (255, 255, 255))

        screen_.blit(restart_text, restart_text.get_rect(center=(long//2, wide//2 + 30)))
        screen_.blit(level_text, level_text.get_rect(center=(long//2, wide//2 + 100)))
        screen_.blit(quit_text, quit_text.get_rect(center=(long//2, wide//2 + 170)))
        pygame.display.flip()

        #处理输入
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                return 'quit'
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_w or event_.key == pygame.K_UP:
                    selected = (selected - 1) % 3
                elif event_.key == pygame.K_s or event_.key == pygame.K_DOWN:
                    selected = (selected + 1) % 3
                elif event_.key == pygame.K_SPACE or event_.key == pygame.K_RETURN:

                    if selected == 0:
                        return 'restart'
                    elif selected == 1:
                        return 'select_level'
                    else:
                        return 'quit'


'''
暂停页面函数
'''
def pause_menu_fun():
    """返回 'continue', 'restart', 'select_level', 'quit'"""
    selected = 0
    while True:
        # 半透明遮罩
        overlay = pygame.Surface((LONG, WIDE), pygame.SRCALPHA)
        overlay.set_alpha(128)
        overlay.fill((28, 28, 128, 5))
        screen.blit(overlay, (0, 0))

        # 标题
        title_font = pygame.font.SysFont('华文楷体', 60)
        title = title_font.render('游戏暂停', True, (255, 255, 0))
        title_rect = title.get_rect(center=(LONG // 2, WIDE // 2 - 150))
        screen.blit(title, title_rect)

        # 选项
        option_font = pygame.font.SysFont('华文楷体', 48)

        options = ['继续游戏', '重新开始', '选择关卡', '退出游戏']
        colors = [(255, 255, 0) if i == selected else (255, 255, 255) for i in range(4)]

        for i, (opt, color) in enumerate(zip(options, colors)):
            if i == selected:
                text = option_font.render(f'> {opt} <', True, color)
            else:
                text = option_font.render(f'  {opt}  ', True, color)
            y = WIDE // 2 - 30 + i * 70
            screen.blit(text, text.get_rect(center=(LONG // 2, y)))

        pygame.display.flip()

        # 输入处理
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                return 'quit'
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_w or event_.key == pygame.K_UP:
                    selected = (selected - 1) % 4
                elif event_.key == pygame.K_s or event_.key == pygame.K_DOWN:
                    selected = (selected + 1) % 4
                elif event_.key == pygame.K_SPACE or event_.key == pygame.K_RETURN:
                    if selected == 0:
                        return 'continue'
                    elif selected == 1:
                        return 'restart'
                    elif selected == 2:
                        return 'select_level'
                    else:
                        return 'quit'


'''
重置游戏状态函数
'''
def reset_game(level_num=1):
    global my_tank_life, my_tank, game_over, all_sprites,\
        my_tank_group, enemies_group, en_nu_now, enemies_number,\
        current_level


    current_level = level_num  #读取关卡信息
    my_tank_life = 3        #重置血量
    game_over = False       #重置游戏状态
    enemies_number = 12      #重置敌人数量
    en_nu_now = 0           #重置场上敌人数量


    #清空所有精灵组
    all_sprites.empty()
    enemies_group.empty()
    shell_group.empty()
    my_tank_group.empty()
    text_group.empty()
    brick_group.empty()
    iron_group.empty()
    pool_group.empty()

    #重建墙
    spawn_grid = level.load_level_walls(level_num)  #获取关卡的出生位置
    #重建我方坦克
    my_tank = sprite.MyTank(spawn_grid[0], spawn_grid[1], angle=0, speed=5)   #使用关卡的出生位置创造坦克
    my_tank.add(all_sprites, my_tank_group)

    #重置血量显示
    global health_text, enemy_count_text
    health_text = sprite.Text('■■■', color=(50, 230, 50), position=(950, 720), size=30, up_time=-1)
    health_text.add(all_sprites, text_group)
    #重置敌军数量显示
    enemy_count_text = sprite.Text(
        f'剩余敌军: {enemies_number}',
        color=(255, 255, 255),
        position=(100, 730),  # 左下角
        size=30,
        up_time=-1
    )
    enemy_count_text.add(all_sprites, text_group)


'''
选关页面函数
'''
def select_level_fun(screen_=screen, long=LONG, wide=WIDE):
    """选关画面，返回选择的关卡编号"""
    levels = [1, 2, 3, 4, 5, 6]  # 可用的关卡列表
    selected_index = 0

    while True:
        # 创建半透明背景
        overlay = pygame.Surface((long, wide), pygame.SRCALPHA)
        overlay.set_alpha(200)
        overlay.fill((30, 30, 30, 120))          #这个第四位数字好像有个关键帧的效果
        screen_.blit(overlay, (0, 0))

        # 标题
        title_font = pygame.font.SysFont('华文楷体', 60)
        title = title_font.render('选择关卡', True, (255, 255, 0))
        title_rect = title.get_rect(center=(long // 2, wide // 2 - 150))
        screen_.blit(title, title_rect)

        # 显示关卡选项（网格布局）
        option_font = pygame.font.SysFont('华文楷体', 40)
        cols = 3  # 每行3个
        start_x = long // 2 - 150
        start_y = wide // 2 - 50

        for i, level_ in enumerate(levels):
            #enumerate可以获取索引和值，比如[1,2,3]索引i=0,值level=1
            row = i // cols   #计算行号
            col = i % cols    #计算列号
            x = start_x + col * 150       #计算x坐标
            y = start_y + row * 80        #计算y坐标

            if selected_index == i:
                # 选中状态：黄色 + 方框
                level_text = option_font.render(f'第 {level_} 关', True, (255, 255, 0))
                pygame.draw.rect(screen_, (255, 255, 0),
                                 (x - 50, y - 20, 100, 45), 2)
            else:
                level_text = option_font.render(f'第 {level_} 关', True, (255, 255, 255))

            screen_.blit(level_text, level_text.get_rect(center=(x, y)))

        # 提示文字
        tip_font = pygame.font.SysFont('华文楷体', 24)
        tip = tip_font.render('方向键移动 | 空格/回车确认 | ESC返回', True, (200, 200, 200))
        tip_rect = tip.get_rect(center=(long // 2, wide - 50))
        screen_.blit(tip, tip_rect)

        pygame.display.flip()

        # 处理输入
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                return "quit"
            if event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_LEFT or event_.key == pygame.K_a:
                    selected_index = max(0, selected_index - 1)
                elif event_.key == pygame.K_RIGHT or event_.key == pygame.K_d:
                    selected_index = min(len(levels) - 1, selected_index + 1)
                elif event_.key == pygame.K_UP or event_.key == pygame.K_w:
                    if selected_index - cols >= 0:
                        selected_index -= cols
                elif event_.key == pygame.K_DOWN or event_.key == pygame.K_s:
                    if selected_index + cols < len(levels):
                        selected_index += cols
                elif event_.key == pygame.K_SPACE or event_.key == pygame.K_RETURN:
                    return levels[selected_index]
                elif event_.key == pygame.K_ESCAPE:        #esc退出
                    return "back"


#加载关卡
current_level = 1
init_spawn = level.load_level_walls(current_level)  #获取对应关卡的出生位置


#我方坦克相关属性
#我方坦克的刷新位置
G_T_X = init_spawn[0]      #375
G_T_Y = init_spawn[1]
direction = 0                                  #我方坦克和炮弹方向初始化

my_tank = sprite.MyTank(G_T_X, G_T_Y, angle=direction, speed=5)        #创建一个我方坦克
my_tank_life = 3                                           #我方坦克血量
my_tank.add(all_sprites, my_tank_group)                    #把这个坦克加入精灵组


#显示坦克血量，用方块表示
health_text = sprite.Text("■■■", color=(0, 255, 0), position=(950, 720), size=30, up_time=-1)
health_text.add(all_sprites, text_group)

#显示敌军数量
enemy_count_text = sprite.Text(
    f'剩余敌军: {enemies_number}',
    color=(255, 255, 255),
    position=(100, 730),  # 左下角
    size=30,
    up_time=-1
)
enemy_count_text.add(all_sprites, text_group)


"""游戏主循环"""
game_over = False
Bomb_run = False
running = True
while running:


    screen_0 = screen.blit(background, (0, 0))   #显示背景图片，放在前面是为了防止遮挡文本
    #screen_1 = screen.fill((255, 255, 255))      #显示纯色背景，需要修改渲染部分的背景名称，顺便注释掉前面读取背景的代码，
    current_time = pygame.time.get_ticks()       #获取游戏时间

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #点击关闭按钮退出循环
            running = False
            # 把单次事件（比如炮弹按一下打一下）放在循环里面


        # ESC 呼出菜单
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

            choice = pause_menu_fun()

            if choice == 'quit':
                running = False
            elif choice == 'restart':
                reset_game(current_level)
            elif choice == 'select_level':
                selected_level = select_level_fun()
                if selected_level == 'quit':
                    running = False
                if selected_level not in ('back', 'quit'):
                    reset_game(selected_level)
                    # 如果选择 'back' 或其他，什么都不做，继续游戏


        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #KEYDOWN表示按键按下的一瞬间；KEYUP表示按键抬起的一瞬间

            if my_tank.shoot():
                shell = sprite.Shell(my_tank.rect.centerx, my_tank.rect.centery, direction)
                all_sprites.add(shell)
                shell_group.add(shell)

    #把按键检测放在循环外面可以每一帧都移动，手感丝滑！
    keys = pygame.key.get_pressed()                #捕捉键盘的按下状态，进而实现一直按一直走
    old_x, old_y = my_tank.rect.x, my_tank.rect.y  #保存当前位置，用于碰撞回退

    if keys[pygame.K_w] and my_tank.rect.y > 0:
        direction = my_tank.rotate(0)                   #接收当前坦克朝向，发射炮弹时判定方向用
        my_tank.rect.y -= my_tank.speed

    elif keys[pygame.K_a] and my_tank.rect.x > 0:
        direction = my_tank.rotate(270)                 #接收当前坦克朝向，发射炮弹时判定方向用
        my_tank.rect.x -= my_tank.speed

    elif keys[pygame.K_s] and my_tank.rect.y < WIDE-60:
        direction = my_tank.rotate(180)                 #接收当前坦克朝向，发射炮弹时判定方向用
        my_tank.rect.y += my_tank.speed

    elif keys[pygame.K_d] and my_tank.rect.x < LONG-60:
        direction = my_tank.rotate(90)                  #接收当前坦克朝向，发射炮弹时判定方向用
        my_tank.rect.x += my_tank.speed

    #我方坦克与墙的碰撞检测
    if my_tank.collide_with_walls(brick_group) or \
            my_tank.collide_with_walls(iron_group) or \
            my_tank.collide_with_walls(pool_group):
        my_tank.rect.x, my_tank.rect.y = old_x, old_y


    #我方坦克与敌方坦克的碰撞
    if my_tank.collide_with_walls(enemies_group):
        my_tank.rect.x, my_tank.rect.y = old_x, old_y


    """敌方坦克刷新模块"""
    if enemies_number > en_nu_now and en_nu_now < 3:         #敌方坦克的刷新条件；前为剩余敌军总数，后为场上敌军总数
        bad_tank = add_bad_tank(player_tank=my_tank)                       #调用添加敌方坦克的函数

        if bad_tank is not None:
            en_nu_now += 1
            enemy_count_text.new_text(f'剩余敌人：{enemies_number}')
        else:                                #如果没找到合适位置刷新就吞掉这个敌人
            #print('有个敌人卡墙里寄了！')
            enemies_number -= 1
            temp_text = sprite.Text(f'有一个敌人掉出了世界~', color=(255, 100, 100), position=(200, 600), size=35,
                                    up_time=3)
            temp_text.add(all_sprites, text_group)
            enemy_count_text.new_text(f'剩余敌人：{enemies_number}')


    #如果敌方坦克全部消灭，就进入Game over页面
    if en_nu_now <= 0 and not game_over:

        #进入Game over页面
        game_over = True
        condition = game_over_fun(text='VICTORY!', back_color=(20, 153, 51, 3), text_color=(0, 255, 0))
        if condition == 'quit':                  #退出选项
            running = False
        elif condition == 'restart':             #重新开始选项
            reset_game(current_level)
        elif condition == 'select_level':        #选关选项
            selected_level = select_level_fun()
            if selected_level == 'quit':
                running = False
            if selected_level != 'back' and selected_level != 'quit':
                game_over = False
                reset_game(selected_level)


    """碰撞检测模块"""
    #代码用于炮弹与敌方坦克碰撞判定
    shell_bt_collision = pygame.sprite.groupcollide(shell_group, enemies_group, False, False)
    #这里不删除任何精灵，等炮弹无效时间判定之后再删除
    if shell_bt_collision:
        for shell_1 in shell_bt_collision:
            b_tank = shell_bt_collision[shell_1]
            #遍历击中列表获取炮弹键后再获取其值，这个值是所有被击中坦克的列表
            if current_time > shell_1.ignore_time:
                b_tank_1 = b_tank[0]
                shell_1.kill()
                b_tank_1.kill()
                enemies_number -= 1
                en_nu_now -= 1
                enemy_count_text.new_text(f'剩余敌人：{enemies_number}')    #更新敌人数量显示



    #代码用于炮弹与我方坦克碰撞判定
    shell_mt_collision = pygame.sprite.groupcollide(shell_group, my_tank_group, False, False)
    for shell_2 in shell_mt_collision:

        if current_time > shell_2.ignore_time:
            my_tank_life -= 1
            text_2 = sprite.Text('我方受击！', (240, 0, 0), (750, 385), 35, 2)
            text_2.add(all_sprites, text_group)
            shell_2.kill()
            # 更新坦克血量显示
            blocks = "■" * my_tank_life + "□" * (3 - my_tank_life)
            health_text.new_text(blocks)  #文字类更新方法


        if my_tank_life <= 0:
            choice = game_over_fun()  #调用Game over函数，绘制游戏结束页面

            if choice == 'restart':
                reset_game(current_level)       #重置游戏状态，加载当前关卡
            elif choice == 'select_level':
                selected_level = select_level_fun()
                if selected_level == 'quit':
                    running = False
                if selected_level != 'back' and selected_level != 'quit':
                    game_over = False
                    reset_game(selected_level)
            elif choice == 'quit':
                running = False


    #代码用于检测砖墙与炮弹碰撞
    shell_bw_collision = pygame.sprite.groupcollide(brick_group, shell_group, False, False)
    for shell_3 in shell_bw_collision:          #用子弹遍历碰撞列表，
        b_walls = shell_bw_collision[shell_3]   #这是这个子弹撞到的所有墙的列表

        b_walls_0 = b_walls[0]                  #取出碰到的第一个墙，删除它
        shell_3.kill()
        b_walls_0.kill()

    #检测铁墙与炮弹的碰撞
    #删除炮弹但不删除墙
    shell_iw_collision = pygame.sprite.groupcollide(iron_group, shell_group, False, True)



    """游戏渲染"""
    all_sprites.draw(screen)                        #绘制所有精灵组
    all_sprites.update()                            #更新所有精灵组
    pygame.display.update(screen_0)                #更新显示
    pygame.time.Clock().tick(30)                   #游戏时钟


