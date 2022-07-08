from random import randint
from tokenize import group
import pygame
from pygame.locals import *
from PIL import *  # pour les images
from inventaire import Inventaire
import main_menu
from generation import *
from mob import Mob

from projectile import Projectile
from selection import colisionItem, majSelection, majSelectionJoueur, selectionDispoItem
from game import Game
from item import Item
from game import background_pil
from findPos import *
fenetrePygame = ""
infoObject = 0
suiviePerso=160
global moveY, moveX
moveY=0
moveX=0
last = 0
annimIncendieListe=[]
annimTremblementListe=[]
annimIncendie=0

nombreAnnimationIncendie=3

#for i in range(1,10):
#    im = pygame.image.load("data/cata/tremblement/tremblement"+str(i)+".png")
#    annimTremblementListe.append(pygame.transform.scale(im, (im.get_width()*1.5, im.get_height()*1.5)))
for i in range(1,10):
    annimIncendieListe.append(pygame.image.load("data/cata/feu/flamme"+str(i)+".png"))
annimTremblementListe=annimIncendieListe
tailleEcran = [(3840, 2160), (2560, 1440), (1920, 1080),(1536,864),(1280, 720), (800, 600), (640, 480)]
# stocke la largeur et la hauteur de l'écran de l'utilisateur
# initialise la taille de l'écran (largeur, hauteur) en pixel
largeurEtHauteur = (0, 0)
modification = False
delayIncendie=500
timeComtpeur=0
def pygameInit():  # fonction servant à l'initialisation pygame
    
    global infoObject, modification, joueur,timeComtpeur, annimIncendie, delayIncendie,nombreAnnimationIncendie, annimTremblementListe
    global largeurEtHauteur, fenetrePygame, moveX, moveY, last
     #if Options.music == True:
    
    
    #music = pygame.mixer.music.load("data/Music/level0.mp3")
    # pygame.mixer.music.play(10)
    print("Génération de la map")
    imDebug = pygame.image.load("data/tuiles/debug.png")
    imDebug = pygame.transform.scale(imDebug, (2,2))
    BLACK = (0, 0, 0)
    continuer = True  # répeter à l'infini la fenetre pygame jusqu'a que continuer = false
    fenetrePygame = pygame.init()  # Initialisation de la bibliothèque Pygame
    pygame.mixer.init()

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 30)

    infoObject = pygame.display.Info()  # récupère la taille de l'écran
    affichagePersonalise = affichage()
    fenetrePygame = pygame.display.set_mode(
        (tailleEcran[affichagePersonalise][0], tailleEcran[affichagePersonalise][1]), pygame.DOUBLEBUF, pygame.FULLSCREEN)
    game = Game(infoObject, fenetrePygame)
    
    
    
    
    # mise a l'echelle du perso les argument sont la surface qui est modifie et la taille
    # valeur de x qui place perso au milieu de l'ecran sur l'axe horizontale
    Imselection = pygame.image.load("data/tuiles/selection.png").convert_alpha()
    buttonHome = pygame.image.load("data/menu/buttonHome.png").convert_alpha()
    buttonHome = pygame.transform.scale(buttonHome, (70, 70))
    bookicon = pygame.image.load("data/menu/book.png").convert_alpha()
    bookicon = pygame.transform.scale(bookicon,(50,50))

    librairieIMG = pygame.image.load("data/personnages/infoBulle/librairie.png").convert_alpha()
    health = pygame.image.load("data/menu/health.png").convert_alpha()
    health = pygame.transform.scale(health, (50, 50))
    feuille = pygame.image.load("data/menu/feuille.png").convert_alpha()
    feuille = pygame.transform.scale(feuille, (50, 50))
    listeInfoButton = [("data/menu/scierie")]

    tick_ressource=0
    move_ticker=0
    cooldown=0
    tuile=False
    fini=True
    librairie=False
    tickBatiment=1000

    inventaire=Inventaire(0,0, [])

    for i in range(-1, 2):
        for j in range(-1, 2):
            game.deleteFog(game.joueur.posX+i, game.joueur.posY+j)
    game.genererImg()


    for deplacement in range(1675-infoObject.current_w):
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerX(-4)
        game.joueur.rect.x-=4 

        moveX-=4
    
    for deplacement in range(1250-infoObject.current_h):
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerY(-4)
        game.joueur.rect.y-=4

        moveY-=4
    
    #game.groupMob.add(Mob(game,"golem_des_forets", 100, 2, tuile=game.map[1][1]))
    #game.groupMob.add(Mob(game, "oursin", 150, 3, pique=True, tuile=game.map[1][2]))
    #game.groupMob.add(Mob(game, "kraken", 50, 1, aquatique=True))
    #game.groupMob.add(Mob(game, "dragon", 100, 2,game.map[1][1], aerien=True))
    #game.groupMob.add(Mob(game, "mage", 50, 1, game.map[1][1]))
    #the_path = [[game.groupMob.sprites()[0].posY, game.groupMob.sprites()[0].posX]]
    #fleche= Projectile(game, "fleche", 10, 0,0, game.joueur)
    #game.groupProjectile.add(fleche)
    game.debutDePartie=pygame.time.get_ticks()
    while continuer == True:
        
        
        game.augmenterMob()
        
        modification=False
        cliqueItem = False
        modification, tuileTemp = KEY_move(game, game.joueur, fenetrePygame)
        
        listeColide = game.checkCollision(game.joueur, game.groupMob)
        
        
        for mob in game.groupMob:#Gestion des pieux
            
            if mob.name=="oursin":
                if game.avoirTuileJoueur(mob).trou:
                    game.joueur.changerImageBatiment(game.avoirTuileJoueur(mob), "trou_bouche")
                    pygame.mixer.Sound.play(game.son.trou)
                    modification=True
                    game.avoirTuileJoueur(mob).aEteModifie=True
                    game.avoirTuileJoueur(mob).trou=False
                    mob.kill()
                    
            
            tuileMob=majSelectionJoueur(game, pos=(mob.getFeet()))
            if not mob.pique and not mob.aerien and tuileMob.pieux:
            #if game.map[mob.posY][mob.posX].pieux==True:
                mob.takeDamage(0.1)
                if not mob.slow:
                    mob.slow =True


            elif tuileMob.sableMouvant and not mob.aerien:
                mob.takeDamage(0.3)
                pygame.mixer.Sound.play(game.son.sableMouvantPassage, maxtime=2000)
                if not mob.slow:
                    mob.slow =True
                    
                    mob.velocity=mob.velocity/3
                    if mob.velocity<1:
                        mob.velocity=1
                        
            elif tuileMob.ventilo and not mob.aerien:
                mob.takeDamage(0.5)
                pygame.mixer.Sound.play(game.son.ventilo, maxtime=2000)
                if not mob.slow:
                    mob.slow =True
                    
                    mob.velocity=mob.velocity/3
                    if mob.velocity<1:
                        mob.velocity=1
                        
            elif mob.slow:
                 mob.slow =False
                 mob.velocity =mob.maxVelocity
                 
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
                
                
            

        
            if event.type == pygame.MOUSEBUTTONDOWN:  # si clic souris
                
                for item in inventaire.listeItem: 
                    if colisionItem(item, pygame.mouse.get_pos()) and tuile: #on a une tuile de selectionné
                        batimentConstruit = game.joueur.construireBatiment(tuile, item)
                        modification=True
                        cliqueItem=True
                        if not batimentConstruit:
                            tickBatiment=0
                            
                            

                if mouse[0] <= 75 and mouse[1] <= 75:  # detection si clic sur menu pricipal
                    continuer = False
                    main_menu.load =False
                if mouse[0] <= bookicon.get_width() and mouse[1] <= bookicon.get_height()+80 and mouse[1] >= 80:  # detection si clic sur menu pricipal
                    if librairie ==True : 
                        librairie = False 
                    else : 
                        librairie = True 
                else :
                    librairie = False
                if not cliqueItem:
                    tuile = majSelection(game, pygame.mouse.get_pos(), game.joueur)
                else :
                    if tuile:
                        tuile.estSelect=False
                    tuile=False
            
                
        if continuer == True:  # récupère la position de la souris mais uniquement si la fenetre pygame est ouverte
            mouse = pygame.mouse.get_pos()
            deplacement_cam(mouse, game, game.joueur, game.groupMob)
            
           
            #### Deplacement des mobs
            now = pygame.time.get_ticks()
            for mob in game.groupMob:
                
                if now-mob.last>=mob.cooldown and mob.fini and not (game.map[game.joueur.posY][game.joueur.posX].estMer() and not mob.aquatique and not mob.aerien) and not (not game.map[game.joueur.posY][game.joueur.posX].estMer() and mob.aquatique):
                    mob.the_path = findPos(game, game.joueur.posX, game.joueur.posY, mob.posX, mob.posY, aqua=mob.aquatique, aerien=mob.aerien)
                    
                    mob.last = now
                    mob.majCoolDown()
                if not mob.slow:
                    mob.fini = mob.allerVersTuile(mob.the_path[0][1], mob.the_path[0][0])
                else :
                    if now%2==0:
                        mob.fini = mob.allerVersTuile(mob.the_path[0][1], mob.the_path[0][0])
                        
                if mob.fini and len(mob.the_path)>1:
                    mob.the_path = mob.the_path[1:]

            for tour in game.groupDefense:
                tour.attack()
            for projo in game.groupProjectile:
                projo.moveProjectile()

            if move_ticker>0:
                move_ticker-=1

            # efface l'image pour pouvoir actualiser le jeu
            fenetrePygame.fill(BLACK)

            ####CATASTROPHE

            
                
                
                
                
            modification=True
            #affichage selection
            if tick_ressource==0:
                tick_ressource=600
                game.joueur.ajouterRessources()
                game.spawMob()
                tuileCata = game.majCata()
                if game.incendie and tuileCata:
                    annimIncendieListe.append(tuileCata)
                    annimTremblementListe.append(tuileCata)
                    choixIncendie = random.randint(0,1)
                    if choixIncendie:
                        pygame.mixer.Sound.play(game.son.incendie, maxtime=4000)
                    else:
                        #pygame.mixer.Sound.play(game.son.tremblement)
                        pass
            else:
                tick_ressource-=1

            if modification:

                game.genererImg()

            fenetrePygame.blit(game.mapImg, (moveX, moveY))
            fenetrePygame.blit(buttonHome, (10, 10))
            fenetrePygame.blit(bookicon, (0,80))
            
            if tuile :  
                fenetrePygame.blit(Imselection, (tuile.getRectX(), tuile.getRectY()))  
                if tuile.tour:      
                    #pygame.draw.circle(fenetrePygame, (155,155,155), (tuile.tour.rect.x+30, tuile.tour.rect.y), tuile.tour.range, width=3, )
                    pass
            #affichage personnage
            
            if not game.joueur.bateau:
                fenetrePygame.blit(game.joueur.skin, (game.joueur.rect.x, game.joueur.rect.y))
            for mob in game.groupMob:
                if game.map[mob.posY][mob.posX].isExplored :
                    fenetrePygame.blit(mob.skin, (mob.rect.x, mob.rect.y))
                fenetrePygame.blit(imDebug, mob.getFeet())

            if game.joueur.bateau:
                fenetrePygame.blit(game.joueur.skinBateau, (game.joueur.rect.x-15, game.joueur.rect.y+30))
                
            for mob in game.groupMob:
                if game.map[mob.posY][mob.posX].isExplored:
                    mob.update_health_bar()
            if tuile :
                liste = selectionDispoItem(game, tuile, game.joueur)
                inventaire = Inventaire(tuile.getRectX()-85, tuile.getRectY()-25, liste)
                inventaire.blitInventaire(fenetrePygame)
                for item in inventaire.listeItem:
                        if colisionItem(item, pygame.mouse.get_pos()):##INFO BULLE##
                            inventaire.blitInfoBulle(fenetrePygame, item)
            for projectile in game.groupProjectile:              
                fenetrePygame.blit(projectile.img, (projectile.rect.x, projectile.rect.y))                

            
            for collision in listeColide:
                fenetrePygame.blit(game.imCollision,(random.randint(game.joueur.rect.x-20, game.joueur.rect.x+20), random.randint(game.joueur.rect.y, game.joueur.rect.y+120)))
            
            if (annimIncendie or  game.incendie) and type(annimIncendieListe[-1])==Tuile :
                if choixIncendie:
                    entreImage=100
                    fenetrePygame.blit(annimIncendieListe[annimIncendie], (annimIncendieListe[-1].rect.x+50, annimIncendieListe[-1].rect.y-annimIncendieListe[annimIncendie].get_height()+100))
                else:
                    entreImage=500
                    fenetrePygame.blit(annimTremblementListe[annimIncendie], (annimTremblementListe[-1].rect.x+50, annimTremblementListe[-1].rect.y-annimTremblementListe[annimIncendie].get_height()+100))
                game.incendie=False
                if pygame.time.get_ticks()-delayIncendie>entreImage:
                    annimIncendie+=1

                    
                    delayIncendie=pygame.time.get_ticks()
                    if annimIncendie==9:
                        if nombreAnnimationIncendie>0:
                            annimIncendie=1
                            nombreAnnimationIncendie-=1
                        else:
                            game.joueur.detruireBatimentRessource(annimIncendieListe[-1])
                            annimIncendieListe.pop(len(annimIncendieListe)-1)
                            annimTremblementListe.pop(len(annimTremblementListe)-1)
                            nombreAnnimationIncendie=3
                            annimIncendie=0

            
            
            #if game.joueur.estMort:
            #    fenetrePygame.blit(pygame.image.load("data/menu/gameover.png").convert_alpha(), (200,200))
            if librairie ==True :
                    fenetrePygame.blit(librairieIMG,(infoObject.current_w-librairieIMG.get_width()-(infoObject.current_w-librairieIMG.get_width())/2,200))
            for i in range(len(game.joueur.ressourcesIMG)):
                fenetrePygame.blit(game.joueur.ressourcesIMG[i], (infoObject.current_w-190-(190*i), 25))
                fenetrePygame.blit(game.joueur.RessourcesTEXT[i], (infoObject.current_w-120-(190*i), 3/100*infoObject.current_h))
                if game.joueur.RessourcesInfoModified[i] != False:
                    timeComtpeur +=1
                    if timeComtpeur <=60 :
                        fenetrePygame.blit(game.joueur.RessourcesInfoModified[i],(infoObject.current_w-95-(190*i),90))
                    else :
                        timeComtpeur = 0
                        game.joueur.resetRessourcesModified()
            game.joueur.update_health_bar()
            game.joueur.update_ecolo_bar()
            fenetrePygame.blit(health, (120,15))
            fenetrePygame.blit(feuille, (10,155))
            if tickBatiment<60:
                fenetrePygame.blit(game.imageErreurRessource, (infoObject.current_w-game.imageErreurRessource.get_width()-(infoObject.current_w-game.imageErreurRessource.get_width())/2,infoObject.current_h - 200))
                tickBatiment+=1

                
            if librairie ==True : 
                i =0
                for mob in game.groupMob : 
                    i+=1
                    fenetrePygame.blit(mob.infoBulle,(50*i,150))
                    
            pygame.display.flip()
        
        else:
            print("Fermeture du jeu & Lancement du menu principal")
            #main_menu.Main_Menu()
            pygame.display.quit()
            pygame.quit()  # ferme pygame et le jeu
            fenetrePygame=""
            return
        clock.tick(60)
           











def affichage():
        for i in range(len(tailleEcran)):
            if tailleEcran[i][0] == infoObject.current_w and tailleEcran[i][1] == infoObject.current_h:
                return i
        return 2
    
def KEY_move(game,joueur,fenetre):
    modification=False
    tuile=False
    keys=pygame.key.get_pressed()
    
    if keys[K_d] or keys[K_RIGHT]:
        if joueur.deplacementAutorise("droite") :
            deplacementCamDroite((infoObject.current_w-suiviePerso, 0), game, game.joueur, game.groupMob)
            joueur.goRight()
            tuile = majSelectionJoueur(game, joueur.getFeet())
            joueur.setPos(tuile)
            #joueur.majBateau()
            for i in range(-1,2):
                for j in range(-1, 2):
                    if game.deleteFog(joueur.posX+i, joueur.posY+j): ##MODIFICATION
                        modification=True

                
                
    if keys[K_q]or keys[K_LEFT]:
            if joueur.deplacementAutorise("gauche"):
                deplacementCamGauche((suiviePerso, 0), game, game.joueur, game.groupMob)
                #joueur.majBateau()
                joueur.goLeft()
                tuile = majSelectionJoueur(game, joueur.getFeet())
                joueur.setPos(tuile)
                for i in range(-1,2):
                    for j in range(-1, 2):
                        if game.deleteFog(joueur.posX+i, joueur.posY+j): ##MODIFICATION
                            modification=True
    

    if keys[K_z] or keys[K_UP]:
            if joueur.deplacementAutorise("haut"):
                deplacementCamHaut((0, suiviePerso), game, game.joueur, game.groupMob)
                #joueur.majBateau()
                joueur.goUp()
                tuile = majSelectionJoueur(game, joueur.getFeet())
                joueur.setPos(tuile)
                for i in range(-1,2):
                    for j in range(-1, 2):
                        if game.deleteFog(joueur.posX+i, joueur.posY+j): ##MODIFICATION
                            modification=True

    if keys[K_s]or keys[K_DOWN]:
            
            if joueur.deplacementAutorise("bas"):
                deplacementCamBas((0, infoObject.current_h-suiviePerso), game, game.joueur, game.groupMob)
                joueur.goDown()
                tuile = majSelectionJoueur(game, joueur.getFeet())
                joueur.setPos(tuile)
                #joueur.majBateau()
                for i in range(-1,2):
                    for j in range(-1, 2):
                        if game.deleteFog(joueur.posX+i, joueur.posY+j): ##MODIFICATION
                            modification=True
                
        
    if keys[K_b]:
        if game.map[joueur.posY][joueur.posX].port:
            joueur.bateau=True
    if keys[K_v]:
        if game.map[joueur.posY][joueur.posX].port:
            joueur.bateau = False

    return modification, tuile


def deplacement_cam(mouse, game, joueur, listeMob): #gestion du déplacement de la caméra 
    deplacementCamBas(mouse, game, joueur, listeMob)
    deplacementCamDroite(mouse, game, joueur, listeMob)
    deplacementCamGauche(mouse, game, joueur, listeMob)
    deplacementCamHaut(mouse, game, joueur, listeMob)
    
    

    

    
        
        
    

def deplacementCamBas(mouse, game, joueur, listeMob):
    global moveY, moveX
    x=infoObject.current_h-mouse[1]
    y=f(x)
    
    if x < 200 :  # Si souris en bas
        print(x)
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerY(y)
        joueur.rect.y+=y
        moveY+=y
        for mob in listeMob:
            mob.rect.y+=y
        for projo in game.groupProjectile:
            projo.rect.y+=y
        for defense in game.groupDefense:
            defense.rect.y+=y
    

def deplacementCamHaut(mouse, game, joueur, listeMob):
    global moveY, moveX
    x = mouse[1]
    y = -f(x)
    
    if x < 200 : #Si souris en haut
        print(x)
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerY(y)
        joueur.rect.y+=y
        moveY+=y
        for mob in listeMob:
            mob.rect.y+=y
        for projo in game.groupProjectile:
            projo.rect.y+=y
        for defense in game.groupDefense:
            defense.rect.y+=y
        
def deplacementCamGauche(mouse, game, joueur, listeMob):
    global moveY, moveX
    x= mouse[0]
    y = -f(x)
    if x < 200:  # Si souris à gauche
        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerX(y)
        joueur.rect.x+=y
        for mob in listeMob:
            mob.rect.x+=y
        moveX+=y
        for projo in game.groupProjectile:
            projo.rect.x+=y
        for defense in game.groupDefense:
            defense.rect.x+=y
        
def deplacementCamDroite(mouse, game, joueur, listeMob):
    global moveY, moveX
    x = infoObject.current_w-mouse[0]
    y=f(x)

    if x < 200:  # Si souris à droite

        for i in range(len(game.map)):
            for j in range(len(game.map[0])):
                game.map[i][j].decalerX(y)
        joueur.rect.x+=y
        moveX+=y
        for mob in listeMob:
            mob.rect.x+=y
        for projo in game.groupProjectile:
            projo.rect.x+=y
        for defense in game.groupDefense:
            defense.rect.x+=y


def f(x):  #fonction vitesse deplacement cam
    y  = round(x*0.04-10)
    if y>20:
        return 15
    return y