import time
import pygame
import requests

# колесико мыши - увеличение/уменьшение карты

pygame.init()
screen = pygame.display.set_mode((600, 450))


class MainClass():
    def main(x: int, y: int, type: str, zoom: int):
        map_link = f'http://static-maps.yandex.ru/1.x/?ll={str(x)}%2C-{str(y)}&l={type}&z={zoom}&size=600,450&lang=ru_RU'
        response = requests.get(map_link)
        try:
            map_file = "map.bmp"
            with open(map_file, "wb") as file:
                file.write(response.content)

            global screen
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
            return True
        except:
            return False


type = "map"
zoom = 3
x = 5
y = 5

mc = MainClass
mc.main(x, y, type, zoom)

while True:
    time.sleep(0.001)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()

        elif i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 5:
                zoom -= 1
                if not mc.main(x, y, type, zoom):
                    zoom += 1
            elif i.button == 4:
                zoom += 1
                if not mc.main(x, y, type, zoom) or zoom > 20:
                    zoom -= 1

