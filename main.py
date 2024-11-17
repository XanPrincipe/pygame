import pygame
from pygame import KEYDOWN, KEYUP, MOUSEBUTTONUP, MOUSEBUTTONDOWN

clock = pygame.time.Clock()     # Создаем переменную для задержки анимации
pygame.init()   # Запуск программы, используется всегда как например в tkinter win = Tk()
screen = pygame.display.set_mode((1280, 720))    # Метод для указания размеров экрана(в скобочках указывется кортеж)
pygame.display.set_caption("DND")   # Задаем название для игры
icon = pygame.image.load("images/icon.png").convert_alpha()    # Создаем переменную для картинки
pygame.display.set_icon(icon)       # Загружаем иконку для приложения


# Подкючаем задник и все анимации
bg = pygame.image.load("images/Game_Background.png").convert_alpha()
walk_left = [
    pygame.image.load("images/player_left/left1.png").convert_alpha(),
    pygame.image.load("images/player_left/left2.png").convert_alpha(),
    pygame.image.load("images/player_left/left3.png").convert_alpha(),
    pygame.image.load("images/player_left/left4.png").convert_alpha(),
]

walk_right = [
    pygame.image.load("images/player_right/right1.png").convert_alpha(),
    pygame.image.load("images/player_right/right2.png").convert_alpha(),
    pygame.image.load("images/player_right/right3.png").convert_alpha(),
    pygame.image.load("images/player_right/right4.png").convert_alpha(),
]

lose_bg = pygame.image.load("images/gameover.jpg").convert()

# Добавляем врага
enemy = pygame.image.load("images/enemy/enemy.png").convert_alpha() # Для png всегда писать convert_alpha, а для всех других можно просто convert
# Добавляем патрон
bullet = pygame.image.load("images/bullet/bullet.png").convert_alpha()
bullets = []
# Добавляем список с врагами
enemy_list_in_game = []
# Создаем счетчик анимаций
player_anim_count = 0
#

# Создаем переменную для дальнейшего движения заднего фона
bgx = 0
bg_lose_x = 0

player_speed = 12    # Скорость персонажа
player_x = 150      # Координата персонажа по x
player_y = 565      # Координата персонажа по y

is_jump = False
jump_height = 7     # Высота прыжка


# Подключаем звук для задника
# bg_sound = pygame.mixer.Sound("sound/bg_snd.mp3")
# bg_sound.play(-1)   # Бесконечное проигрывание
# Добавляем таймер появления монстров на экране
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2000)

ammo = 5

# Подключаем шрифт и задаем параметры текста
label = pygame.font.Font("fonts/SourGummy-VariableFont_wdth,wght.ttf", 40)
lose_label = label.render("You Lost", False,(193,196,199))
label_rect = lose_label.get_rect(center=(640, 360))
restart_label = label.render("Play again [R]", False,("white"))
restart_label_rect = restart_label.get_rect(center=(640, 460))
ammo_left =label.render(f'Ammo Left: {ammo} ', False,(193,196,199))
ammo_left_rect = ammo_left.get_rect(topright=(640, 460))


gameplay = True

running = True
while running: # Аналог из tkinter win.mainloop()

    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 1280, 0))
    screen.blit(ammo_left, (1, 1))
    if gameplay:
    # Создаем коллизию
        player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))

    # Создаем переменную el, которая принимает картинку enemy и координаты из списка, добавляем enumerate для того,
    # чтобы удобно индексировать врагов и удалять их после исчезновения с экрана
        if enemy_list_in_game:
            for (i, el) in enumerate (enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10      # Движение врага

                if el.x < -10:
                    enemy_list_in_game.pop(0)   # Без 0 неправильно чистилось

    # Задаем условия столкновения
                if player_rect.colliderect(el):
                    gameplay = False


    # Проверка на движение влево/вправо
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

    # Движение персонажа
        if keys[pygame.K_a] and player_x > 50:   # Если нажата кнопка влево и координата по x больше 50, то персонаж дальше не идет
            player_x -= player_speed + 6
        elif keys[pygame.K_d] and player_x < 1230:   # Если нажата кнопка вправо и координата по x меньше 200, то персонаж дальше не идет
            player_x += player_speed
    # Прыжок
        if not is_jump:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_height >= -7:
                if jump_height > 0:
                    player_y -= (jump_height ** 2) / 2
                else:
                    player_y += (jump_height ** 2) / 2
                jump_height -= 1
            else:
                is_jump = False
                jump_height = 7
    # Смена анимации при движении
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1
    # Скорость смены задника
        bgx -= 6
    # Условие движения экрана
        if bgx <= -1280:
            bgx = 0

        ammo_left = label.render(f'Ammo Left: {ammo} ', False, ("black"))
        ammo_left_rect = ammo_left.get_rect(topright=(640, 460))

        if bullets:
            for (i, el) in enumerate (bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 1290:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate (enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        # Вывод экрана проигрыша вместе с текстом
        screen.blit(lose_bg, (bg_lose_x, 0))
        screen.blit(restart_label, restart_label_rect)

        # Условия рестарта
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()      # Этот метод присваивает координаты x, y переменной mouse
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] or keys[pygame.K_r]:    # collidepoint - проверяет соприкосновение прямоугольника текста рестарта с мышью
            gameplay = True
            player_x = 150
            player_y = 565
            bullets.clear()
            enemy_list_in_game.clear()  # Чистим врагов
            ammo = 5

    pygame.display.flip()     # Обновляет изображения на экране

    for event in pygame.event.get():    # Получаем список из всех возможных событий
        if event.type == pygame.QUIT:   # Если мы нажимаем на кнопку закрытия, то закрывается цикл, соответственно закрывается программа
            running = False
            pygame.quit()
        if event.type == enemy_timer:   # Если событие enemy_timer, то добавляем колизию врага в список
           enemy_list_in_game.append(enemy.get_rect(topleft=(1290, 587)))
        if gameplay and event.type == pygame.MOUSEBUTTONDOWN and ammo > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30,player_y + 10)))
            ammo -= 1

# Скоросить движения персонажа и также смены задника
    clock.tick(60)