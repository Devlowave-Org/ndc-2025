import pyxel
import random as r


def algo_ship_placement(x, y, taille, orientation, ship_list):
    if orientation == "horizontal" and x + taille > 9:
        print(f"Taille {taille} -- Orientation {orientation} = {x + taille}")
        return False
    if orientation == "vertical" and y + taille > 9:
        print(f"Taille {taille} -- Orientation {orientation} = {y + taille}")
        return False

    if orientation == "horizontal":
        for i in range(0, taille):
            for ship in ship_list:
                for chunk in ship.chunks_list:
                    if chunk.x == x + i:
                        print(f"{chunk.x} {x+i}")
                        return False

    if orientation == "vertical":
        for i in range(0, taille):
            print(i)
            for ship in ship_list:
                for chunk in ship.chunks_list:
                    if chunk.y == y + i:
                        print(f"{chunk.y} {y+i}")
                        return False
    return True


class Chunk:
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
            if self.orientation == "horizontal":
                self.chunks_list.append(Chunk(self.x+i, self.y))
            if self.orientation == "vertical":
                self.chunks_list.append(Chunk(self.x, self.y+i))



class Ennemy:
    def __init__(self, ship_tailles: list):
        self.ship_tailles = ship_tailles
        self.ship_list = []
        self.attack_list = []

    def generate_ships(self):
        # On génère les bateaux en fonction de leur taille
        for ship_taille in self.ship_tailles:
            orientation = r.choice(["horizontal", "vertical"])
            x = 0
            y = 0
            algo = False
            while algo is False:
                x_p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                y_p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                x = r.choice(x_p)
                y = r.choice(y_p)
                algo = algo_ship_placement(x, y, ship_taille, orientation, self.ship_list)
                if orientation == "horizontal":
                    x_p.pop(x)
                if orientation == "vertical":
                    y_p.pop(y)
                print("---- On ressaie ----")


            ship = Ship(x, y, ship_taille, orientation)
            self.ship_list.append(ship)
            ship.generate_chunks()


    def lancer_une_torpille(self):
        x = r.randint(0, 9)




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




