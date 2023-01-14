import tkinter
from tkinter import *
from tkinter import messagebox as mb


class Case:
    def __init__(self, nbrmaxpions, nbrpions=0, joueurs=0):
        self.__nbrpions = nbrpions
        self.__nbrmaxpions = nbrmaxpions
        self.__joueurs = joueurs
        self.__has_changed = True

    def set_joueurs(self, x):
        self.__joueurs = x
        self.set_changed(True)

    def get_joueurs(self):
        return self.__joueurs

    def ajout_pion(self):
        self.__nbrpions += 1
        self.set_changed(True)

    def set_nbr_pions(self, x):
        self.__nbrpions = x
        self.set_changed(True)

    def get_nbrpions(self):
        return self.__nbrpions

    def get_nbrmaxpions(self):
        return self.__nbrmaxpions

    def has_changed(self):
        return self.__has_changed

    def set_changed(self, boolean):
        self.__has_changed = boolean


class Game:
    def __init__(self):
        self.__cases = None
        self.__nextPlayerCanvas = None
        self.__playerSelectCanvas = None
        self.__rowText = None
        self.__columnText = None
        self.__selectionFrame = None
        self.__isStarted = False
        self.listejoueurs = []
        self.compteur = 1
        self.__gameFrame = None
        self.__colors = {1: "blue", 2: "red", 3: "yellow", 4: "green", 5: "orange", 6: "pink", 7: "purple",
                         8: "cyan"}

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
        if self.listejoueurs.count(color) == 1:
            canvas.config(bg='white')
            self.listejoueurs.remove(color)
        else:
            canvas.config(bg='green')
            self.listejoueurs.append(color)

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

        if self.taille_jeu((int(columns)), int(rows)):
            if len(self.listejoueurs) > 1:
                self.startGame()
            else:
                mb.showerror("Erreur", "Veuillez choisir minimum 2 joueurs !")
        else:
            mb.showerror("Erreur", "Veuillez choisir une taille de jeux conforme !")

    def startGame(self):
        self.__selectionFrame.destroy()
        self.__isStarted = True

        self.poser = False
        self.__cases = [[Case(self.quel_type_case(i, j), 0, 0) for j in range(self.colonnes)] for i in
                        range(self.lignes)]

        self.compteur = 1
        self.nombre_joueurs()
        self.showNextPlayer()

        self.__gameFrame = tkinter.Frame(self.__root)
        self.affichage()
        self.__gameFrame.grid(row=0, column=0, rowspan=5)

    def Gagnant(self):
        if len(self.listejoueurs) == 1:
            return True
        else:
            return False

    def Tour(self):
        if not self.__isStarted:
            return
        if not self.Gagnant():
            if self.poser:
                if self.compteur == len(self.listejoueurs):
                    self.compteur = 1
                else:
                    self.compteur += 1
                if not self.PossiblePoserPion():
                    self.listejoueurs.pop(self.compteur - 1)
                    self.compteur -= 1
                    self.Tour()
            else:
                if self.compteur == len(self.listejoueurs):
                    self.compteur = 1
                    self.poser = True
                else:
                    self.compteur += 1
            self.showNextPlayer()
            return True
        else:
            self.FinDePartie()
            return False

    def showNextPlayer(self):
        if not self.__isStarted:
            return
        self.__nextPlayerCanvas = Canvas(self.__root, width=64, height=64)

        print(self.listejoueurs, self.compteur - 1)
        self.__nextPlayerCanvas.create_oval(8, 56, 56, 8, fill=self.__colors[self.listejoueurs[self.compteur - 1]])

        self.__nextPlayerCanvas.grid(pady=10, column=0, row=5)
        self.__nextPlayerCanvas.config(bg='black', borderwidth=0, highlightthickness=0)

    def FinDePartie(self):
        self.show_selection()
        self.__gameFrame.destroy()
        self.__nextPlayerCanvas.delete("all")
        mb.showinfo("Gagnant", "le joueur " + self.__colors[self.listejoueurs[0]] + " a gagner !")
        self.__isStarted = False
        self.clear_game()

    def PossiblePoserPion(self):
        for lignes in self.__cases:
            for case in lignes:
                if case.get_joueurs() == self.listejoueurs[self.compteur - 1]:
                    return True
        else:
            return False

    def taille_jeu(self, column, row):
        if 3 <= row <= 10 and 3 <= column <= 12:
            self.lignes = row
            self.colonnes = column
            return True
        else:

            return False

    def nombre_joueurs(self):
        # self.nbrjoueurs = eval(input("Nombre de joueurs, si 1 joueur, une IA sera votre adversaire"))
        self.nbrjoueurs = len(self.listejoueurs)
        if 1 < self.nbrjoueurs < 9:
            return self.nbrjoueurs
        else:
            return self.nombre_joueurs()

    def affichage(self):
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

                    if case.get_nbrpions() == 1:
                        canvas1.create_oval(x + coordonate_1_pionts[0], y + coordonate_1_pionts[0],
                                            x + coordonate_1_pionts[1], y + coordonate_1_pionts[1],
                                            fill=self.__colors[case.get_joueurs()])
                    elif case.get_nbrpions() == 2:
                        canvas1.create_oval(x + coordonate_2_pionts[0], y + coordonate_2_pionts[0],
                                            x + coordonate_2_pionts[1], y + coordonate_2_pionts[1],
                                            fill=self.__colors[case.get_joueurs()])
                        canvas1.create_oval(x + coordonate_2_pionts[2], y + coordonate_2_pionts[2],
                                            x + coordonate_2_pionts[3], y + coordonate_2_pionts[3],
                                            fill=self.__colors[case.get_joueurs()])
                    elif case.get_nbrpions() == 3:
                        canvas1.create_oval(x + coordonate_3_pionts[0], y + coordonate_3_pionts[0],
                                            x + coordonate_3_pionts[1], y + coordonate_3_pionts[1],
                                            fill=self.__colors[case.get_joueurs()])
                        canvas1.create_oval(x + coordonate_3_pionts[2], y + coordonate_3_pionts[2],
                                            x + coordonate_3_pionts[3], y + coordonate_3_pionts[3],
                                            fill=self.__colors[case.get_joueurs()])
                        canvas1.create_oval(x + coordonate_3_pionts[4], y + coordonate_3_pionts[4],
                                            x + coordonate_3_pionts[5], y + coordonate_3_pionts[5],
                                            fill=self.__colors[case.get_joueurs()])
                    canvas1.bind('<Button-1>', lambda event, coord=(x, y): self.jouer(coord))

    def jouer(self, coord):
        coordX = coord[0]
        coordY = coord[1]
        case = self.__cases[coordX][coordY]
        if case.get_joueurs() == self.listejoueurs[self.compteur - 1] or case.get_joueurs() == 0:
            case.set_changed(True)
            if case.get_nbrpions() == case.get_nbrmaxpions():
                self.explosion(coordX, coordY)
            else:
                self.ajouter_pion(coordX, coordY)
            if self.Tour():
                self.affichage()

    def ajouter_pion(self, coordX, coordY):
        self.__cases[coordX][coordY].set_joueurs(self.listejoueurs[self.compteur - 1])
        self.__cases[coordX][coordY].ajout_pion()

    def quel_type_case(self, coordX, coordY):
        if coordX == 0 and coordY == 0:
            return 1  # La case est un coin
        if coordX == 0 and coordY == self.colonnes - 1:
            return 1  # La case est un coin
        if coordX == self.lignes - 1 and coordY == 0:
            return 1  # La case est un coin
        if coordX == self.lignes - 1 and coordY == self.colonnes - 1:
            return 1  # La case est un coin
        if coordX == 0:
            return 2  # La case est un côté
        if coordX == self.lignes - 1:
            return 2  # La case est un côté
        if coordY == 0:
            return 2  # La case est un côté
        if coordY == self.colonnes - 1:
            return 2  # La case est un côté
        else:
            return 3  # La case n'est ni un côté ni un coin

    def explosion(self, coordX, coordY):  # Je change l'attribut de la couleur joueur des cases   A FAIRE
        self.__cases[coordX][coordY].set_nbr_pions(0)
        self.__cases[coordX][coordY].set_joueurs(0)
        if coordX != 0:
            self.__cases[coordX - 1][coordY].set_joueurs(self.listejoueurs[self.compteur - 1])
            self.reaction_en_chaines(coordX - 1, coordY)
        if coordX != self.lignes - 1:
            self.__cases[coordX + 1][coordY].set_joueurs(self.listejoueurs[self.compteur - 1])
            self.reaction_en_chaines(coordX + 1, coordY)
        if coordY != 0:
            self.__cases[coordX][coordY - 1].set_joueurs(self.listejoueurs[self.compteur - 1])
            self.reaction_en_chaines(coordX, coordY - 1)
        if coordY != self.colonnes - 1:
            self.__cases[coordX][coordY + 1].set_joueurs(self.listejoueurs[self.compteur - 1])
            self.reaction_en_chaines(coordX, coordY + 1)

    def reaction_en_chaines(self, coordX, coordY):
        if self.__cases[coordX][coordY].get_nbrpions() == self.__cases[coordX][coordY].get_nbrmaxpions():
            self.explosion(coordX, coordY)
        else:
            self.ajouter_pion(coordX, coordY)

    def clear_game(self):
        self.listejoueurs = []
        self.compteur = 1
        self.poser = False
        self.__cases = []

Game()
# A chaque tour -> on change de joueur,
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
