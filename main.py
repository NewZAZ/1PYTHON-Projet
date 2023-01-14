import tkinter
from tkinter import *
from tkinter import messagebox as mb, Frame, Text
from typing import Tuple, List, Dict


class Case:
    def __init__(self, max_pawn, pawn=0, player=0):
        self.__pawn = pawn
        self.__max_pawn = max_pawn
        self.__player = player
        self.__has_changed = True

    def set_player(self, x):
        self.__player = x
        self.set_changed(True)

    def get_player(self):
        return self.__player

    def increment_pawn(self):
        self.__pawn += 1
        self.set_changed(True)

    def set_pawn(self, x):
        self.__pawn = x
        self.set_changed(True)

    def get_pawn(self):
        return self.__pawn

    def get_max_pawn(self):
        return self.__max_pawn

    def has_changed(self):
        return self.__has_changed

    def set_changed(self, boolean):
        self.__has_changed = boolean


class Game:

    def __init__(self):
        self.__amount_players: int = None
        self.__rows: int = None
        self.__columns: int = None
        self.__place: bool = False
        self.__cases: List[List[Case]] = []
        self.__next_player_canvas: Canvas = None
        self.__player_select_canvas: Canvas = None
        self.__rowText: Text = None
        self.__columnText: Text = None
        self.__selection_frame: Frame = None
        self.__is_started: bool = False
        self.__players: List[int] = []
        self.__counter: int = 1
        self.__game_frame: Frame = None
        self.__colors: Dict[int, str] = {1: "blue", 2: "red", 3: "yellow", 4: "green", 5: "orange", 6: "pink",
                                         7: "purple", 8: "cyan"}

        self.__root = tkinter.Tk()
        self.__root.title("Jeux python")
        self.__root.config(bg='black')

        self.show_selection()

        self.__root.mainloop()

    def show_selection(self):

        self.__selection_frame = tkinter.Frame(self.__root)
        self.__selection_frame.config(bg='white')
        self.__selection_frame.grid(row=0, column=1, padx=25)

        columnLabel = Label(self.__selection_frame, text="Nombre de colonne(s) : ")
        columnLabel.config(bg='white')
        columnLabel.grid(row=0, column=0)

        self.__columnText = Text(self.__selection_frame, height=1, width=20, bg='white')

        self.__columnText.grid(row=0, column=1)

        rowLabel = Label(self.__selection_frame, text="Nombre de ligne(s) : ")

        rowLabel.config(bg='white')
        rowLabel.grid(row=1, column=0)

        self.__rowText = Text(self.__selection_frame, height=1, width=20, bg='white')

        self.__rowText.grid(row=1, column=1)

        self.__player_select_canvas = tkinter.Frame(self.__selection_frame)

        self.__player_select_canvas.config(bg='white')
        self.__player_select_canvas.grid(row=5, column=0)

        currentColumn = 0
        currentRow = 0
        for colors in self.__colors:
            color = self.__colors[colors]
            canvas = Canvas(self.__player_select_canvas, width=64, height=64)

            canvas.create_oval(8, 56, 56, 8, fill=color)

            if colors != 1 and colors % 4 == 1:
                currentRow += 1
                currentColumn = 0
            canvas.grid(pady=10, column=currentColumn, row=currentRow)
            canvas.config(bg='white', borderwidth=0, highlightthickness=0)
            canvas.bind('<Button-1>',
                        lambda event, selectCanvas=canvas, selectColor=colors: self.selectPlayer(selectCanvas,
                                                                                                 selectColor))
            currentColumn += 1

        startButton = Button(self.__selection_frame, height=1, width=10, text="Commencez",
                             command=lambda: self.canStart())
        startButton.config(bg='white')
        startButton.grid(row=2, column=0)

    def selectPlayer(self, canvas, color):
        if self.__players.count(color) == 1:
            canvas.config(bg='white')
            self.__players.remove(color)
        else:
            canvas.config(bg='green')
            self.__players.append(color)

    def canStart(self):

        columnResult = self.__columnText.get("1.0", "end-1c")
        rowResult = self.__rowText.get("1.0", "end-1c")
        if not columnResult.isnumeric():
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 3 et 12 \ndans la case colonne !")
            return
        if not rowResult.isnumeric():
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 3 et 10 \ndans la case ligne !")
            return
        columns = int(eval(columnResult))
        rows = int(eval(rowResult))

        if 3 <= rows <= 10 and 3 <= columns <= 12:
            if len(self.__players) > 1:
                self.__rows = rows
                self.__columns = columns
                self.startGame()
            else:
                mb.showerror("Erreur", "Veuillez choisir minimum 2 joueurs !")
        else:
            mb.showerror("Erreur", "Veuillez choisir une taille de jeux conforme !")

    def startGame(self):
        self.__selection_frame.destroy()
        self.__is_started = True

        self.__place = False
        self.__cases = [[Case(self.case_type(i, j), 0, 0) for j in range(self.__columns)] for i in
                        range(self.__rows)]

        self.__counter = 1
        self.show_next_player()

        self.__game_frame = tkinter.Frame(self.__root)
        self.show_game()
        self.__game_frame.grid(row=0, column=0, rowspan=5)

    def has_winner(self):
        if len(self.__players) == 1:
            return True
        else:
            return False

    def handle_round(self):
        if not self.__is_started:
            return
        if not self.has_winner():
            if self.__place:
                if self.__counter == len(self.__players):
                    self.__counter = 1
                else:
                    self.__counter += 1
                if not self.can_place_pawn():
                    self.__players.pop(self.__counter - 1)
                    self.__counter -= 1
                    self.handle_round()
            else:
                if self.__counter == len(self.__players):
                    self.__counter = 1
                    self.__place = True
                else:
                    self.__counter += 1
            self.show_next_player()
            return True
        else:
            self.game_finish()
            return False

    def show_next_player(self):
        if not self.__is_started:
            return
        self.__next_player_canvas = Canvas(self.__root, width=64, height=64)
        self.__next_player_canvas.create_oval(8, 56, 56, 8, fill=self.__colors[self.__players[self.__counter - 1]])

        self.__next_player_canvas.grid(pady=10, column=0, row=5)
        self.__next_player_canvas.config(bg='black', borderwidth=0, highlightthickness=0)

    def game_finish(self):
        self.show_selection()
        self.__game_frame.destroy()
        self.__next_player_canvas.delete("all")
        mb.showinfo("Gagnant", "le joueur " + self.__colors[self.__players[0]] + " a gagner !")
        self.__is_started = False
        self.clear_game()

    def can_place_pawn(self):
        for rows in self.__cases:
            for case in rows:
                if case.get_player() == self.__players[self.__counter - 1]:
                    return True
        else:
            return False

    def show_game(self):
        if not self.__is_started:
            return
        location_1: Tuple[int, int] = (16, 48)
        location_2: Tuple[int, int, int, int] = (8, 28, 28, 48)
        location_3: Tuple[int, int, int, int, int, int] = (8, 24, 24, 40, 40, 56)

        for x in range(len(self.__cases)):
            for y in range(len(self.__cases[x])):
                case = self.__cases[x][y]
                if case.has_changed():
                    case.set_changed(False)
                    pawn_canvas = tkinter.Canvas(self.__game_frame)
                    pawn_canvas.grid(row=x, column=y, padx=0, pady=0)
                    pawn_canvas.config(width=64, height=64, highlightbackground="red", highlightcolor="red",
                                       highlightthickness=1, bg='#004F61')

                    if case.get_pawn() == 1:
                        pawn_canvas.create_oval(x + location_1[0], y + location_1[0],
                                                x + location_1[1], y + location_1[1],
                                                fill=self.__colors[case.get_player()])
                    elif case.get_pawn() == 2:
                        pawn_canvas.create_oval(x + location_2[0], y + location_2[0],
                                                x + location_2[1], y + location_2[1],
                                                fill=self.__colors[case.get_player()])
                        pawn_canvas.create_oval(x + location_2[2], y + location_2[2],
                                                x + location_2[3], y + location_2[3],
                                                fill=self.__colors[case.get_player()])
                    elif case.get_pawn() == 3:
                        pawn_canvas.create_oval(x + location_3[0], y + location_3[0],
                                                x + location_3[1], y + location_3[1],
                                                fill=self.__colors[case.get_player()])
                        pawn_canvas.create_oval(x + location_3[2], y + location_3[2],
                                                x + location_3[3], y + location_3[3],
                                                fill=self.__colors[case.get_player()])
                        pawn_canvas.create_oval(x + location_3[4], y + location_3[4],
                                                x + location_3[5], y + location_3[5],
                                                fill=self.__colors[case.get_player()])
                    pawn_canvas.bind('<Button-1>', lambda event, coord=(x, y): self.play(coord))

    def play(self, coord):
        coord_x = coord[0]
        coord_y = coord[1]
        case = self.__cases[coord_x][coord_y]
        if case.get_player() == self.__players[self.__counter - 1] or case.get_player() == 0:
            case.set_changed(True)
            if case.get_pawn() == case.get_max_pawn():
                self.blast(coord_x, coord_y)
            else:
                self.put_pawn(coord_x, coord_y)
            if self.handle_round():
                self.show_game()

    def put_pawn(self, coord_x, coord_y):
        self.__cases[coord_x][coord_y].set_player(self.__players[self.__counter - 1])
        self.__cases[coord_x][coord_y].increment_pawn()

    def case_type(self, coord_x, coord_y):
        if coord_x == 0 and coord_y == 0:
            return 1  # La case est un coin
        if coord_x == 0 and coord_y == self.__columns - 1:
            return 1  # La case est un coin
        if coord_x == self.__rows - 1 and coord_y == 0:
            return 1  # La case est un coin
        if coord_x == self.__rows - 1 and coord_y == self.__columns - 1:
            return 1  # La case est un coin
        if coord_x == 0:
            return 2  # La case est un côté
        if coord_x == self.__rows - 1:
            return 2  # La case est un côté
        if coord_y == 0:
            return 2  # La case est un côté
        if coord_y == self.__columns - 1:
            return 2  # La case est un côté
        else:
            return 3  # La case n'est ni un côté ni un coin

    def blast(self, coord_x, coord_y):
        self.__cases[coord_x][coord_y].set_pawn(0)
        self.__cases[coord_x][coord_y].set_player(0)

        player = self.__players[self.__counter - 1]
        if coord_x != 0:
            self.__cases[coord_x - 1][coord_y].set_player(player)
            self.chain_reaction(coord_x - 1, coord_y)
        if coord_x != self.__rows - 1:
            self.__cases[coord_x + 1][coord_y].set_player(player)
            self.chain_reaction(coord_x + 1, coord_y)
        if coord_y != 0:
            self.__cases[coord_x][coord_y - 1].set_player(player)
            self.chain_reaction(coord_x, coord_y - 1)
        if coord_y != self.__columns - 1:
            self.__cases[coord_x][coord_y + 1].set_player(player)
            self.chain_reaction(coord_x, coord_y + 1)

    def chain_reaction(self, coord_x, coord_y):
        if self.__cases[coord_x][coord_y].get_pawn() == self.__cases[coord_x][coord_y].get_max_pawn():
            self.blast(coord_x, coord_y)
        else:
            self.put_pawn(coord_x, coord_y)

    def clear_game(self):
        self.__players = []
        self.__counter = 1
        self.__place = False
        self.__cases = []


Game()  # A chaque tour -> on change de joueur,
#                  es ce que le joueur peut jouer,
#                   si le joueur peut pas jouer, le supprimer des tours, et passer au tour suivant
# si le joueur joue, lui demander les coordonnées, si il peut poser, sur SA Couleur ou case vide
#   alors poser, et faire réaction en chaines de SA couleur si explosion
#   après pose, passer tour


# nbrjoueurs=input
# colonnes=input
# lignes=input
# case1=[nbrpions, joueurs]
# [[case1,case2,case3],[case1bas,case2bas,cas3bas]]
# method spread(spread gauche,spreaddroit,spreadhaut,spreadbas)
# fctn tableau
# def get_lignes(lignes)
# possibleposerpion-> si la case est vide ou lui appartient,
#                             check le nombremaxium de pion que la case peut supporter,
#                                 si on est a son maximum ->3
#                                     explosion() rajoute automatiquement explose des cotés otut odzdz
#                                 sinon ajouter +1
# self.poser / poser=False, Permet de savoir si les joueurs ont tous pu au moins poser 1 pion
