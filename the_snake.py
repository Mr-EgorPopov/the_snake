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


# Тут опишите все классы игры.
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
        self.position = (
            randint(0, 31) * GRID_SIZE,
            randint(0, 23) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Рандомайзер для позиционирования яблока"""
        self.position = (
            randint(0, 31) * GRID_SIZE,
            randint(0, 23) * GRID_SIZE
        )


class Stone(GameObject):
    """Создаем класс для булыжника"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR
        self.position = (
            randint(0, 31) * GRID_SIZE,
            randint(0, 23) * GRID_SIZE
        )

    def randomize_position(self):
        """Метод для рандомизации позиционирования булыжника"""
        self.position = (
            randint(0, 31) * GRID_SIZE,
            randint(0, 23) * GRID_SIZE
        )

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
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]

    def update_direction(self) -> None:
        """Обновление информации о направлении движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            return self.direction

    def get_head_position(self):
        """Получаем текущую позиция головы змеюки"""
        return self.positions[0]

    def move(self) -> None:
        """Заставляем змеюку двигаться в стиле диско"""
        self.get_head_position()
        d_x, d_y = self.direction
        d_x, d_y = d_x * GRID_SIZE, d_y * GRID_SIZE
        result = (
            self.get_head_position()[0] + d_x,
            self.get_head_position()[1] + d_y
        )
        self.positions.insert(0, result)
        # Проверка на выход за границы поля
        if self.get_head_position()[0] > 620:
            self.positions.pop(0)
            self.positions.insert(0, (0, self.get_head_position()[1]))

        elif self.get_head_position()[0] < 0:
            self.positions.pop(0)
            self.positions.insert(0, (620, self.get_head_position()[1]))

        elif self.get_head_position()[1] > 460:
            self.positions.pop(0)
            self.positions.insert(0, (self.get_head_position()[0], 0))

        elif self.get_head_position()[1] < 0:
            self.positions.pop(0)
            self.positions.insert(0, (self.get_head_position()[0], 460))
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

    def reset(self) -> None:
        """Возвращение змейки в дефолтное положение"""
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]


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
    # Инициализацияя pg
    pg.init()
    # Создание экземпляров класса
    apple = Apple()
    snake = Snake()
    stone = Stone()
    # Описание основной логики игры
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        snake.update_direction()
        # Проверка и пересоздание камня, если оно
        # создалось в яблоке
        if stone.position == apple.position:
            stone.randomize_position()
            # Проверка и пересоздание яблока, если оно
            # сьедено головой змейки и 'недопуск'
            # создания яблока в самой змейке
        elif apple.position == snake.positions[0]:
            apple.randomize_position()
            if apple.position == snake.positions[0]:
                apple.position = (randint(0, 31) * GRID_SIZE,
                                  randint(0, 23) * GRID_SIZE
                                  )
            snake.length += 1
        # Проверка на столкновение с телом
        elif snake.positions[0] in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        # Проверка на столкновение с камнем
        elif snake.positions[0] == stone.position:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        snake.draw()
        stone.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
