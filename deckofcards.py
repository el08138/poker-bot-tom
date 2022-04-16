"""
Created on Sun May 24 20:28:34 2020
Deck of cards
@author: Stamatis
"""

""" import libraries """
from modules import ImageEditor as imgedt
import matplotlib.image as mpimg
import random

class Card:
    def __init__(self, rank, figure, suit):
        self.rank = rank
        self.figure = figure
        self.suit = suit
    
    def __repr__(self):
        return "{} of {}".format(self.figure, self.suit)
        
    def show(self):
        img = mpimg.imread('Images/{}{}.jpg'.format(self.figure, self.suit[0]))
        imgedt().print_image(img)


        
class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        
    def __repr__(self):
        return "Standard deck of cards: {0} cards remaining".format(len(self.cards))
    
    def create_deck(self):
        for s in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
            for i in range(2,11):
                self.cards.append(Card(i,str(i),s))
            for r,f in enumerate(['J', 'Q', 'K', 'A']):
                self.cards.append(Card(r+11,f,s))
                
    def reveal(self):
        for c in self.cards: c
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def cut(self, cutting_point=random.randint(0,51)):
        self.cards = self.cards[cutting_point:] + self.cards[:cutting_point]
        
    def drawCard(self):
        return self.cards.pop()
        
    
    
    