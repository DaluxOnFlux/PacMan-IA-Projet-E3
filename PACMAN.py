import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

caseDuParcours = np.count_nonzero(TBL != 1)


# Carte des distances des pacgums
CDD = np.zeros(TBL.shape,dtype=np.int32)
CDD[TBL == 1] = 1000 # les murs sont à distance infinie
CDD[TBL != 1] = caseDuParcours # les cases vides sont à distance max

# Carte des distancess des fantomes
CDDG = np.zeros(TBL.shape,dtype=np.int32)
CDDG[TBL == 1] = 1000 # les murs sont à distance infinie
CDDG[TBL != 1] = caseDuParcours # les maisons des fantomes sont à distance infinie



# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
         elif ( TBL[x][y] == 1):
            GUM[x][y] = 5
   return GUM
            
GUM = PlacementsGUM()   
CDD[GUM == 1] = 0 # les pacgums sont à distance 0



      

PacManPos = [5,5]


Ghosts  = []
#Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink", (0, 0)])
#Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", (0, 0)])
#Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan", (0, 0)])
#Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red", (0, 0)])




##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################
def Collision():
   global PacManPos, Ghosts
   for ghost in Ghosts:
      if PacManPos[0] == ghost[0] and PacManPos[1] == ghost[1]:
         return True
   return False
   

def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 or TBL[x][y-1] == 0): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 or TBL[x][y+1] == 0): L.append((0, 1))
   if ( TBL[x+1][y] == 2 or TBL[x+1][y] == 0): L.append(( 1,0))
   if ( TBL[x-1][y] == 2 or TBL[x-1][y] == 0): L.append((-1,0))
   return L
   
def IAPacman():
   global PacManPos, Ghosts, CDD
   #deplacement Pacman
   L = PacManPossibleMove()
   min_distance = float('inf')
   next_move = None
   for move in L:
      new_x = PacManPos[0] + move[0]
      new_y = PacManPos[1] + move[1]
      if CDD[new_x][new_y] < min_distance:
         min_distance = CDD[new_x][new_y]
         next_move = move
   if next_move:
      PacManPos[0] += next_move[0]
      PacManPos[1] += next_move[1]
   return Collision()
   



   µ
def IAGhosts():
   #deplacement Fantome
   for F in Ghosts:
      x, y = F[0], F[1]
      dx, dy = F[3] # direction actuelle
      L = GhostsPossibleMove(x,y)
      
      # Si le fantôme est dans un couloir, continuer dans la direction actuelle
      if (dx, dy) in L and len(L) == 2:  # Le fantôme peut continuer et il est dans un couloir (2 directions possibles)
            new_dx, new_dy = dx, dy
      else:
            choix = random.randrange(len(L))
            new_dx = L[choix][0]
            new_dy = L[choix][1]
            

      # Mettre à jour la position et la direction
      F[0], F[1] = x + new_dx, y + new_dy
      F[3] = (new_dx, new_dy)
      #print(F)
   return Collision()
      
"""
def updateCDD():
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (TBL[x][y] == 0):
            neighbors = [CDD[x][y-1], CDD[x][y+1], CDD[x+1][y], CDD[x-1][y]]
            minimal = min(neighbors)
            if CDD[x][y] != 0: 
               CDD[x][y] = minimal + 1
            SetInfo1(x, y, minimal+1)
"""

G = 999  # une valeur G très grande
M = LARGEUR * HAUTEUR 
axes = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def updateCDD():
   global CDD, axes, G, M

   update = True

   while update:
      update = False
      for y in range(1, HAUTEUR-1):
         for x in range(1, LARGEUR-1):
               if CDD[x][y] != G:
                  voisins = []
                  for dx, dy in axes:
                     nx = x + dx
                     ny = y + dy
                     if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                        voisins.append((nx, ny))

                  voisinsVal = []

                  for nx, ny in voisins:
                        voisinsVal.append(CDD[nx][ny])
                  
                  min_val = min(voisinsVal)

                  if CDD[x][y] > min_val + 1:
                     CDD[x][y] = min_val + 1
                     anyUpdate = True
                  SetInfo1(x, y, CDD[x][y])
               
"""
def updateCDDG():
   for i in range(LARGEUR):
      for j in range(HAUTEUR):
"""        
            

   




def PacmanEatGum():
   global pacManScore
   if GUM[PacManPos[0]][PacManPos[1]] == 1:  # si la pos du pacman est sur un pacgum
      GUM[PacManPos[0]][PacManPos[1]] = 0    # on enleve le pacgum
      CDD[PacManPos[0]][PacManPos[1]] = caseDuParcours
      pacManScore = pacManScore + 100


#  Boucle principale de votre jeu appelée toutes les 500ms
pacManScore = 0
iteration = 0
gameOver = False
def PlayOneTurn():
   global iteration
   global pacManScore
   global gameOver

   if not PAUSE_FLAG and not gameOver: 
      PacmanEatGum()
      updateCDD()
      #updateCDDG()
      iteration += 1
      if iteration % 2 == 0 :   
         if IAPacman(): gameOver = True
      else:                     
         if IAGhosts(): gameOver = True

   Affiche(PacmanColor = "yellow", message = "Score : "+str(pacManScore))  
   print("")
   print("")
   print(CDD)

###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   