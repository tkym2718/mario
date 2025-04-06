# cd game_env
# .\.venv\Scripts\activate
# cd ..\games\mine
# pyxel edit mario
# python mario.py
# cd ../../pyxel-tracker; & python editor.py
# cd ../games/mine

import pyxel

pyxel.init(256, 256, title="Mario", fps=60)   # 画面を生成
pyxel.load("mario.pyxres")                      # リソースファイルの読み込み
pyxel.playm(0, loop=True)                        # 音楽の再生

# 定数定義
GRAVITY = 15
INERTIA = 0.7
TRANSPARENT = 6

x = 32
y = 200
dx = 0
dy = 0
direction = 1
jump = 0
char_width = 16
char_height = 16
chk_point = [(0,0),(char_width,0),(0,char_height),(char_width,char_height)]

def is_collision(x, y):
    for xi,yi in chk_point:
        tile_x = (x + xi)//8
        tile_y = (y + yi)//8
        if 2 <= pyxel.tilemap(0).pget(tile_x,tile_y)[1] < 6:
            return True
    return False

def update_position(x, y, dx, dy, is_jump):
    # 横方向の移動
    lr = pyxel.sgn(dx) # 移動方向 (-1, 0, 1)
    steps_x = abs(dx) # 移動量
    while steps_x > 0:
        if is_collision(x + lr, y):
            dx = 0
            break
        x += lr
        steps_x -= 1

    # 縦方向の移動
    ud = pyxel.sgn(dy) # 移動方向 (-1, 0, 1)
    steps_y = abs(dy)
    while 0 < steps_y:
        if is_collision(x, y + ud):
            dy = 0
            if ud > 0:
                is_jump = False
            break
        y += ud
        steps_y -= 1
    else:
        if not is_collision(x, y + 1):
            is_jump = True
            dy = 0

    return x, y, dx, dy, is_jump

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_alive = True
        self.is_falling =False
        self.is_jumping = False

    def update(self):

        if pyxel.btn(pyxel.KEY_A):
            self.dx = max(self.dx -1, -3)
            self.direction = -1
        elif pyxel.btn(pyxel.KEY_D):
            self.dx = min(self.dx + 1, 3)
            self.direction = 1
        else:
            self.dx = int(self.dx * INERTIA) # 慣性

        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.dy = GRAVITY
            self.is_jumping = True

def update():
    global x,y,dx,dy,direction,jump

    # 操作判定
    if pyxel.btn(pyxel.KEY_A):
        if -3 < dx:
            dx -= 1
        direction = -1
    elif pyxel.btn(pyxel.KEY_D):
        if dx < 3:
            dx += 1
        direction = 1
    else:
        dx = int(dx * 0.7) # 慣性

    # 横方向の移動
    lr = pyxel.sgn(dx)
    steps = abs(dx)
    while 0 < steps :
        if is_collision(x + lr, y)  == True:
            dx = 0
            break
        x += lr
        steps -= 1

    # ジャンプと落下
    if jump == 0:
        if is_collision(x, y + 1) == False:
            jump = 2  # 床が無ければ落下
        if pyxel.btnp(pyxel.KEY_SPACE):
            dy = GRAVITY
            jump = 1   # ジャンプ開始
    else:
        dy -= 1
        if dy < 0:
            jump = 2    # 頂点で落下開始

    ud = pyxel.sgn(dy)
    steps = abs(dy)
    while 0 < steps :
        if is_collision(x, y - ud) == True:
            dy = 0
            if jump == 1:
                jump = 2   # 壁にぶつかって落下
            elif jump == 2:
                jump = 0   # 着地　落下終了
            break
        y -= ud
        steps -= 1
    return

def draw():
    pyxel.cls(0) # 画面クリア
    cam_x = max(0, x - pyxel.width // 2 + char_width // 2) # カメラのX座標
    pyxel.bltm(0, 0, 0, cam_x, 0, pyxel.width, pyxel.height, 0) # タイルマップを描画
    screen_x = pyxel.width // 2 - char_width // 2 # 画面の中央に描画
    pyxel.blt(screen_x, y, 0, 0, 96, direction * char_width, char_height, TRANSPARENT) # プレイヤーを描画
    pyxel.text(5, 5, f"({x},{y})", 7) # デバッグ用の座標表示
    return

pyxel.run(update,draw)
