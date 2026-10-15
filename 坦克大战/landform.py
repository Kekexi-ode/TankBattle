"""地形模块 - 砖墙、铁墙、水池"""

import pygame

pygame.init()

# 常量定义
TILE_SIZE = 68  # 每个墙块的像素大小


class BaseWall(pygame.sprite.Sprite):
    """墙体基类，所有墙体继承此类"""

    # 子类覆写
    image_path = None

    def __init__(self, x, y):
        super().__init__()
        if self.image_path is None:
            raise NotImplementedError("子类应定义 image_path")
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    @classmethod
    def vertical_wall(cls, start_x, start_y, length):
        """创建一排竖直的墙"""
        walls = []
        for i in range(length):
            wall = cls(start_x, start_y + i * TILE_SIZE)
            walls.append(wall)
        return walls

    @classmethod
    def horizontal_wall(cls, start_x, start_y, length):
        """创建一排横向的墙"""
        walls = []
        for i in range(length):
            wall = cls(start_x + i * TILE_SIZE, start_y)
            walls.append(wall)
        return walls

    @classmethod
    def rect_walls(cls, x, y, x_length, y_length, solid=False):
        """创建矩形区域墙体（边框或实心）"""
        walls = []
        for i in range(x_length):
            for j in range(y_length):
                # 边框或实心填充
                if solid or i == 0 or i == x_length - 1 or j == 0 or j == y_length - 1:
                    wall = cls(x + i * TILE_SIZE, y + j * TILE_SIZE)
                    walls.append(wall)
        return walls


class BrickWall(BaseWall):
    """砖墙（可摧毁）"""
    image_path = '砖墙1.png'


class IronWall(BaseWall):
    """铁墙（不可摧毁/耐久高）"""
    image_path = '铁墙.png'


class Pool(BaseWall):
    """水池（不可通过）"""
    image_path = 'pool.png'