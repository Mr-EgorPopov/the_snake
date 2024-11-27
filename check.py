from random import choice, randint
import pygame as pg

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
STONE_COLOR = (128, 128, 128)
SNAKE_COLOR = (0, 255, 0)
SPEED = 7

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

class GameObject:
    def __init__(self, body_color=APPLE_COLOR):
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        raise NotImplementedError('Метод должен быть реализован в дочерних классах')

class Apple(GameObject):
    def __init__(self, taken_positions=None):
        super().__init__(APPLE_COLOR)
        self.randomize_position(taken_positions)

    def draw(self):
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, taken_positions):
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if taken_positions is None or self.position not in taken_positions:
                break

class Stone(GameObject):
    def __init__(self, taken_positions=None):
        super().__init__(STONE_COLOR)
        self.randomize_position(taken_positions)

    def randomize_position(self, taken_positions):
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if taken_positions is None or self.position not in taken_positions:
                break

    def draw(self):
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [SCREEN_CENTER]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        d_x, d_y = self.direction
        d_x *= GRID_SIZE
        d_y *= GRID_SIZE
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + d_x) % SCREEN_WIDTH
        new_head_y = (head_y + d_y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [SCREEN_CENTER]

def handle_keys(snake):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

def main():
    pg.init()
    snake = Snake()
    apple = Apple([])
    stone = Stone([*snake.positions, apple.position])
    
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == stone.position:
            snake.reset()
            apple.randomize_position([*snake.positions])
            stone.randomize_position([*snake.positions, apple.position])
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif apple.position == snake.get_head_position():
            apple.randomize_position([*snake.positions])
            snake.length += 1
            
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position([*snake.positions])
            stone.randomize_position([*snake.positions, apple.position])
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        stone.draw()
        snake.draw()
        pg.display.update()

if __name__ == '__main__':
    main()
