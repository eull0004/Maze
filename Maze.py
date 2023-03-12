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
        Si empty = True, contruction d'une grille où chaque cellule a pour voisines celles qui lui sont contigües donc aucun mur n'est généré
        Et si empty = False, construction d'une grille où aucune cellule n’a de voisines donc tous les murs sont générés
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}
        self.empty     = empty
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

    """
    Méthodes d'instance permettant d'ajouter un mur entre deux cellules c1 et c2 placées en paramètres
    Version robuste permettant de tester la présence des sommets dans la grille
    """
    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire

    """
    Méthode d'instance permettant d'obtenir la liste des cellules de la grille
    afin de faciliter par la suite d'autres méthodes d'instance
    """
    def get_cells(self):
        L = []
        for i in range(self.height):
            for j in range(self.width):
                L.append((i,j))
        return L
    
    """
    Méthode d'instance permettant de retirer un mur entre deux cellules c1 et c2 placées en paramètre.
    Mais donc de les ajouter dans leurs voisines respectives.
    """
    def remove_wall(self,c1,c2):
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)

    """
    Méthode d'instance permettant d'obtenir la liste de tous les murs de la grille.
    """
    def get_walls(self):
        L = []
        for i in range(self.height):
            for j in range(self.width):
                c1 = (i,j)
                c2 = (c1[0],c1[1]+1)
                c3 = (c1[0]+1,c1[1])
                if c2 in self.get_cells() and c2 not in self.neighbors[c1]:
                    L.append((c1,c2))
                elif c3 in self.get_cells() and c3 not in self.neighbors[c1]:
                    L.append((c1,c3))
        return L

    """
    Méthode d'instance permettant d'ajouter tous les murs possibles dans le labyrinthe.
    """
    def fill(self):
        for i in range(self.width):
            for j in range(self.height):
                voisin_lst = []
                for elt in self.neighbors[(i,j)]:
                    voisin_lst.append(elt)
                for k in range(len(voisin_lst)):
                    self.neighbors[(i,j)].remove(voisin_lst[k])
                    self.neighbors[voisin_lst[k]].remove((i,j))

    """
    Méthode d'instance permettant de retirer tous les murs du labyrinthe.
    """
    def empty_(self):
         for i in range(1,self.height):
                for j in range(self.width):
                    self.neighbors[(i,j)].add((i-1,j)) 
                    self.neighbors[(i-1,j)].add((i,j))
                    self.neighbors[(j,i)].add((j,i-1)) 
                    self.neighbors[(j,i-1)].add((j,i))

    """
    Méthode d'instance permettant d'obtenir la liste de toutes les cellules touchant la cellule c mise en paramètre
    On ne prend pas en compte les murs. 
    """
    def get_contiguous_cells(self, c):
        contigue = []
        i = c[0]
        j = c[1]
        if i-1 >= 0:
            contigue.append((i-1,j))
        if i+1 < self.height:
            contigue.append((i+1,j))
        if j-1 >= 0:
            contigue.append((i,j-1))
        if j+1 < self.width:
            contigue.append((i,j+1))
        return contigue

    """
    Méthode d'instance permettant d'obtenir la liste de toutes les cellules atteignables depuis la cellule c mise en paramètre
    C'est à dire les cellules touchant c n'étant pas séparées par un mur.
    """
    def get_reachable_cells(self, c):
        access = []
        for i in range(len(self.get_contiguous_cells(c))):
            if c in self.neighbors[self.get_contiguous_cells(c)[i]] and self.get_contiguous_cells(c)[i] in self.neighbors[c]:
                access.append(self.get_contiguous_cells(c)[i])
        return access 
    
    """
    Méthode d'instance permettant d'obtenir la liste des murs d'une cellule c1 placées en paramètre.
    """
    def get_cell_walls(self, c1):
        L = []
        c2 = (c1[0],c1[1]+1)
        c3 = (c1[0]+1,c1[1])
        if c2 in self.get_cells() and c2 not in self.neighbors[c1]:
            L.append((c1,c2))
        if c3 in self.get_cells() and c3 not in self.neighbors[c1]:
            L.append((c1,c3))
        return L 