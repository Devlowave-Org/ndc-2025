import pyxel
import random as r


def algo_ship_placement(x, y, taille, orientation, ship_list):
    if orientation == "horizontal" and x + taille > 9:
        return False
    if orientation == "vertical" and y + taille > 9:
        return False
    for ship in ship_list:
        for chunk in ship.chunks:
            for i in range(0, taille):
                if chunk.x == x + i and chunk.y == y + i:
                    return False
    return True


class Chunck:
    def __init__(self, x, y, state="vivant"):
        self.x = x
        self.y = y
        self.state = state


class Ship:
    def __init__(self, x: int, y: int, taille: int, orientation):
        self.x = x
        self.y = y
        self.taille = taille
        self.orientation = orientation
        self.chunks_list = []

    def generate_chunks(self):
        for i in range(0, self.taille):
            self.chunks_list.append(Chunck(self.x, self.y))



class Ennemy:
    def __init__(self, ship_tailles: list):
        self.ship_tailles = ship_tailles
        self.ship_list = []

    def generate_ships(self):
        for ship_taille in self.ship_tailles:
            x = r.randint(0, 10)
            y = r.randint(0, 10)
            orientation = r.choice(["horizontal", "vertical"])
            while algo_ship_placement(x, y, ship_taille, orientation, self.ship_list) is False:
                x = r.randint(0, 10)
                y = r.randint(0, 10)
                orientation = r.choice(["horizontal", "vertical"])

            self.ship_list.append(Ship(x, y, ship_taille, orientation))


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scale = 4
        self.grid = [[0 for x in range(width)] for y in range(height)]

    def draw(self):
        pyxel.rect(0, 0, self.width*self.scale, self.height*self.scale, 1)





class App:
    def __init__(self):
        pyxel.init(128, 128, title="MégaBataille", fps=60)

    def update(self):
        pass

    def draw(self):
        pass




