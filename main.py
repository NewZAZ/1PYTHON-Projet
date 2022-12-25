class case:
    def __init__(self, nbrmaxpions, nbrpions=0, joueurs=0):
        self.__nbrpions = nbrpions
        self.__nbrmaxpions = nbrmaxpions
        self.__joueurs = joueurs

    def Set_Joueurs(self, x):
        self.__joueurs = x

    def Get_Joueurs(self):
        return self.__joueurs

    def AjoutPion(self):
        self.__nbrpions += 1

    def Set_NbrPions(self, x):
        self.__nbrpions = x

    def get_nbrpions(self):
        return self.__nbrpions

    def get_nbrmaxpions(self):
        return self.__nbrmaxpions


class jeu:
    def __init__(self, listejoueurs=[], compteur=1, poser=False,
                 couleurs={1: "bleu", 2: "rouge", 3: "jaune", 4: "vert", 5: "orange", 6: "rose", 7: "violet",
                           8: "cyan"}):
        self.listejoueurs = listejoueurs
        self.couleurs = couleurs
        self.compteur = compteur
        self.Nombrejoueurs()
        self.CompteurJoueur()
        self.TailleJeu()
        self.poser = poser
        self.__cases = [[case(self.QuelTypeCases(i, j), 0, 0) for j in range(self.colonnes)] for i in
                        range(self.lignes)]

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
        print("Le gagnant estle joueur ", self.listejoueurs[0])

    def PossiblePoserPion(self):
        for lignes in self.__cases:
            for case in lignes:
                if (case.Get_Joueurs() == self.compteur):
                    return True
        else:
            return False

    def TailleJeu(self):
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
            return self.TailleJeu()

    def Nombrejoueurs(self):
        self.nbrjoueurs = eval(input("Nombre de joueurs, si 1 joueur, une IA sera votre adversaire"))
        if 1 < self.nbrjoueurs < 9:
            return self.nbrjoueurs
        else:
            return self.Nombrejoueurs()

    def affichage(self):
        for lignes in self.__cases:
            for case in lignes:
                print(case.get_nbrpions(), end="")
            print()

    def affichageJ(self):
        for lignes in self.__cases:
            for case in lignes:
                print(case.Get_Joueurs(), end="")
            print()

    def Jouer(self, coordX, coordY):
        if self.__cases[coordX][coordY].Get_Joueurs() == self.compteur or self.__cases[coordX][
            coordY].Get_Joueurs() == 0:
            if self.__cases[coordX][coordY].get_nbrpions() == self.__cases[coordX][coordY].get_nbrmaxpions():
                self.Explosion(coordX, coordY)
            else:
                self.AjouterPion(coordX, coordY)
            self.Tour()
            self.affichage()

    def AjouterPion(self, coordX, coordY):
        self.__cases[coordX][coordY].Set_Joueurs(self.compteur)
        self.__cases[coordX][coordY].AjoutPion()

    def QuelTypeCases(self, coordX, coordY):
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

    def Explosion(self, coordX, coordY):  # Je change l'attribut de la couleur joueur des cases   A FAIRE
        self.__cases[coordX][coordY].Set_NbrPions(0)
        self.__cases[coordX][coordY].Set_Joueurs(0)
        if coordX != 0:
            self.__cases[coordX - 1][coordY].Set_Joueurs(self.compteur)
            self.ReactionEnChaines(coordX - 1, coordY)
        if coordX != self.lignes - 1:
            self.__cases[coordX + 1][coordY].Set_Joueurs(self.compteur)
            self.ReactionEnChaines(coordX + 1, coordY)
        if coordY != 0:
            self.__cases[coordX][coordY - 1].Set_Joueurs(self.compteur)
            self.ReactionEnChaines(coordX, coordY - 1)
        if coordY != self.colonnes - 1:
            self.__cases[coordX][coordY + 1].Set_Joueurs(self.compteur)
            self.ReactionEnChaines(coordX, coordY + 1)

    def ReactionEnChaines(self, coordX, coordY):
        if self.__cases[coordX][coordY].get_nbrpions() == self.__cases[coordX][coordY].get_nbrmaxpions():
            self.Explosion(coordX, coordY)
        else:
            self.AjouterPion(coordX, coordY)

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
