import pygame
from pygame import KEYDOWN

pygame.init()   # Запуск программы, используется всегда как например в tkinter win = Tk()
screen = pygame.display.set_mode((600, 300))    # Метод для указания размеров экрана(в скобочках указывется кортеж)
pygame.display.set_caption("DND")   # Задаем название для игры
icon = pygame.image.load("images/icon.png")     # Создаем переменную для картинки
pygame.display.set_icon(icon)       # Загружаем иконку для приложения

square = pygame.Surface((50, 170))      # Содаем квадрат
square.fill("Blue")

# Подгружаем шрифт в PyCharm
myfont = pygame.font.Font("fonts/SourGummy-VariableFont_wdth,wght.ttf", 40)
# Обращаемся к переменной myfont и благодаря методу render меняем доп.параметры текста(текст, сглаживание, цвет, фон)
text_surface = myfont.render("DND Project", False, "Blue")

player = pygame.image.load("images/icon.png")

running = True
while running: # Аналог из tkinter win.mainloop()

    screen.blit(square,(100,0))   #blit выводим объект на экран, первое значение это название переменной объкта, а второе это координаты

    pygame.draw.circle(screen, "Purple", (250, 125), 30)    # Альтернативный вариант добавления фигуры на поверхность

    screen.blit(text_surface,(300, 100)) # Располагаем текст на экране

    screen.blit(player, (100, 50))

    pygame.display.update()     # Обновляет изображения на экране

    for event in pygame.event.get():    # Получаем список из всех возможных событий
        if event.type == pygame.QUIT:   # Если мы нажимаем на кнопку закрытия, то закрывается цикл, соответственно закрывается программа
            running = False
            pygame.quit()

