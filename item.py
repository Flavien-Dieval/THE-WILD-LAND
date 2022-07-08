import pygame

class Item(pygame.sprite.Sprite):

    def __init__(self, game, nom, coutWater, coutFood, coutWood, coutStone) :
        self.game = game
        self.nom = nom
        self.image = game.images.returnImItem(nom)
        self.coutWater = coutWater
        self.coutWood = coutWood
        self.coutFood = coutFood
        self.coutStone = coutStone
        self.infoBulle =game.images.ImInfoBullItem(nom)
        self.rect = self.image.get_rect()