import tuto
from item import Item
def majSelection(game, pos, joueur=False, infoDehors=False):
    clicDehors=True
    tuileSelect = False
    souris = pos
    if not joueur:
        for i in range(game.taille_matriceY):
            for j in range(game.taille_matriceX):
                pos_in_mask = souris[0] - game.map[i][j].rect.x, souris[1] - game.map[i][j].rect.y
                touching = game.map[i][j].rect.collidepoint(souris) and game.map[i][j].mask.get_at(pos_in_mask)
                if touching :
                    clicDehors=False
                    if game.map[i][j].estSelect:
                        game.map[i][j].setSelect(False)
                        
                    else:
                        game.map[i][j].setSelect(True)
                        
                        tuileSelect = game.map[i][j]
                else :
                    game.map[i][j].setSelect(False)
    else:
        for i in range(-1, 2):
            for j in range(-1, 2):
                pos_in_mask = souris[0] - game.map[joueur.posY+i][joueur.posX+j].rect.x, souris[1] - game.map[joueur.posY+i][joueur.posX+j].rect.y
                touching = game.map[joueur.posY+i][joueur.posX+j].rect.collidepoint(souris) and game.map[joueur.posY+i][joueur.posX+j].mask.get_at(pos_in_mask)
                if touching :
                    clicDehors=False
                    if game.map[joueur.posY+i][joueur.posX+j].estSelect:
                        game.map[joueur.posY+i][joueur.posX+j].setSelect(False)
                        pass
                    else:
                        game.map[joueur.posY+i][joueur.posX+j].setSelect(True)
                        tuto.upadateStatutTuto(game,"select")
                        tuileSelect = game.map[joueur.posY+i][joueur.posX+j]
                else :
                    game.map[joueur.posY+i][joueur.posX+j].setSelect(False)
                    pass
    if not infoDehors:
        return tuileSelect
    else:
        return tuileSelect, clicDehors

def majSelectionJoueur(game, xSup=0, ySup=0): #xSup decalage en x
        tuileSelect = False
        souris = [game.joueur.getFeet()[0], game.joueur.getFeet()[1]]
        souris[0]+=xSup
        souris[1]+=ySup
        for i in range(-1,2):
            for j in range(-1,2):
                
                pos_in_mask = souris[0] - game.map[game.joueur.posY+i][game.joueur.posX+j].rect.x, souris[1] - game.map[game.joueur.posY+i][game.joueur.posX+j].rect.y
                touching = game.map[game.joueur.posY+i][game.joueur.posX+j].rect.collidepoint(souris) and game.map[game.joueur.posY+i][game.joueur.posX+j].mask.get_at(pos_in_mask)
                if touching :
                    tuileSelect = game.map[game.joueur.posY+i][game.joueur.posX+j]
                    return tuileSelect

        if not tuileSelect:
            print("attention majSelectionJoueur n'a pas trouvé de tuile en", souris)
            #Pour ne pas crash, decommenter la ligne suivante, après avoir fait suivre le bug
            return None
            assert(False)
        return tuileSelect

def majSelectionMob(game, mob, supX=0, supY=0): #version ultra opti de maj selection joueur
    tuileSelect = False
    for i in range(-1,2):
        for j in range(-1,2):
            if game.verifierCo(mob.posX+j, mob.posY+i):
                souris = [mob.getFeet()[0], mob.getFeet()[1]]
                souris[0]+=supX
                souris[1]+=supY
                pos_in_mask = souris[0] - game.map[mob.posY+i][mob.posX+j].rect.x, souris[1] - game.map[mob.posY+i][mob.posX+j].rect.y
                touching = game.map[mob.posY+i][mob.posX+j].rect.collidepoint(souris) and game.map[mob.posY+i][mob.posX+j].mask.get_at(pos_in_mask)
                if touching :
                    mob.tuileMob = game.map[mob.posY+i][mob.posX+j]
                    tuileSelect=mob.tuileMob

    if not tuileSelect:
        #print("attention majSelectionMob n'a pas trouvé de tuile en", souris)
        game.listeDebug.append([souris[0], souris[1]])
        #Pour ne pas crash, decommenter la ligne suivante, après avoir fait suivre le bug
        return None
        assert(False)
    return tuileSelect


def terreAutour(joueur, tuile):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not joueur.game.map[tuile.posY+i][tuile.posX+j].caseBloquante():
                return True
    return False

def selectionDispoItem(game, tuile, joueur):
    optionDIspo = []
    if tuile.isExplored :
        if tuile.type==1 and not tuile.elevage and not tuile.champs and not tuile.tour and not tuile.pieux and not tuile.ville and not tuile.statue:
            optionDIspo.append(Item(game, "elevage", 175, 25,0,0))
            optionDIspo.append(Item(game, "champs", 50, 0,0,0))
            optionDIspo.append(Item(game, "tour", 0, 0, 0, 300 ))
            optionDIspo.append(Item(game, "pieux", 0,0, 50, 50))
            if not joueur.statueFood:
                optionDIspo.append(Item(game, "statueFood", 0, 150,0,0))
            
        elif tuile.type==2 and not tuile.forge and not tuile.mine and not tuile.mortier and not tuile.ville and not tuile.forge and not tuile.statue:
            optionDIspo.append(Item(game, "mine", 0,0,50,50))
            optionDIspo.append(Item(game, "mortier", 0,0,0,200))
            if not joueur.statuePierre:
                optionDIspo.append(Item(game, "statuePierre", 0,0,0,150))
            
        elif tuile.type==3 and not tuile.moulin and not tuile.port and not tuile.ville  and not tuile.statue :
            optionDIspo.append(Item(game, "moulin", 0,0,100,0))
            if not joueur.statueEau:
                optionDIspo.append(Item(game, "statueEau", 150,0,0,0))
            
            if not game.avoirTuileJoueur(joueur).port and terreAutour(joueur, tuile):
                optionDIspo.append(Item(game, "port", 0,0,100,0))
                
                
        elif (tuile.type==4 or tuile.type==10) and not tuile.scierie and not tuile.ville and not tuile.statue:
            if not joueur.statueBois:
                optionDIspo.append(Item(game, "statueBois", 0,0,150,0))
            optionDIspo.append(Item(game, "scierie", 0,0,100,0))
        
        elif tuile.type==5 and not tuile.frigo and not tuile.ventilo and not tuile.ville:
            optionDIspo.append(Item(game, "frigo", 200, 50, 0, 0))
            optionDIspo.append(Item(game, "ventilo", 0, 0, 500, 400))
        elif tuile.type==6 and not tuile.sableMouvant and not tuile.trou and not tuile.ville:
            optionDIspo.append(Item(game, "sableMouvant", 150, 100,0,0))
            optionDIspo.append(Item(game, "trou", 20,0, 10, 0))
            optionDIspo.append(Item(game, "ville", 0, 0,0,1000))
        elif tuile.type==7 and not game.boss:
            if not tuile.forge:
                optionDIspo.append(Item(game, "forge", 0,0,0,50))
            else:
                if joueur.nomArmure==None:
                    optionDIspo.append(Item(game, "armure1", 0, 100,0,0))
                elif joueur.nomArmure=="armure1":
                    optionDIspo.append(Item(game, "armure2", 0, 150,0,50))
                elif joueur.nomArmure=="armure2":
                    optionDIspo.append(Item(game, "armure3", 0, 250,0,150))
                elif joueur.nomArmure=="armure3":
                    optionDIspo.append(Item(game, "armure4", 0, 350,0,250))
                if joueur.nomProj=="joueur":
                    optionDIspo.append(Item(game, "marteau1", 0, 150,0,100))
                elif joueur.nomProj=="marteau1":
                    optionDIspo.append(Item(game, "marteau2", 0, 300,0,200))
    return optionDIspo


def colisionItem(item, pos):
    return item.rect.collidepoint(pos)
