class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty):
        """
        Constructeur d'un labyrinthe de height cellules de haut,
        de width cellules de large et d'un empty ayant comme valeur un booléen
        Les voisinages sont initialisés à des ensembles vides
        Si empty = True, contruction d'une grille où chaque cellule a pour voisines celles qu'elles touchent donc aucun mur n'est généré
        Et si empty = False, construction d'une grille où aucune cellule n’a de voisines donc tous les murs sont générés.
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}
        self.empty = empty
        
        if empty == True:
             for i in range(1,height):
                for j in range(width):
                    self.neighbors[(i,j)].add((i-1,j)) 
                    self.neighbors[(i-1,j)].add((i,j))
                    self.neighbors[(j,i)].add((j,i-1)) 
                    self.neighbors[(j,i-1)].add((j,i)) 
        elif empty == False:
            for i in range(1,height):
                for j in range(width):
                    if (i,j) in self.neighbors[(i-1,j)]:
                        self.neighbors[(i-1,j)].remove((i,j)) 
                    elif (i-1,j) in self.neighbors[(i,j)]:
                        self.neighbors[(i,j)].remove((i-1,j))
                    elif (j,i) in self.neighbors[(j,i-1)]:
                        self.neighbors[(j,i-1)].remove((j,i)) 
                    elif (j,i-1) in self.neighbors[(j,i)]:
                        self.neighbors[(j,i)].remove((j,i-1))
        
    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt