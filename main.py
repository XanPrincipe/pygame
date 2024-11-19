import pygame

clock = pygame.time.Clock()  # Создаем переменную для задержки анимации
pygame.init()  # Запуск программы, используется всегда как например в tkinter win = Tk()
screen = pygame.display.set_mode((1280, 720))  # Метод для указания размеров экрана(в скобочках указывется кортеж)
pygame.display.set_caption("DND")  # Задаем название для игры
icon = pygame.image.load("images/icon.png").convert_alpha()  # Создаем переменную для картинки
pygame.display.set_icon(icon)  # Загружаем иконку для приложения

# Подключаем задник и все анимации
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

ammo_reload = pygame.image.load("images/bullet/reload.png").convert_alpha()

# Добавляем врага
enemy = pygame.image.load("images/enemy/enemy.png").convert_alpha()  # Для png всегда писать convert_alpha, а для всех других можно просто convert
# Добавляем патрон
bullet = pygame.image.load("images/bullet/bullet.png").convert_alpha()
bullets = []
# Добавляем список с врагами
enemy_list_in_game = []
# Создаем счетчик анимаций
player_anim_count = 0
# Список с паверапами
power_up = []

# Создаем переменную для дальнейшего движения заднего фона
bgx = 0
bg_lose_x = 0

player_speed = 7  # Скорость персонажа
player_x = 150  # Координата персонажа по x
player_y = 565  # Координата персонажа по y

is_jump = False
jump_speed = 0  # Начальная скорость прыжка
gravity = 0.5  # Ускорение свободного падения

# Подключаем звук для задника
bg_sound = pygame.mixer.Sound("sound/bg_snd.mp3")
bg_sound.play(-1)
bg_sound.set_volume(0.1)
# Добавляем таймер появления монстров на экране

enemy_timer = pygame.USEREVENT + 1
power_up_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_timer, 2000)
# Добавляем таймер появления паверавов на экране
pygame.time.set_timer(power_up_timer, 5000)
ammo = 5

# Подключаем шрифт и задаем параметры текста
label = pygame.font.Font("fonts/SourGummy-VariableFont_wdth,wght.ttf", 40)
restart_label = label.render("Play again [R]", False, ("white"))
restart_label_rect = restart_label.get_rect(center=(640, 460))
ammo_left = label.render(f'Ammo Left: {ammo} ', False, (193, 196, 199))
ammo_left_rect = ammo_left.get_rect(topright=(640, 460))

gameplay = True
running = True
show_restart_button = False  # Добавляем флаг для отображения кнопки перезапуска

while running:  # Аналог из tkinter win.mainloop()
    for event in pygame.event.get():  # Получаем список из всех возможных событий
        if event.type == pygame.QUIT:  # Если мы нажимаем на кнопку закрытия, то закрывается цикл, соответственно закрывается программа
            running = False
            pygame.quit()
        if event.type == enemy_timer:  # Если событие enemy_timer, то добавляем коллизию врага в список
            enemy_list_in_game.append(enemy.get_rect(topleft=(1290, 587)))
        if gameplay and event.type == pygame.MOUSEBUTTONDOWN and ammo > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            ammo -= 1
        if event.type == power_up_timer:
            power_up.append(ammo_reload.get_rect(topleft=(1290, 500)))
        if (not gameplay and event.type == pygame.KEYUP
                and event.key == pygame.K_r
                or (show_restart_button and restart_label_rect.collidepoint(pygame.mouse.get_pos())
                    and event.type == pygame.MOUSEBUTTONDOWN)):
            gameplay = True
            player_x = 150
            player_y = 565
            bullets.clear()
            enemy_list_in_game.clear()  # Чистим врагов
            ammo = 5
            is_jump = False  # Сброс состояния прыжка
            jump_speed = 0  # Сброс скорости прыжка
            bg_sound.play(-1)
            power_up.clear()
            show_restart_button = False  # Скрываем кнопку перезапуска

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 1280, 0))
    screen.blit(ammo_left, (0, 0))


    if gameplay:
        # Создаем коллизию
        player_rect = walk_right[0].get_rect(topleft=(player_x, player_y))

        # Создаем переменную el, которая принимает картинку enemy и координаты из списка, добавляем enumerate для того,
        # чтобы удобно индексировать врагов и удалять их после исчезновения с экрана
        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10  # Движение врага

                if el.x < -10:
                    enemy_list_in_game.pop(0)  # Без 0 неправильно чистилось

                # Задаем условия столкновения
                if player_rect.colliderect(el):
                    gameplay = False
                    show_restart_button = True  # Показываем кнопку перезапуска
        # Создаем паверап
        if power_up:
            for (i, el) in enumerate (power_up):
                screen.blit(ammo_reload, el)
                el.x -= 5

                if el.x < -10:
                    power_up.pop(0)

                if player_rect.colliderect(el):
                    if ammo == 4:
                        ammo = 5
                    if ammo < 5:
                        ammo += 2

                    power_up.pop(0)
        # Проверка на движение влево/вправо
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count // 20], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count // 20], (player_x, player_y))

        # Движение персонажа
        if keys[pygame.K_a] and player_x > 50:  # Если нажата кнопка влево и координата по x больше 50, то персонаж дальше не идет
            player_x -= player_speed + 6
        elif keys[pygame.K_d] and player_x < 1230:  # Если нажата кнопка вправо и координата по x меньше 200, то персонаж дальше не идет
            player_x += player_speed

        # Прыжок
        if not is_jump:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                is_jump = True
                jump_speed = -10  # Начальная скорость прыжка
        else:
            player_y += jump_speed  # Изменяем положение по вертикали
            jump_speed += gravity  # Увеличиваем скорость падения (гравитация)

            # Если персонаж на земле, то сбросить параметры прыжка
            if player_y >= 565:
                player_y = 565
                is_jump = False

        # Смена анимации при движении
        if player_anim_count == 60:
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
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 1290:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        # Вывод экрана проигрыша вместе с текстом
        screen.blit(lose_bg, (bg_lose_x, 0))
        if show_restart_button:
            screen.blit(restart_label, restart_label_rect)
        bg_sound.stop()

    pygame.display.update()  # Обновляет изображения на экране

    # Скорость движения персонажа и также смены задника
    clock.tick(120)
