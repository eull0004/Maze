from random import *
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
                for elt in self.get_contiguous_cells((i,j)):
                    if not elt in self.neighbors[(i,j)] and [elt,(i,j)] not in L:
                        L.append([(i,j),elt])
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

    def get_cell_walls(self, c1):
        L = []
        c2 = (c1[0],c1[1]+1)
        c3 = (c1[0]+1,c1[1])
        if c2 in self.get_cells() and c2 not in self.neighbors[c1]:
            L.append((c1,c2))
        if c3 in self.get_cells() and c3 not in self.neighbors[c1]:
            L.append((c1,c3))
        return L 

    
    @classmethod
    def gen_btree(self,h,w):
        self = Maze(h, w, empty = False)
        for i in range(h):
            for j in range(w):
                if len(self.get_cell_walls((i,j))) == 2:
                    a = randint(0, 1)
                    if a == 1:
                        self.remove_wall((i,j),(i+1,j))
                    if a == 0:
                        self.remove_wall((i,j),(i,j+1))
                elif len(self.get_cell_walls((i,j))) == 1:
                    self.remove_wall((i,j), self.get_cell_walls((i,j))[0][1])
        return self

    
    @classmethod
    def gen_sidewinder(self,h,w):
        self = Maze(h, w, empty = False)
        for i in range(h-1):
            sequence = []
            for j in range(w-1):
                sequence.append((i,j))
                a = randint(0, 1)
                if a == 0:
                    self.remove_wall((i,j), (i,j+1))
                if a == 1:
                    b = randint(0, len(sequence)-1)
                    self.remove_wall(sequence[b], (sequence[b][0]+1,sequence[b][1]))
                    sequence = []
            sequence.append((i,w-1))
            c = randint(0, len(sequence)-1)
            self.remove_wall(sequence[c], (sequence[c][0]+1,sequence[c][1]))
        for k in range(w-1):
            self.remove_wall((h-1,k),(h-1,k+1))
        return self
    

    @classmethod
    def gen_fusion(self,h,w):
        self = Maze(h, w, empty = False)
        cells = []
        count = 1
        label = []
        for i in range(h):
            for j in range((w)):
                cells.append((i,j))
                label.append(count)
                count += 1
        fusion = dict(zip(cells, label))
        l_mur = []
        
        for elmnt in self.get_walls():
            l_mur.append(elmnt)
        shuffle(l_mur)
        
        for i in range((h*w)-1):
            if fusion[l_mur[i][0]] != fusion[l_mur[i][1]]:
                self.remove_wall(l_mur[i][0], l_mur[i][1])
                label_cell = fusion[l_mur[i][0]]
                for cle in fusion.keys():
                    if fusion[cle] == label_cell:
                        fusion[cle] = fusion[l_mur[i][1]]
        return self
    @classmethod
    def gen_exploration(self,h,w):
        self = Maze(h , w, empty = False)
        a = randint(0, len(self.get_cells())-1)
        cellule = self.get_cells()[a]
        visite = [cellule]
        pile = [cellule]

        while len(pile) != 0:
            cell_retire = pile.pop(0)
            if self.neighbors[cell_retire] not in visite:
                pile.insert(0, cell_retire)
                not_visite = []
                for i in range(len(self.get_contiguous_cells(cell_retire))):
                    if self.get_contiguous_cells(cell_retire) not in visite:
                        not_visite.append(self.get_contiguous_cells(cell_retire)[i])
                b = randint(0,len(not_visite)-1)
                cell_contigue = not_visite[b]
                self.remove_wall(pile[0], cell_contigue)
                visite.append(cell_contigue)
                pile.insert(0, cell_contigue)
                
        return self
    
    @classmethod
    def gen_wilson(self,h,w):
        self = Maze(h,w,empty = False)
        all_cells = []
        for elmt in self.get_cells():
            all_cells.append(elmt)
        marquage = [all_cells[randint(0,len(all_cells)-1)]]
        marquage_toutes_cellules = False
        while not marquage_toutes_cellules: #Tant qu’il reste des cellules non marquées :
            # - Choisir une cellule de départ au hasard, parmi les cellules non marquées
            cellule_depart = (-1,-1)
            while cellule_depart == (-1,-1):
                cellule_test = all_cells[randint(0,len(all_cells)-1)]
                if not cellule_test in marquage:
                    cellule_depart = cellule_test
            
            '''- Effectuer une marche aléatoire jusqu’à ce qu’une cellule marquée soit atteinte (en cas de boucle, 
            si la tête du snake se mord la queue, « couper » la boucle formée 
            [autrement dit, supprimer toutes étapes depuis le précédent passage])'''
            chemin = []
            murs_to_destruct = []
            boucleEnCours = True
            cellule_actuelle = cellule_depart
            while boucleEnCours:
                # obtenir les cellules contigu et en sélectionner 1 au hasard
                cell_contigu = []
                for elmnt in self.get_contiguous_cells(cellule_actuelle):
                    cell_contigu.append(elmnt)
                cellule_suivante = cell_contigu[randint(0,len(cell_contigu)-1)]
                
                while cellule_suivante == cellule_depart: # cas ou je me mords la qeue
                    cellule_suivante = cell_contigu[randint(0,len(cell_contigu)-1)]
                
                # ajout de la cellule suivante  dans l'historique
                chemin.append(cellule_suivante)
                
                #ajout des murs (cellule précédente et cellule sélectionner)
                '''wall_got_destruct = False'''  # a t-on casser un mur lors de notre passage
                if [cellule_suivante,cellule_actuelle] in self.get_walls():
                    murs_to_destruct.append([cellule_suivante,cellule_actuelle])
                    '''wall_got_destruct = True'''
                if [cellule_actuelle,cellule_suivante] in self.get_walls(): # meme que au dessus mais il est impossible que les deux s'active en meme temps
                    murs_to_destruct.append([cellule_actuelle,cellule_suivante])
                    '''wall_got_destruct = True'''
                # stoper la boucle
                if cellule_suivante in marquage:
                    boucleEnCours = False
                cellule_suivante = cellule_actuelle
            
            # - Marquer chaque cellule du chemin, et casser tous les murs rencontrés, jusqu’à la cellule marquée
            marquage.append(chemin)
            for i in range(len(murs_to_destruct)):
                self.remove_wall(murs_to_destruct[i][0],murs_to_destruct[i][1])
            
            # verif état marquage  pour stop boucle
            marquage_sans_doublons = []
            compteur = 0
            for elt in marquage:
                for elmt in all_cells:
                    if elt == elmt and elt not in marquage_sans_doublons:
                        compteur += 1
                        marquage_sans_doublons.append(elt)
            if compteur == len(all_cells):
                marquage_toutes_cellules = True
        return self