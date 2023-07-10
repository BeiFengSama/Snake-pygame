import sys
from tkinter import messagebox
import pygame as pg
import random


class Point:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col

    def copy(self):
        return Point(self.row, self.col)


# 参数初始化
W = 400
H = 500
ROW = 40
COL = 40
# 定义蛇
snakes = []
head_1 = Point(row=int(ROW/2), col=int(COL/2))
head_2 = Point(head_1.row + 1, head_1.col)
head_3 = Point(head_2.row + 1, head_2.col)
snakes.append(head_1)
snakes.append(head_2)
snakes.append(head_3)
score = 0
snake_color = (255, 255, 255)
is_sup_food = False
eat_num = 0
add_len = 1
# 定义食物


def draw_food():
    while True:
        food_pos = Point(random.randint(0, 39), random.randint(0, 39))
        is_collider = False
        for snake in snakes:
            if snake.row == food_pos.row and snake.col == food_pos.col:
                is_collider = True
                break
        if not is_collider:
            return food_pos


food = draw_food()
food_color = (255, 255, 255)

# 初始化
pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("贪吃蛇")
clock = pg.time.Clock()
dir = 'left'
button_width = 200
button_height = 50
button_color = (128, 128, 128)
button_text = "Start Game"
button_font = pg.font.Font(None, 36)
button_text_color = (255, 255, 255)

# 游戏状态
game_started = False


def draw_score():
    font = pg.font.Font(None, 30)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (30, 450))


def circle(pox, color):
    radius = 5
    pg.draw.circle(screen, color, (pox.col*10+5, pox.row*10+5), radius)


def draw_changing_circle(pox, color):
    radius = 6
    pg.draw.circle(screen, (255, 0, 0), (pox.col*10+5, pox.row*10+5), radius)


def rect(pox, color):
    left = pox.col * 10
    top = pox.row * 10
    pg.draw.rect(screen, color, (left, top, 10, 10))


# 函数：开始游戏逻辑
def start_game():
    # 开始游戏的逻辑代码
    # 这里只是简单地将game_started设置为True，你可以根据你的实际需求自定义这个函数

    global game_started
    game_started = True


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # 鼠标左键点击事件
            if not game_started:  # 如果游戏还未开始
                mouse_pos = pg.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):  # 检测按钮是否被点击
                    start_game()
    # 游戏逻辑部分

    screen.fill((0, 0, 0))  # 清空屏幕

    # 绘制按钮
    button_rect = pg.Rect((W - button_width) // 2, (H - button_height) // 2, button_width, button_height)
    pg.draw.rect(screen, button_color, button_rect)
    button_text_render = button_font.render(button_text, True, button_text_color)
    text_x = button_rect.centerx - button_text_render.get_width() // 2
    text_y = button_rect.centery - button_text_render.get_height() // 2
    screen.blit(button_text_render, (text_x, text_y))

    # 如果游戏已经开始，则绘制游戏的其他元素...
    if game_started:
        # 游戏已经开始，绘制游戏元素、逻辑等等...
        # 遍历事件
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == pg.K_w:
                if dir == 'left' or dir == 'right':
                    dir = 'up'
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                if dir == 'left' or dir == 'right':
                    dir = 'down'
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                if dir == 'up' or dir == 'down':
                    dir = 'left'
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                if dir == 'up' or dir == 'down':
                    dir = 'right'
        # 吃食物判断
        eat = False
        if snakes[0].row == food.row and snakes[0].col == food.col:
            if is_sup_food is True:
                add_len = 2
                score += 500
            else:
                add_len = 1
                score += 100
            eat_num += 1
            if eat_num == 4:
                is_sup_food = True
                eat_num = 0
                start_time = pg.time.get_ticks()
            else:
                is_sup_food = False
            food = draw_food()
            eat = True
        # 移动
        p_1 = Point(snakes[0].row, snakes[0].col)
        p_2 = Point(p_1.row, p_1.col)
        if dir == 'left':
            snakes[0].col -= 1
        elif dir == 'right':
            snakes[0].col += 1
        elif dir == 'up':
            snakes[0].row -= 1
        elif dir == 'down':
            snakes[0].row += 1
        for snake in snakes[1:]:
            p_1.row = snake.row
            p_1.col = snake.col
            snake.row = p_2.row
            snake.col = p_2.col
            p_2.row = p_1.row
            p_2.col = p_1.col
        if add_len > 0:
            snakes.append(p_1)
            add_len -= 1

        # 死亡判断
        if snakes[0].row < 0 or snakes[0].row >= 40 or snakes[0].col < 0 or snakes[0].col >= 40:
            response = messagebox.showinfo("游戏结束", "您的分数为："+str(score))
            if response == 'ok':
                break
        for snake in snakes[1:]:
            if snakes[0].row == snake.row and snakes[0].col == snake.col:
                response = messagebox.showinfo("游戏结束", "您的分数为："+str(score))
                if response == 'ok':
                    break
        # 页面渲染
        pg.draw.rect(screen, (0, 0, 0), (0, 0, 400, 400))
        pg.draw.rect(screen, (128, 128, 128), (0, 400, 400, 5))
        pg.draw.rect(screen, (128, 128, 128), (0, 0, 5, 600))
        pg.draw.rect(screen, (128, 128, 128), (0, 0, 400, 5))
        pg.draw.rect(screen, (128, 128, 128), (395, 0, 5, 600))
        pg.draw.rect(screen, (128, 128, 128), (0, 495, 400, 5))
        # 画食物
        if is_sup_food is True:
            current_time = pg.time.get_ticks()
            elapsed_time = current_time - start_time
            if elapsed_time > 5000:
                food = draw_food()
                is_sup_food = False
            draw_changing_circle(food, (255, 0, 0))
        else:
            circle(food, food_color)
        # 画蛇
        for snake in snakes:
            rect(snake, snake_color)
        draw_score()

    pg.display.update()
    clock.tick(10)
