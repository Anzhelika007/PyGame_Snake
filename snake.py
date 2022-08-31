import pygame
import sys
import random
import pygame_menu

pygame.init()

# фоновая заставка
bg_image = pygame.image.load('file.jpg')

frame_color_head = (230, 168, 14)
frame_color2 = (250, 240, 230)
frame_color3 = (204, 196, 188)
frame_color_margin = (230, 214, 165)
color_snake = (122, 73, 165)
color_food = (225, 0, 0)
# размер квадрата и их количество на поле
size_square = 20
count_square = 20
# margin
margin = 1
# место под заголовок
margin_header = 70

red = (255, 0, 0)

# установили размер окна который зависит от кол-ва квадратов на поле(изменяем: х=ширина блока*кол-во+рамка+margin*их кол-во; )
# высота у = высота хедера + 2 блока рамка +
# вынесли в отд перем - т.к. будем обращаться к размеру при отрисовке др элементов
size = [size_square * count_square + 2 * size_square + margin * count_square,
        size_square * count_square + 2 * size_square + margin * count_square + margin_header]
dis = pygame.display.set_mode((size))

# заголовок окна
pygame.display.set_caption('Snake')
# шрифты
courier = pygame.font.SysFont('courier', 36)
# таймер
timer = pygame.time.Clock()


class SnakeBlock:
    # класс нам будет передавать координаты в "хранилище"
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # проверка диапазона поля и нахождения змеи
    def is_inside(self):
        return 0 <= self.x < count_square and 0 <= self.y < count_square

    # мы не можем просто сравнить 2 экземпляра, поэтому исп метод
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def draw_field(color, row, column):
    # отрисовка всего
    # в цикле меняем значение х и y (первые значения переменных - рамка)
    pygame.draw.rect(dis, color, [size_square + column * size_square + margin * (column + 1),
                                  margin_header + size_square + row * size_square + margin * (row + 1), size_square,
                                  size_square])

# функция старта из pygame-menu
def start_the_game():
    # запуск по нажатию кнопки в меню

    def get_random_empty():
        x = random.randint(0, count_square - 1)
        y = random.randint(0, count_square - 1)
        empty_block = SnakeBlock(x, y)
        # проверим чтобы еда была не на змее
        while empty_block in snake_step:
            empty_block.x = random.randint(0, count_square - 1)
            empty_block.y = random.randint(0, count_square - 1)
        return empty_block

    # хранилице ходов змейки([x,y]....)
    snake_step = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    # еда
    foot = get_random_empty()
    # переменные движения змеи (buf - для отлова бага)
    d_row = buf_row = 0
    d_column = buf_column = 1
    total = 0
    speed = 1

    # сам цикл игры
    while True:
        # запускаем 'слушатель событий'
        for event in pygame.event.get():
            # если тип этого события "выход" > вызываем соответствующую функцию
            if event.type == pygame.QUIT:
                print('Exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # идем вправо/влево если до этого мы ходили вверх/вниз (вертикально)!!!
                if event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_column = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_column = 1
                # идем вверх/вниз если до этого мы ходили влево или вправо (горизонтально) не вниз/вверх!!!
                elif event.key == pygame.K_UP and d_column != 0:
                    buf_row = -1
                    buf_column = 0
                elif event.key == pygame.K_DOWN and d_column != 0:
                    buf_row = 1
                    buf_column = 0

        # применили цвет к фрейму
        dis.fill(frame_color_head)
        # отрисовали шапку
        pygame.draw.rect(dis, frame_color_margin, [0, 0, size[0], margin_header])
        # написали счет(обтекание текста, цвет)
        text_total = courier.render(f'Total: {total}', 0, color_food)
        dis.blit(text_total, (size_square, size_square))
        text_speed = courier.render(f'Speed: {speed}', 0, color_food)
        dis.blit(text_speed, (size_square + 230, size_square))

        # рисуем поле(квадраты), rect(где мы хотим рисовать, каким цветом, и координаты фигуры (левая верхняя точка и размер фигуры))
        for row in range(count_square):
            for column in range(count_square):
                if (row + column) % 2 == 0:
                    color = frame_color2
                else:
                    color = frame_color3
                # в цикле меняем значение х и y (первые значения переменных - рамка)
                draw_field(color, row, column)

        # при двежении добавляем один блок(новая голова) но последний удаляем
        head = snake_step[-1]
        if not head.is_inside():
            print('crash')
            break
            # pygame.quit()
            # sys.exit()

        # еда
        draw_field(color_food, foot.x, foot.y)

        # рисуем змею (проходимся по списку ходов, где класс нам создал вложенные кортежи ходов (х, у)
        for step in snake_step:
            draw_field(color_snake, step.x, step.y)

        # обновление экрана
        pygame.display.flip()

        # метод сравнения экземпляров - описан в классе
        if foot == head:
            total += 1
            # увеличим скорость при съеденых 5 яблоках
            speed = total // 5 + 1
            snake_step.append(foot)
            foot = get_random_empty()

        # двигаем змею
        d_row = buf_row
        d_column = buf_column

        # добавляем к змее новую голову
        new_head = SnakeBlock(head.x + d_row, head.y + d_column)
        # проверка на пересечение змеи самой себя
        if new_head in snake_step:
            print('crash')
            break

        snake_step.append(new_head)
        snake_step.pop(0)

        timer.tick(1 + speed)

# отрисовка модульного окна pygame-menu (через ctrl - можно выбрать тему)
menu = pygame_menu.Menu('', 300, 220, theme=pygame_menu.themes.THEME_DARK)
menu.add.text_input('Name : ', default='Player_1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

# цикл для отрисовки фоновой картинки из pygame-menu
while True:

    dis.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(dis)

    pygame.display.update()

pygame = quit()
quit()
