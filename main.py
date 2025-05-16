import pyxel
import random as r

global scale
scale = 12


def algo_ship_placement(x, y, taille, orientation, ship_list):
    if orientation == "horizontal" and x + taille > 9:
        print(f"Taille {taille} -- Orientation {orientation} = {x + taille}")
        return False
    if orientation == "vertical" and y + taille > 9:
        print(f"Taille {taille} -- Orientation {orientation} = {y + taille}")
        return False


    return True

def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
        return True
    return False


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
        for i in range(self.taille):
            if self.orientation == "horizontal":
                print(f"Génération du chunk en x{self.x+i} y{self.y}")
                self.chunks_list.append(Chunk(self.x+i, self.y))
            if self.orientation == "vertical":
                print(f"Génération du chunk en x{self.x} y{self.y+i}")
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
            x_p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            y_p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            algo = False
            while algo is False:
                x = r.choice(x_p)
                y = r.choice(y_p)
                print(f"Génération d'un bateau de taille {ship_taille} {orientation} en x{x}, y{y} \n"
                      f"xp {x_p}"
                      f"yp {y_p}")
                algo = algo_ship_placement(x, y, ship_taille, orientation, self.ship_list)
                if orientation == "horizontal":
                    x_p.pop(x-(10-len(x_p)))
                if orientation == "vertical":
                    y_p.pop(y-(10-len(y_p)))
                print(x_p)
                print(y_p)


            ship = Ship(x, y, ship_taille, orientation)
            ship.generate_chunks()
            self.ship_list.append(ship)


    def torpille(self):
        x = r.randint(0, 9)
        y = r.randint(0, 9)
        for attack in self.attack_list:
            if attack == (x, y):
                self.torpille()

        self.attack_list.append((x, y))
        return x, y

    def toucher(self, x, y):
        for ship in self.ship_list:
            for chunk in ship.chunks_list:
                if chunk.x == x and chunk.y == y and chunk.state == "vivant":
                    chunk.state = "mort"
                    return True
        return False

    def vivant(self):
        for ship in self.ship_list:
            for chunk in ship.chunks_list:
                if chunk.state == "vivant":
                    return True
        return False


class App:
    def __init__(self):
        pyxel.init(128, 128, title="MégaBataille", fps=30)
        self.turn = "player"
        self.player = Player()
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)





    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()



class Player:
    def __init__(self):
        self.ship_size = [5, 4, 3, 3, 2]
        self.ship_list_preview = [[0, 0, width, 1, 0] for width in self.ship_size]
        self.selected_ship = 0
        self.placement_error = False
        self.edit = True
        self.ship_list = []
        self.attack_list = []
        self.ennemy = Ennemy([5, 4, 3, 3, 2])
        self.ennemy.generate_ships()


    def vivant(self):
        for ship in self.ship_list:
            for chunk in ship.chunks_list:
                if chunk.state == "vivant":
                    return True
        return False

    def rotate_selected_ship(self):
        x, y, width, height, orientation = self.ship_list_preview[self.selected_ship]
        width, height = height, width
        self.ship_list_preview[self.selected_ship][2] = width
        self.ship_list_preview[self.selected_ship][3] = height

    def select_ship(self):
        for i, ship in enumerate(self.ship_list_preview):
            x, y, width, height, orientation = ship
            if collision(x, y, width * scale, height * scale, pyxel.mouse_x, pyxel.mouse_y, 4, 4) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.selected_ship = i
                break

    def ship_collision(self):
        for i, ship in enumerate(self.ship_list_preview):
            if i == self.selected_ship:
                continue
            else:
                x, y, width, height, orientation = self.ship_list_preview[self.selected_ship]
                x2, y2, width2, height2, orientation2 = ship
                if collision(x, y, width * scale, height * scale, x2, y2, width2 * scale, height2 * scale):
                    self.placement_error = True
                    break
                else:
                    self.placement_error = False

    def move_ship(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.ship_list_preview[self.selected_ship][0] = pyxel.mouse_x - (pyxel.mouse_x % scale)
            self.ship_list_preview[self.selected_ship][1] = pyxel.mouse_y - (pyxel.mouse_y % scale)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self.ship_list_preview[self.selected_ship][4] = 0 if self.ship_list_preview[self.selected_ship][4] == 1 else 1
            self.rotate_selected_ship()

    def place_ship(self):
        self.select_ship()
        self.move_ship()
        self.ship_collision()

    def toucher(self, x, y):
        for ship in self.ship_list:
            for chunk in ship.chunks_list:
                if chunk.x == x and chunk.y == y and chunk.state == "vivant":
                    chunk.state = "mort"
                    return True
        return False

    def click(self):
        if self.ennemy.vivant() and self.vivant():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x = (pyxel.mouse_x - 34) // scale
                y = pyxel.mouse_y // scale
                self.attack_list.append((x, y))
                if 0 <= x <= 9 and 0 <= y <= 9:
                    self.ennemy.toucher(x, y)
                torpille = self.ennemy.torpille()
                self.toucher(torpille[0], torpille[1])
        else:
            pyxel.cls(0)
            pyxel.text(0, 0, "Le jeu est terminé.", 8)


    def start(self):
        if pyxel.btn(pyxel.KEY_RETURN) and not self.placement_error:
            self.edit = False
            for ship in self.ship_list_preview:
                orientation = {0: "horizontal", 1: "vertical"}
                if orientation[ship[4]] == "horizontal":
                    self.ship_list.append(Ship(ship[0] // scale, ship[1] // scale, ship[2], orientation[ship[4]]))
                else:
                    self.ship_list.append(Ship(ship[0] // scale, ship[1] // scale, ship[3], orientation[ship[4]]))
            for ship in self.ship_list:
                ship.generate_chunks()
                print(ship)





    def draw_ship_preview(self):
        for i, ship in enumerate(self.ship_list_preview):
            x, y, width, height, orientation = ship
            colkey = 2
            if self.selected_ship == i:
                colkey = 3
                if self.placement_error:
                    colkey = 8
            width, height = width * scale, height * scale
            pyxel.rect(x, y, width, height, colkey)

    def draw_rectangles(self):
        pyxel.rect(34, 0, 60, 60, 10)
        pyxel.rect(34, 68, 60, 60, 10)

    def draw_ship(self):
        for attack in self.attack_list:
            pyxel.rect((attack[0] * scale + 34), (attack[1] * scale), scale, scale, 13)

        for ship in self.ennemy.ship_list:
            for chunk in ship.chunks_list:
                if chunk.state == "mort":
                    pyxel.rect((chunk.x*scale + 34), (chunk.y*scale), scale, scale, 8)

        for attack in self.ennemy.attack_list:
            pyxel.rect((attack[0] * scale + 34), (attack[1] * scale + 68), scale, scale, 13)

        for ship in self.ship_list:
            for chunk in ship.chunks_list:
                if chunk.state == "vivant":
                    pyxel.rect((chunk.x * scale + 34), (chunk.y * scale + 68), scale, scale, 11)
                else:
                    pyxel.rect((chunk.x * scale + 34), (chunk.y * scale + 68), scale, scale, 8)


    def update(self):
        if self.edit:
            self.place_ship()
            self.start()
        else:  #Début du jeu
            globals()["scale"] = 6
            self.click()

    def draw(self):
        if self.edit:
            self.draw_ship_preview()
        else:
            self.draw_rectangles()
            self.draw_ship()

App()
