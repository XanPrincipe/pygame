import pygame
from pygame import KEYDOWN


clock = pygame.time.Clock()#    Создаем переменную для задержки анимации
pygame.init()   # Запуск программы, используется всегда как например в tkinter win = Tk()
screen = pygame.display.set_mode((1280, 720))    # Метод для указания размеров экрана(в скобочках указывется кортеж)
pygame.display.set_caption("DND")   # Задаем название для игры
icon = pygame.image.load("images/icon.png")     # Создаем переменную для картинки
pygame.display.set_icon(icon)       # Загружаем иконку для приложения


# Подкючаем задник и все анимации
bg = pygame.image.load("images/Game_Background.png")
walk_left = [
    pygame.image.load("images/player_left/left1.png"),
    pygame.image.load("images/player_left/left2.png"),
    pygame.image.load("images/player_left/left3.png"),
    pygame.image.load("images/player_left/left4.png"),
]

walk_right = [
    pygame.image.load("images/player_right/right1.png"),
    pygame.image.load("images/player_right/right2.png"),
    pygame.image.load("images/player_right/right3.png"),
    pygame.image.load("images/player_right/right4.png"),
]
# Создаем счетчик анимаций
player_anim_count = 0
# Создаем переменную для дальнейшего движения заднего фона
bgx = 0
# Подключаем звук для задника
bg_sound = pygame.mixer.Sound("sound/bg_snd.mp3")
bg_sound.play(-1)   # Бесконечное проигрывание


running = True
while running: # Аналог из tkinter win.mainloop()

    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 1280, 0))
    screen.blit(walk_right[player_anim_count], (300,565))

    if player_anim_count == 3:
        player_anim_count = 0
    else:
        player_anim_count += 1
# Скорость смены задника
    bgx -= 6
# Условие движения экрана
    if bgx <= -1280:
        bgx = 0


    pygame.display.update()     # Обновляет изображения на экране

    for event in pygame.event.get():    # Получаем список из всех возможных событий
        if event.type == pygame.QUIT:   # Если мы нажимаем на кнопку закрытия, то закрывается цикл, соответственно закрывается программа
            running = False
            pygame.quit()
# Скоросить движения персонажа и также смены задника
    clock.tick(30)