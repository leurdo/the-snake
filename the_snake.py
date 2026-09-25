from random import randint

import pygame

# алиасы для сложных типов
Position = tuple[int, int]
Color = tuple[int, int, int]


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Position = (0, -1)
DOWN: Position = (0, 1)
LEFT: Position = (-1, 0)
RIGHT: Position = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color: Color = BORDER_COLOR) -> None:
        self.position: Position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        )
        self.body_color: Color = body_color

    def draw(self) -> None:
        """Отрисовать игровой объект на экране."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко на игровом поле."""

    def __init__(self) -> None:
        super().__init__(APPLE_COLOR)

    def randomize_position(self) -> None:
        """Установить случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self) -> None:
        """Отрисовать яблоко"""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
        dx, dy = self.direction

        new_head_position: Position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self) -> None:
        """Изменить направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовать змейку"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(
            self.positions[0],
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect,
            )

    def reset(self) -> None:
        """Вернуть змейку и игровое поле в исходное состояние"""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object: Snake) -> None:
    """Обработка нажатий клавиш пользователем"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if (
                    event.key == pygame.K_UP
                    and game_object.direction != DOWN
            ):
                game_object.next_direction = UP

            elif (
                    event.key == pygame.K_DOWN
                    and game_object.direction != UP
            ):
                game_object.next_direction = DOWN

            elif (
                    event.key == pygame.K_LEFT
                    and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT

            elif (
                    event.key == pygame.K_RIGHT
                    and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры"""
    pygame.init()

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

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
