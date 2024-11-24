from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Начальная клетка по оси х и у
zero_cell = 0

# Крайняя клетка по оси х
x_cell = 31

# Крайняя клетка по оси у
y_cell = 23

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет булыжника
STONE_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Описание родительского класса"""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Метод для отрисовки объекта на экран."""
        pass


class Apple(GameObject):
    """Описание класса для яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, *args):
        """Рандомайзер для позиционирования яблока"""
        while True:
            new_position = (
                randint(zero_cell, x_cell) * GRID_SIZE,
                randint(zero_cell, y_cell) * GRID_SIZE
            )

            if new_position != args:
                self.position = new_position
                break


class Stone(GameObject):
    """Создаем класс для булыжника"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR
        self.randomize_position()

    def randomize_position(self, *args):
        """Метод для рандомизации позиционирования булыжника"""
        while True:
            new_position = (
                randint(zero_cell, x_cell) * GRID_SIZE,
                randint(zero_cell, y_cell) * GRID_SIZE
            )

            if new_position != args:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка булыжника"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание класса для змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()
        self.direction = RIGHT

    def update_direction(self, next_direction) -> None:
        """Обновление информации о направлении движения"""
        if next_direction is not None:
            self.direction = next_direction
            return self.direction

    def get_head_position(self):
        """Получаем текущую позиция головы змеюки"""
        return self.positions[0]

    def move(self) -> None:
        """Заставляем змеюку двигаться в стиле диско"""
        self.position_of_head = self.get_head_position()
        d_x, d_y = self.direction
        d_x, d_y = d_x * GRID_SIZE, d_y * GRID_SIZE
        result = (
            self.position_of_head[0] + d_x,
            self.position_of_head[1] + d_y
        )
        self.positions.insert(0, result)
        # Проверка на выход за границы поля
        self.new_position = (
            (self.get_head_position()[0] + SCREEN_WIDTH) % SCREEN_WIDTH,
            (self.get_head_position()[1] + SCREEN_HEIGHT) % SCREEN_HEIGHT
        )
        self.positions.pop(0)
        self.positions.insert(0, self.new_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Метод для отрисовки змейки"""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Возвращение змейки в дефолтное положение"""
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [self.position]
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Метод для считывания нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры"""
    pg.init()
    apple = Apple()
    snake = Snake()
    stone = Stone()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.update_direction(snake.next_direction)
        occupied_for_apple = [stone.position, snake.positions]
        occupied_for_stone = [snake.positions, apple.position]
        if stone.position == apple.position:
            stone.randomize_position(occupied_for_stone)
        elif apple.position == snake.get_head_position():
            apple.randomize_position(occupied_for_apple)
            if apple.position == snake.get_head_position():
                apple.position = (randint(zero_cell, x_cell) * GRID_SIZE,
                                  randint(zero_cell, y_cell) * GRID_SIZE
                                  )
            snake.length += 1
        elif snake.positions[0] in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        elif snake.position_of_head == stone.position:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        snake.draw()
        stone.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
