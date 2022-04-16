"""
Created on Wed May 27 18:50:51 2020
Play poker GUI
@author: Stamatis
"""

""" import libraries """
from nlholdem import PokerGameGUI
from tkinter import *
from PIL import ImageTk,Image  
import os
import tkinter.font as font

""" set working directory """
os.chdir('/Files/Personal/Projects/Poker AI')

""" initialize tkinter object """
root = Tk()
root.title("Welcome to Tom's Poker Room!")
root.iconbitmap('Images/Original/Aces.ico')
widgets = dict()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
font_family = 'Bookman Old Style'

""" initialize positions for every widget """
positions = dict()
positions['poker_table'] = [0, 0]
positions['player_names_entries'] = [[970, 170], [1265, 250], [1225, 530], [950, 580], [695, 580], [443, 580], [180, 550], [110, 290], [380, 170]]
positions['game_settings'] = [650, 290]
positions['prize_pool'] = [0, 0]
positions['player_actions'] = [1080, 730]
positions['raise_amount'] = [1259, 680]
positions['dealer'] = [690, 260]
positions['button'] = [[928, 260], [1110, 340], [1157, 477], [950, 496], [705, 496], [468, 496], [280, 420], [355, 284], [432, 260]]
positions['player_hands'] = dict()
positions['player_hands'][1] = [[948, 260], [988, 260]]
positions['player_hands'][2] = [[1130, 270], [1170, 270]]
positions['player_hands'][3] = [[1157, 388], [1197, 388]]
positions['player_hands'][4] = [[970, 426], [1010, 426]]
positions['player_hands'][5] = [[725, 426], [765, 426]]
positions['player_hands'][6] = [[488, 426], [528, 426]]
positions['player_hands'][7] = [[300, 420], [340, 420]]
positions['player_hands'][8] = [[274, 304], [314, 304]]
positions['player_hands'][9] = [[452, 260], [492, 260]]
positions['player_bets'] = dict()
positions['player_bets'][1] = [1048, 260]
positions['player_bets'][2] = [1230, 338]
positions['player_bets'][3] = [1257, 388]
positions['player_bets'][4] = [1070, 494]
positions['player_bets'][5] = [825, 494]
positions['player_bets'][6] = [588, 494]
positions['player_bets'][7] = [400, 488]
positions['player_bets'][8] = [374, 304]
positions['player_bets'][9] = [552, 260]
positions['player_info'] = dict()
positions['player_info'][1] = [1050, 25]
positions['player_info'][2] = [1380, 140]
positions['player_info'][3] = [1430, 400]
positions['player_info'][4] = [1055, 650]
positions['player_info'][5] = [750, 650]
positions['player_info'][6] = [445, 650]
positions['player_info'][7] = [80, 500]
positions['player_info'][8] = [90, 200]
positions['player_info'][9] = [410, 25]
positions['board'] = dict()
positions['board'][0] = [625, 330]
positions['board'][1] = [680, 330]
positions['board'][2] = [735, 330]
positions['board'][3] = [790, 330]
positions['board'][4] = [845, 330]

""" create intro screen """
poker_table_empty_img = ImageTk.PhotoImage(Image.open('Images/Original/Poker_Table_v1_Empty.jpg'))
poker_table_full_img = ImageTk.PhotoImage(Image.open('Images/Original/Poker_Table_v1_Full.png'))
widgets['poker_table'] = Label(image=poker_table_empty_img)
widgets['poker_table'].place(x=positions['poker_table'][0], y=positions['poker_table'][1])

""" create entry widgets for player names """
widgets['player_names_entries'] = []
for i in range(9):
    widgets['player_names_entries'].append(Entry(root, justify='center'))
    widgets['player_names_entries'][-1].place(x=positions['player_names_entries'][i][0], y=positions['player_names_entries'][i][1])
    widgets['player_names_entries'][-1]['font'] = font.Font(family=font_family, size=10)

""" poker settings frame """
# game settings frame
widgets['game_settings'] = LabelFrame(root, bg='#FCE6C9', padx=5, pady=5)
widgets['game_settings'].place(x=positions['game_settings'][0], y=positions['game_settings'][1])
# title
widgets['title_settings'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Poker Game - Settings', justify='center')
widgets['title_settings'].grid(row=0, column=0, columnspan=2)
widgets['title_settings']['font'] = font.Font(family=font_family, size=14)
# small blind
widgets['small_blind_label'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Small blind')
widgets['small_blind_label'].grid(row=1, column=0)
widgets['small_blind_label']['font'] = font.Font(family=font_family, size=10)
widgets['small_blind_entry'] = Entry(widgets['game_settings'], justify='center')
widgets['small_blind_entry'].grid(row=1, column=1)
widgets['small_blind_entry']['font'] = font.Font(family=font_family, size=10)
# big blind
widgets['big_blind_label'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Big blind')
widgets['big_blind_label'].grid(row=2, column=0)
widgets['big_blind_label']['font'] = font.Font(family=font_family, size=10)
widgets['big_blind_entry'] = Entry(widgets['game_settings'], justify='center')
widgets['big_blind_entry'].grid(row=2, column=1)
widgets['big_blind_entry']['font'] = font.Font(family=font_family, size=10)
# buy-in
widgets['buy_in_label'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Buy-in')
widgets['buy_in_label'].grid(row=3, column=0)
widgets['buy_in_label']['font'] = font.Font(family=font_family, size=10)
widgets['buy_in_entry'] = Entry(widgets['game_settings'], justify='center')
widgets['buy_in_entry'].grid(row=3, column=1)
widgets['buy_in_entry']['font'] = font.Font(family=font_family, size=10)
# starting stack
widgets['starting_stack_label'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Starting stack')
widgets['starting_stack_label'].grid(row=4, column=0)
widgets['starting_stack_label']['font'] = font.Font(family=font_family, size=10)
widgets['starting_stack_entry'] = Entry(widgets['game_settings'], justify='center')
widgets['starting_stack_entry'].grid(row=4, column=1)
widgets['starting_stack_entry']['font'] = font.Font(family=font_family, size=10)
# blind change
widgets['blind_change_label'] = Label(widgets['game_settings'], bg='#FCE6C9', text='Blinds change every')
widgets['blind_change_label'].grid(row=5, column=0)
widgets['blind_change_label']['font'] = font.Font(family=font_family, size=10)
widgets['blind_change_entry'] = Entry(widgets['game_settings'], justify='center')
widgets['blind_change_entry'].grid(row=5, column=1)
widgets['blind_change_entry']['font'] = font.Font(family=font_family, size=10)

""" initialize game and create main screen """
def initialize_game():
    game = PokerGameGUI(root, widgets, positions, font_family)
    # destroy old widgets
    widgets['game_settings'].destroy()
    for widget in widgets['player_names_entries']:
        widget.destroy()
    # change screen
    widgets['poker_table'].configure(image=poker_table_full_img)
    # initialize widgets
    game.initialize_widgets()   
widgets['start_game'] = Button(widgets['game_settings'], text='Start game', command=initialize_game)
widgets['start_game'].grid(row=6, column=0, columnspan=2)
widgets['start_game']['font'] = font.Font(family=font_family, size=12)

""" play game """
root.mainloop()