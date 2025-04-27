class Sprite:
    def __init__(self, sprite_id, shape):
        self.sprite_id = sprite_id
        self.shape = shape  # 16x16 pixels
        self.row = 0
        self.col = 0

class SpriteManager:
    def __init__(self):
        self.sprites = {}

    def set_sprite(self, level, sprite_id):
        self.sprites[level] = Sprite(sprite_id, [[0]*16 for _ in range(16)])

    def move_sprite(self, level, row, col):
        if level in self.sprites:
            self.sprites[level].row = row
            self.sprites[level].col = col

    def detect_collision(self, level1, level2):
        # (bounding box collision)
        pass
