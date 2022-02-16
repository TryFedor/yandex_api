import time
import pygame
import requests
from urllib.parse import quote

# w, a, s, d - управление картой
# q - переключение между слоями карт
# колесико мыши - увеличение/уменьшение карты

pygame.init()
screen = pygame.display.set_mode((800, 450))

api = 'd0e1a27b-c598-41c2-bc88-fa646d976d83'


def fetch_coordinates(apikey, address_):
    base_url = f"https://geocode-maps.yandex.ru/1.x?geocode={quote(address_)}&apikey={apikey}&format=json"
    print(base_url)
    response = requests.get(base_url)
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


have_metka = False
x_metka = 0
y_metka = 0


class MainClass():
    def main(x_: float, y_: float, type: str, zoom: int, text="pmwtm1"):
        global have_metka, x_metka, y_metka
        if not have_metka:
            map_link = f'http://static-maps.yandex.ru/1.x/?ll={str(x)}%2C-{str(y)}&l={type}&z={zoom}&size=600,450&lang=ru_RU'
        else:
            map_link = f'http://static-maps.yandex.ru/1.x/?ll={str(x)}%2C-{str(y)}&l={type}&z={zoom}&pt={str(x_metka)},{str(y_metka)},{text}&size=600,450&lang=ru_RU'
        response = requests.get(map_link)
        print(map_link)
        try:
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)

            global screen
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
            return True
        except Exception as ex:
            print(ex, f"\nx: {x_}, y: {y_}, type: {type}, zoom: {zoom}")
            return False


zoom = 3
x = 5
y = 5
horizontal = 10
vertical = 10

mc = MainClass

typesIndex = 0
types = ["map", "sat", "sat,skl"]
type = types[0]

mc.main(x, y, type, zoom)

input_box = None
done = True
text = ''


def CreateInputBox(x_, y_, plus_x, plus_y):
    # screen = pygame.display.set_mode((600, 450))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(x_, y_, plus_x, plus_y)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''

    global done
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 620 < i.pos[0] < 700:
                    done = False
                    # CreateInputBox(620, 80, 50, 50)
                else:
                    pygame.draw.rect(screen, color, input_box, 2)
                    text = ''
                    done = True

                    txt_surface = font.render('', True, color)
                    width = max(plus_x, txt_surface.get_width() + 10)
                    input_box.w = width
                    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                    pygame.draw.rect(screen, color, input_box, 2)

                    pygame.display.flip()
                    clock.tick(30)

                    CreateInputBox(620, 10, 165, 50)

                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                        try:
                            pygame.draw.rect(
                                screen,  # экран
                                (30, 30, 30),  # цвет
                                (x_, y_, plus_x, plus_y))  # координаты

                            coords = fetch_coordinates(api, text)
                            global x, y, mc
                            x = float(coords[0])
                            y = float(coords[1])
                            if x < 0: x = -x
                            if y < 0: y = -y
                            global have_metka, x_metka, y_metka
                            have_metka = True
                            x_metka = float(coords[0])
                            y_metka = float(coords[1])
                            mc.main(x, y, type, zoom, "pmwtm1")  # конго
                        except Exception as ex:
                            print(ex)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        pygame.draw.rect(screen,  # экран
                                         (30, 30, 30),  # цвет
                                         (x_, y_, plus_x, plus_y))  # координаты
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(plus_x, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


color = pygame.Color('lightskyblue3')
input_box = pygame.Rect(620, 10, 165, 50)
pygame.draw.rect(screen, color, input_box, 2)

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
            elif 620 < i.pos[0] < 700:
                done = False
                CreateInputBox(620, 10, 165, 50)
            else:
                text = ''
                done = True

        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_q:
                typesIndex += 1
                if typesIndex == len(types): typesIndex = 0
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

