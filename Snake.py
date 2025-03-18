import random
import pygame_menu
import pygame
import sys

pygame.init()
bg_image = pygame.image.load("public/snake.jpeg")
APPLE_COLOR = (255, 0, 0)
COLOR = (78, 56, 231)
WHITE = [255, 255, 255]
YELLOW = [255, 255, 0]
SIZE_BLOCK = 30
COUNT_BLOCKS = 21
BORDER = 1
SNAKE_COLOR = [0, 102, 0]

size = [500, 600]  # размер окна
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")


def draw_block(color, rows, colums):
    pygame.draw.rect(screen, color, [18 + colums * COUNT_BLOCKS + BORDER * (colums + 1),
                                     100 + rows * COUNT_BLOCKS + BORDER * (rows + 1), COUNT_BLOCKS,
                                     COUNT_BLOCKS])  # вводим 4 координаты 1- осьХ, 2- У, длину и ширину квадрата


class Snake_Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS  # проверка на нахождении змейки в поле

    def __eq__(self, other):
        return isinstance(other, Snake_Block) and (self.x == other.x and self.y == other.y)


def start_the_game():
    fps = 2
    total = 0

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = Snake_Block(x, y)
        while empty_block in snake_block:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_block = [Snake_Block(11, 9), Snake_Block(11, 10), Snake_Block(11, 11)]
    apple = get_random_empty_block()
    d_row = 0
    d_col = 1

    courier = pygame.font.SysFont("courier", 36)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():  # обработка всех нажатий клавиш и мышка
            if event.type == pygame.QUIT:  # нажатие крестика приостанавливает работу
                print("exit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and d_col != 0:
                    d_row = -1
                    d_col = 0

                if event.key == pygame.K_s and d_col != 0:
                    d_row = 1
                    d_col = 0

                if event.key == pygame.K_a and d_row != 0:
                    d_row = 0
                    d_col = -1

                if event.key == pygame.K_d and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(COLOR)
        pygame.draw.rect(screen, COLOR, [0, 0, size[0], BORDER])

        total_text = courier.render(f"total: {total}", 0, WHITE)
        fps_text = courier.render(f"FPS: {round(fps, 2)}", 0, WHITE)
        screen.blit(total_text, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(fps_text, (SIZE_BLOCK + 250, SIZE_BLOCK))

        for rows in range(COUNT_BLOCKS):
            for colums in range(COUNT_BLOCKS):
                if (rows + colums) % 2 == 0:
                    color = YELLOW
                else:
                    color = WHITE
                draw_block(color, rows, colums)
        head = snake_block[-1]
        if not head.is_inside():
            print("Game Over")
            break

        draw_block(APPLE_COLOR, apple.x, apple.y)
        for block in snake_block:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            fps += total // 10 + 0.2
            snake_block.append(apple)
            apple = get_random_empty_block()

        new_head = Snake_Block(head.x + d_row, head.y + d_col)

        if new_head in snake_block:  # проверка на столкновение самой с собой
            print("your crash yourself")
            break

        snake_block.append(new_head)
        snake_block.pop(0)

        pygame.display.flip()  # заливка фона
        clock.tick(fps)
    # clock = pygame.time.Clock


# surface = pygame.display.set_mode((600, 400))


menu = pygame_menu.Menu('Welcome', 300, 400,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='Player 1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

#menu.mainloop(screen)

while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
