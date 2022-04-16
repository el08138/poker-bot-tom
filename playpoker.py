"""
Created on Fri Jun  5 23:57:21 2020
Play poker
@author: Stamatis
"""

""" import libraries """
from nlholdem import PokerGame
import os

""" set working directory """
os.chdir('/Files/Personal/Projects/Poker AI')

""" main function """
if __name__ == '__main__':
    # create the game
    game = PokerGame()
    # play until there is a winner
    while game.num_remaining_players > 1:
        # print game statistics
        game.statistics()
        # start hand
        game.start_hand()
        # play hand
        winner = game.play_hand()
        # end hand
        game.end_hand(winner)