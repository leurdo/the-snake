from random import randint

import pygame as pg

# алиасы для сложных типов
Position = tuple[int, int]
Color = tuple[int, int, int]


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP: Position = (0, -1)
DOWN: Position = (0, 1)
LEFT: Position = (-1, 0)
RIGHT: Position = (1, 0)

# Сопроставление клавиш пользовательского ввода и направлений движения
DIRECTION_KEYS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Цвета объектов игры:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)
BORDER_COLOR: Color = (93, 216, 228)
APPLE_COLOR: Color = (255, 0, 0)
SNAKE_COLOR: Color = (0, 255, 0)
ERROR_COLOR: Color = (255, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс, устанавливающий общие характеристики игровых объектов"""

    def __init__(self, body_color: Color = ERROR_COLOR) -> None:
        self.position: Position = GRID_CENTER
        self.body_color: Color = body_color

    def draw_cell(
        self,
        position: Position,
        color: Color | None = None,
        with_border: bool = True
    ) -> None:
        """Отрисовать одну ячейку заданного цвета"""
        if color is None:
            color = self.body_color
        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE),
        )
        pg.draw.rect(screen, color, rect)
        if with_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Отрисовать игровой объект на экране."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён в дочернем классе.'
        )


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле."""

    def __init__(
        self,
        snake_positions: list[Position] = [GRID_CENTER]
    ) -> None:
        super().__init__(APPLE_COLOR)
        self.snake_positions = snake_positions

    def randomize_position(self) -> None:
        """Установить случайную позицию яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in self.snake_positions:
                break

    def draw(self) -> None:
        """Отрисовать яблоко"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self) -> None:
        super().__init__(SNAKE_COLOR)

        self.length: int = 1
        self.direction: Position = RIGHT
        self.next_direction: Position | None = None
        self.last: Position | None = None
        self.positions: list[Position] = [self.position]

    def get_head_position(self) -> Position:
        """Получить координаты головы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """Переместить змейку"""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_position: Position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head_position)
        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def update_direction(self) -> None:
        """Изменить направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовать змейку"""
        # Затирание последнего сегмента.
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, False)

        # Отрисовка хвоста змейки.
        self.draw_cell(self.positions[-1])

        # Отрисовка головы змейки.
        self.draw_cell(self.positions[0])

    def reset(self) -> None:
        """Вернуть змейку и игровое поле в исходное состояние"""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]


def handle_keys(game_object: Snake) -> None:
    """Обработка нажатий клавиш пользователем."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            game_object.next_direction = DIRECTION_KEYS.get(
                (game_object.direction, event.key),
                game_object.direction,
            )


def main() -> None:
    """Основной цикл игры"""
    pg.init()

    snake = Snake()
    apple = Apple()
    apple.randomize_position()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
