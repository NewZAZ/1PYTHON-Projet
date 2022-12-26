import tkinter


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
    def __init__(self, listejoueurs=[], compteur=1, poser=False):
        self.couleurs = {1: "bleu", 2: "rouge", 3: "jaune", 4: "vert", 5: "orange", 6: "rose", 7: "violet",
                         8: "cyan"}
        self.listejoueurs = listejoueurs
        self.compteur = compteur
        self.nombre_joueurs()
        self.CompteurJoueur()
        self.taille_jeu()
        self.poser = poser
        self.__cases = [[Case(self.quel_type_case(i, j), 0, 0) for j in range(self.colonnes)] for i in
                        range(self.lignes)]
        self.__root = tkinter.Tk()
        self.__root.title("Example of GUI")
        self.__frame1 = tkinter.Frame(self.__root)
        self.affichage()
        self.affichageJ()
        self.__frame1.grid(row=0, column=0, rowspan=2)
        self.__root.mainloop()

    def CompteurJoueur(self):
        for k in range(1, self.nbrjoueurs + 1):
            self.listejoueurs.append(k)

    def Gagnant(self):
        if len(self.listejoueurs) == 1:
            return True
        else:
            return False

    def Tour(self):
        if self.Gagnant() == False:
            if self.poser == True:
                if self.compteur == len(self.listejoueurs):
                    self.compteur = self.listejoueurs[0]
                else:
                    self.compteur += 1
                if self.PossiblePoserPion() == False:
                    self.listejoueurs.remove(self.compteur)
                    self.Tour()
            else:
                if self.compteur == len(self.listejoueurs):
                    self.compteur = self.listejoueurs[0]
                    self.poser = True
                else:
                    self.compteur += 1
        else:
            self.FinDePartie()

    def FinDePartie(self):
        print("Le gagnant est le joueur ", self.listejoueurs[0])

    def PossiblePoserPion(self):
        for lignes in self.__cases:
            for case in lignes:
                if (case.get_joueurs() == self.compteur):
                    return True
        else:
            return False

    def taille_jeu(self):
        x = input("lignes")
        y = input("colonnes")
        if x == "" and y == "":
            self.lignes = 8
            self.colonnes = 5
            return self.lignes, self.colonnes
        if 3 <= eval(x) <= 10 and 3 <= eval(y) <= 12:
            self.lignes = eval(x)
            self.colonnes = eval(y)
            return self.lignes, self.colonnes
        else:
            print("TA TAILLE N'EST PAS ADAPTEE")
            return self.taille_jeu()

    def nombre_joueurs(self):
        self.nbrjoueurs = eval(input("Nombre de joueurs, si 1 joueur, une IA sera votre adversaire"))
        if 1 < self.nbrjoueurs < 9:
            return self.nbrjoueurs
        else:
            return self.nombre_joueurs()

    def affichage(self):
        for x in range(len(self.__cases)):
            for y in range(len(self.__cases[x])):
                case = self.__cases[x][y]
                if case.has_changed():
                    canvas1 = tkinter.Canvas(self.__frame1)
                    canvas1.grid(row=x, column=y)
                    canvas1.config(width=5, height=5, highlightthickness=1, bd=0,
                                   bg=self.couleurs[case.get_joueurs()])
                    canvas1.bind('<Button-1>', lambda event, coord=(x, y): self.jouer(coord))

    def affichageJ(self):
        for lignes in self.__cases:
            for case in lignes:
                print(case.get_joueurs(), end="")
            print()

    def jouer(self, coord):
        coordX = coord[0]
        coordY = coord[1]
        case = self.__cases[coordX][coordY]
        if case.get_joueurs() == self.compteur or case.get_joueurs() == 0:
            case.set_changed(True)
            if case.get_nbrpions() == case.get_nbrmaxpions():
                self.explosion(coordX, coordY)
            else:
                self.ajouter_pion(coordX, coordY)
            self.Tour()
            self.affichage()

    def ajouter_pion(self, coordX, coordY):
        self.__cases[coordX][coordY].set_joueurs(self.compteur)
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
            self.__cases[coordX - 1][coordY].set_joueurs(self.compteur)
            self.reaction_en_chaines(coordX - 1, coordY)
        if coordX != self.lignes - 1:
            self.__cases[coordX + 1][coordY].set_joueurs(self.compteur)
            self.reaction_en_chaines(coordX + 1, coordY)
        if coordY != 0:
            self.__cases[coordX][coordY - 1].set_joueurs(self.compteur)
            self.reaction_en_chaines(coordX, coordY - 1)
        if coordY != self.colonnes - 1:
            self.__cases[coordX][coordY + 1].set_joueurs(self.compteur)
            self.reaction_en_chaines(coordX, coordY + 1)

    def reaction_en_chaines(self, coordX, coordY):
        if self.__cases[coordX][coordY].get_nbrpions() == self.__cases[coordX][coordY].get_nbrmaxpions():
            self.explosion(coordX, coordY)
        else:
            self.ajouter_pion(coordX, coordY)

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
