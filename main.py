import pygame
from pygame import KEYDOWN

pygame.init()   # Запуск программы, используется всегда как например в tkinter win = Tk()
screen = pygame.display.set_mode((600, 300))    # Метод для указания размеров экрана(в скобочках указывется кортеж)
pygame.display.set_caption("DND")   # Задаем название для игры
icon = pygame.image.load("images/icon.png")     # Создаем переменную для картинки
pygame.display.set_icon(icon)       # Загружаем иконку для приложения
running = True
while running: # Аналог из tkinter win.mainloop()

    #screen.fill((123, 167, 237))    # Устанавливем заливку заднего фона для основного окна через rgb палитру(помещаем цифры в кортеж)

    pygame.display.update()     # Обновляет изображения на экране
    for event in pygame.event.get():    # Получаем список из всех возможных событий
        if event.type == pygame.QUIT:   # Если мы нажимаем на кнопку закрытия, то закрывается цикл, соответственно закрывается программа
            running = False
            pygame.quit()
        elif event.type == KEYDOWN:     # Если кнопка опущена и если эта кнопка A, то цвет экрана меняется
            if event.key == pygame.K_a:
                screen.fill((155, 30, 227))
