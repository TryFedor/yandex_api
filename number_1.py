import time
import pygame
import requests

# w, a, s, d - управление картой
# q - переключение между слоями карт
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
zoom = 1
x = 5
y = 5
horizontal = 10
vertical = 10

mc = MainClass
mc.main(x, y, type, zoom)

typesIndex = 0
types = ["map", "sat", "sat,skl"]
type = types[0]

while True:
    time.sleep(0.001)

    if zoom < 5:
        horizontal, vertical = 10, 10
    elif zoom < 8:
        horizontal, vertical = 2, 2
    elif zoom < 10:
        horizontal, vertical = 0.5, 0.5
    elif zoom < 13:
        horizontal, vertical = 0.025, 0.025
    else:
        horizontal, vertical = 0.005, 0.005

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

        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_q:
                typesIndex += 1
                if typesIndex == len(types):
                    typesIndex = 0
                type = types[typesIndex]
                mc.main(x, y, type, zoom)
            elif i.key == pygame.K_s:
                y += vertical
                if not mc.main(x, y, type, zoom):
                    y -= vertical
            elif i.key == pygame.K_w:
                y -= vertical
                mc.main(x, y, type, zoom)
                if not mc.main(x, y, type, zoom):
                    y += vertical
            elif i.key == pygame.K_a:
                x -= horizontal
                if not mc.main(x, y, type, zoom):
                    x += horizontal
            elif i.key == pygame.K_d:
                x += horizontal
                if not mc.main(x, y, type, zoom):
                    x -= horizontal

