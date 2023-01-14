import tkinter
from tkinter import *
from tkinter import messagebox as mb


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
        self.__amount_players = None
        self.__rows = None
        self.__columns = None
        self.__place = False
        self.__cases = None
        self.__nextPlayerCanvas = None
        self.__playerSelectCanvas = None
        self.__rowText = None
        self.__columnText = None
        self.__selectionFrame = None
        self.__isStarted = False
        self.__players = []
        self.__counter = 1
        self.__gameFrame = None
        self.__colors = {1: "blue", 2: "red", 3: "yellow", 4: "green", 5: "orange", 6: "pink", 7: "purple", 8: "cyan"}

        self.__root = tkinter.Tk()
        self.__root.title("Jeux python")
        self.__root.config(bg='black')

        self.show_selection()

        self.__root.mainloop()

    def show_selection(self):

        self.__selectionFrame = tkinter.Frame(self.__root)
        self.__selectionFrame.config(bg='white')
        self.__selectionFrame.grid(row=0, column=1, padx=25)

        columnLabel = Label(self.__selectionFrame, text="Nombre de colonne(s) : ")
        columnLabel.config(bg='white')
        columnLabel.grid(row=0, column=0)

        self.__columnText = Text(self.__selectionFrame, height=1, width=20, bg='white')

        self.__columnText.grid(row=0, column=1)

        rowLabel = Label(self.__selectionFrame, text="Nombre de ligne(s) : ")

        rowLabel.config(bg='white')
        rowLabel.grid(row=1, column=0)

        self.__rowText = Text(self.__selectionFrame, height=1, width=20, bg='white')

        self.__rowText.grid(row=1, column=1)

        self.__playerSelectCanvas = tkinter.Frame(self.__selectionFrame)

        self.__playerSelectCanvas.config(bg='white')
        self.__playerSelectCanvas.grid(row=5, column=0)

        currentColumn = 0
        currentRow = 0
        for colors in self.__colors:
            color = self.__colors[colors]
            canvas = Canvas(self.__playerSelectCanvas, width=64, height=64)

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

        startButton = Button(self.__selectionFrame, height=1, width=10, text="Commencez",
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
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 5 et 9 \ndans la case colonne !")
            return
        if not rowResult.isnumeric():
            mb.showerror("Erreur", "Veuillez choisir un nombre entre 5 et 9 \ndans la case ligne !")
            return
        columns = eval(columnResult)
        rows = eval(rowResult)

        if self.is_good_game_size((int(columns)), int(rows)):
            if len(self.__players) > 1:
                self.startGame()
            else:
                mb.showerror("Erreur", "Veuillez choisir minimum 2 joueurs !")
        else:
            mb.showerror("Erreur", "Veuillez choisir une taille de jeux conforme !")

    def startGame(self):
        self.__selectionFrame.destroy()
        self.__isStarted = True

        self.__place = False
        self.__cases = [[Case(self.case_type(i, j), 0, 0) for j in range(self.__columns)] for i in
                        range(self.__rows)]

        self.__counter = 1
        self.show_next_player()

        self.__gameFrame = tkinter.Frame(self.__root)
        self.show_game()
        self.__gameFrame.grid(row=0, column=0, rowspan=5)

    def has_winner(self):
        if len(self.__players) == 1:
            return True
        else:
            return False

    def handle_round(self):
        if not self.__isStarted:
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
        if not self.__isStarted:
            return
        self.__nextPlayerCanvas = Canvas(self.__root, width=64, height=64)
        self.__nextPlayerCanvas.create_oval(8, 56, 56, 8, fill=self.__colors[self.__players[self.__counter - 1]])

        self.__nextPlayerCanvas.grid(pady=10, column=0, row=5)
        self.__nextPlayerCanvas.config(bg='black', borderwidth=0, highlightthickness=0)

    def game_finish(self):
        self.show_selection()
        self.__gameFrame.destroy()
        self.__nextPlayerCanvas.delete("all")
        mb.showinfo("Gagnant", "le joueur " + self.__colors[self.__players[0]] + " a gagner !")
        self.__isStarted = False
        self.clear_game()

    def can_place_pawn(self):
        for rows in self.__cases:
            for case in rows:
                if case.get_player() == self.__players[self.__counter - 1]:
                    return True
        else:
            return False

    def is_good_game_size(self, column, row):
        if 3 <= row <= 10 and 3 <= column <= 12:
            self.__rows = row
            self.__columns = column
            return True
        else:

            return False


    def show_game(self):
        if not self.__isStarted:
            return
        coordonate_1_pionts = (16, 48)
        coordonate_2_pionts = (8, 28, 28, 48)
        coordonate_3_pionts = (8, 24, 24, 40, 40, 56)

        for x in range(len(self.__cases)):
            for y in range(len(self.__cases[x])):
                case = self.__cases[x][y]
                if case.has_changed():
                    case.set_changed(False)
                    canvas1 = tkinter.Canvas(self.__gameFrame)
                    canvas1.grid(row=x, column=y, padx=0, pady=0)
                    canvas1.config(width=64, height=64, highlightbackground="red", highlightcolor="red",
                                   highlightthickness=1, bg='#004F61')

                    if case.get_pawn() == 1:
                        canvas1.create_oval(x + coordonate_1_pionts[0], y + coordonate_1_pionts[0],
                                            x + coordonate_1_pionts[1], y + coordonate_1_pionts[1],
                                            fill=self.__colors[case.get_player()])
                    elif case.get_pawn() == 2:
                        canvas1.create_oval(x + coordonate_2_pionts[0], y + coordonate_2_pionts[0],
                                            x + coordonate_2_pionts[1], y + coordonate_2_pionts[1],
                                            fill=self.__colors[case.get_player()])
                        canvas1.create_oval(x + coordonate_2_pionts[2], y + coordonate_2_pionts[2],
                                            x + coordonate_2_pionts[3], y + coordonate_2_pionts[3],
                                            fill=self.__colors[case.get_player()])
                    elif case.get_pawn() == 3:
                        canvas1.create_oval(x + coordonate_3_pionts[0], y + coordonate_3_pionts[0],
                                            x + coordonate_3_pionts[1], y + coordonate_3_pionts[1],
                                            fill=self.__colors[case.get_player()])
                        canvas1.create_oval(x + coordonate_3_pionts[2], y + coordonate_3_pionts[2],
                                            x + coordonate_3_pionts[3], y + coordonate_3_pionts[3],
                                            fill=self.__colors[case.get_player()])
                        canvas1.create_oval(x + coordonate_3_pionts[4], y + coordonate_3_pionts[4],
                                            x + coordonate_3_pionts[5], y + coordonate_3_pionts[5],
                                            fill=self.__colors[case.get_player()])
                    canvas1.bind('<Button-1>', lambda event, coord=(x, y): self.play(coord))

    def play(self, coord):
        coordX = coord[0]
        coordY = coord[1]
        case = self.__cases[coordX][coordY]
        if case.get_player() == self.__players[self.__counter - 1] or case.get_player() == 0:
            case.set_changed(True)
            if case.get_pawn() == case.get_max_pawn():
                self.blast(coordX, coordY)
            else:
                self.put_pawn(coordX, coordY)
            if self.handle_round():
                self.show_game()

    def put_pawn(self, coordX, coordY):
        self.__cases[coordX][coordY].set_player(self.__players[self.__counter - 1])
        self.__cases[coordX][coordY].increment_pawn()

    def case_type(self, coordX, coordY):
        if coordX == 0 and coordY == 0:
            return 1  # La case est un coin
        if coordX == 0 and coordY == self.__columns - 1:
            return 1  # La case est un coin
        if coordX == self.__rows - 1 and coordY == 0:
            return 1  # La case est un coin
        if coordX == self.__rows - 1 and coordY == self.__columns - 1:
            return 1  # La case est un coin
        if coordX == 0:
            return 2  # La case est un côté
        if coordX == self.__rows - 1:
            return 2  # La case est un côté
        if coordY == 0:
            return 2  # La case est un côté
        if coordY == self.__columns - 1:
            return 2  # La case est un côté
        else:
            return 3  # La case n'est ni un côté ni un coin

    def blast(self, coordX, coordY):  # Je change l'attribut de la couleur joueur des cases   A FAIRE
        self.__cases[coordX][coordY].set_pawn(0)
        self.__cases[coordX][coordY].set_player(0)
        if coordX != 0:
            self.__cases[coordX - 1][coordY].set_player(self.__players[self.__counter - 1])
            self.chain_reaction(coordX - 1, coordY)
        if coordX != self.__rows - 1:
            self.__cases[coordX + 1][coordY].set_player(self.__players[self.__counter - 1])
            self.chain_reaction(coordX + 1, coordY)
        if coordY != 0:
            self.__cases[coordX][coordY - 1].set_player(self.__players[self.__counter - 1])
            self.chain_reaction(coordX, coordY - 1)
        if coordY != self.__columns - 1:
            self.__cases[coordX][coordY + 1].set_player(self.__players[self.__counter - 1])
            self.chain_reaction(coordX, coordY + 1)

    def chain_reaction(self, coordX, coordY):
        if self.__cases[coordX][coordY].get_pawn() == self.__cases[coordX][coordY].get_max_pawn():
            self.blast(coordX, coordY)
        else:
            self.put_pawn(coordX, coordY)

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
